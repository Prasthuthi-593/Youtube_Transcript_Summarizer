from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    if 'watch?v=' in url:
        video_id = url.split('watch?v=')[1]
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1]
    else:
        return "Invalid YouTube URL", 400

    transcript = get_transcript(video_id)
    if not transcript:
        return "Failed to retrieve transcript", 500

    summary = get_summary(transcript)
    return summary, 200

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        return None

def get_summary(transcript):
    prompt = """You are Yotube video summarizer. You will be taking the transcript text
    and summarizing the entire video and providing the important summary in points
    within 250 words. Please provide the summary of the text given here:  """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript)
    return response.text

if __name__ == '__main__':
    app.run()
