function RunSentimentAnalysis() {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    fetch(`/sentimentAnalyzer?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
        .then(response => response.json())
        .then(data => {
            const label = data.label;
            const score = data.score;

            let emoji = "😐", color = "warning";

            if (label === "Positive") {
                emoji = "😊";
                color = "success";
            } else if (label === "Negative") {
                emoji = "😠";
                color = "danger";
            }

            document.getElementById("system_response").innerHTML = `
                <div class="card border-${color} mb-3" style="max-width: 30rem;">
                    <div class="card-header bg-${color} text-white">Sentiment Result ${emoji}</div>
                    <div class="card-body">
                        <p class="card-text">The given text has been identified as <strong>${label}</strong> with a score of <strong>${score}</strong>.</p>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            document.getElementById("system_response").innerText = "Error occurred: " + error;
        });
}
