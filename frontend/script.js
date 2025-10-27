// UPDATE THIS LINE WITH YOUR REAL BACKEND URL
const API_URL = "https://quote-api-5r6y.onrender.com/random";

const quoteEl = document.getElementById("quote");
const authorEl = document.getElementById("author");
const tagFilter = document.getElementById("tag-filter");
const newQuoteBtn = document.getElementById("new-quote");
const copyBtn = document.getElementById("copy-quote");
const statusEl = document.getElementById("status");

async function fetchQuote() {
  const tag = tagFilter.value;
  const url = tag ? `${API_URL}?tag=${tag}` : API_URL;

  try {
    statusEl.textContent = "Loading...";
    const res = await fetch(url);
    const data = await res.json();

    if (data.error) {
      quoteEl.textContent = data.error;
      authorEl.textContent = "";
      statusEl.textContent = "Try another tag";
      return;
    }

    // Safely display quote
    quoteEl.textContent = `"${data.content}"`;
    authorEl.textContent = `— ${data.author}`;
    statusEl.textContent = "";

  } catch (err) {
    console.error("Fetch error:", err);
    quoteEl.textContent = "Failed to load quote";
    authorEl.textContent = "";
    statusEl.textContent = "Check internet";
  }
}

function copyQuote() {
  const text = `${quoteEl.textContent} ${authorEl.textContent}`;
  navigator.clipboard.writeText(text).then(() => {
    statusEl.textContent = "Copied!";
    setTimeout(() => statusEl.textContent = "", 2000);
  });
}

// Event Listeners
newQuoteBtn.addEventListener("click", fetchQuote);
copyBtn.addEventListener("click", copyQuote);
tagFilter.addEventListener("change", fetchQuote);

// Load first quote
fetchQuote();