function RunSentimentAnalysis() {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    fetch(`/sentimentAnalyzer?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById("system_response").innerText = data;
        })
        .catch(error => {
            document.getElementById("system_response").innerText = "Error occurred: " + error;
        });
}
