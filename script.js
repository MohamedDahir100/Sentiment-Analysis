function processVideo() {
    let url = document.getElementById('youtubeUrl').value;
    if (url) {
        analyzeSentiment(url);
    }
}

function analyzeSentiment(url) {
    let resultDisplay = document.getElementById('sentimentResult');
    resultDisplay.innerHTML = "Loading..."; 
    fetch(`http://127.0.0.1:5000/analyze?url=${encodeURIComponent(url)}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        let resultDisplay = document.getElementById('sentimentResult');
        let formattedScore = parseFloat(data.average_score).toFixed(2);  
        resultDisplay.innerHTML = "Sentiment analysis result: " + data.sentiment + 
                                  ", with an average score of " + formattedScore + "%";
    })
    .catch((error) => {
        console.error('Error:', error);
        let resultDisplay = document.getElementById('sentimentResult');
        resultDisplay.innerHTML = "Error processing sentiment analysis.";
    });
}


