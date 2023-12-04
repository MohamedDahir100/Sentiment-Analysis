function processVideo() {
    var url = document.getElementById('youtubeUrl').value;
    if (url) {
        analyzeSentiment(url);
    }
}

function analyzeSentiment(url) {
    fetch('http://127.0.0.1:5000/analyze', {  // Replace with your actual server URL if not running locally
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    })
    .then(response => response.json())
    .then(data => {
        var resultDisplay = document.getElementById('sentimentResult');
        resultDisplay.innerHTML = "Sentiment analysis result: " + JSON.stringify(data.sentiments);
    })
    .catch((error) => {
        console.error('Error:', error);
        var resultDisplay = document.getElementById('sentimentResult');
        resultDisplay.innerHTML = "Error processing sentiment analysis.";
    });
}
