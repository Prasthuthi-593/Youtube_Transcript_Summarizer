const btn = document.getElementById("summarise");
btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Summarising...";
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var url = tabs[0].url;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                var text = xhr.responseText;
                const p = document.getElementById("output");
                p.innerHTML = text;
            } else {
                const p = document.getElementById("output");
                p.innerHTML = "Error: " + xhr.responseText;
            }
            btn.disabled = false;
            btn.innerHTML = "Summarise";
        }
        xhr.onerror = function() {
            const p = document.getElementById("output");
            p.innerHTML = "Request failed";
            btn.disabled = false;
            btn.innerHTML = "Summarise";
        }
        xhr.send();
    });
});
