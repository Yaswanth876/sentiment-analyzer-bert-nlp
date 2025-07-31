// static/mywebscript.js

// Attach event listener to ensure DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('sentimentForm');
  const responseDiv = document.getElementById('system_response');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Clear previous response and show loading state
    responseDiv.innerHTML = '<div class="text-center my-3"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    // Retrieve input
    const text = document.getElementById('textToAnalyze').value.trim();
    if (!text) {
      responseDiv.innerHTML = '<div class="alert alert-warning">Please enter some text to analyze.</div>';
      return;
    }

    try {
      // Fetch sentiment from backend API
      const params = new URLSearchParams({ text });
      const res = await fetch(`/sentiment?${params.toString()}`);

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();

      // Display result
      const { sentiment, confidence } = data;
      responseDiv.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Sentiment: <span class="text-primary">${sentiment.toUpperCase()}</span></h5>
            <p class="card-text">Confidence: ${(confidence * 100).toFixed(2)}%</p>
          </div>
        </div>
      `;

    } catch (error) {
      console.error(error);
      responseDiv.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
    }
  });
});
