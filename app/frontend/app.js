// API endpoint
const API_URL = "/api";

// DOM elements
const englishInput = document.getElementById("english-input");
const spanishOutput = document.getElementById("spanish-output");
const translateBtn = document.getElementById("translate-btn");
const clearBtn = document.getElementById("clear-btn");
const btnText = document.getElementById("btn-text");
const btnSpinner = document.getElementById("btn-spinner");
const errorMessage = document.getElementById("error-message");

// Translate function
async function translate() {
  const text = englishInput.value.trim();

  // Validate input
  if (!text) {
    showError("Please enter some text to translate.");
    return;
  }

  if (text.length > 500) {
    showError("Text is too long. Maximum 500 characters.");
    return;
  }

  // Show loading state
  setLoading(true);
  hideError();
  spanishOutput.value = "";

  try {
    const response = await fetch(`${API_URL}/translate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Translation failed");
    }

    const data = await response.json();
    spanishOutput.value = data.translated_text;
  } catch (error) {
    console.error("Translation error:", error);
    showError(`Translation failed: ${error.message}`);
  } finally {
    setLoading(false);
  }
}

// Set loading state
function setLoading(loading) {
  translateBtn.disabled = loading;
  if (loading) {
    btnText.classList.add("hidden");
    btnSpinner.classList.remove("hidden");
  } else {
    btnText.classList.remove("hidden");
    btnSpinner.classList.add("hidden");
  }
}

// Show error message
function showError(message) {
  errorMessage.textContent = message;
  errorMessage.classList.remove("hidden");
}

// Hide error message
function hideError() {
  errorMessage.classList.add("hidden");
}

// Clear function
function clear() {
  englishInput.value = "";
  spanishOutput.value = "";
  hideError();
}

// Event listeners
translateBtn.addEventListener("click", translate);
clearBtn.addEventListener("click", clear);

// Allow Enter key to translate (Ctrl/Cmd + Enter)
englishInput.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    translate();
  }
});

// Check API health on load
async function checkHealth() {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      console.warn("API health check failed");
    }
  } catch (error) {
    console.warn("API health check error:", error);
  }
}

// Translation suggestions
const suggestions = [
  "Hello, how are you?",
  "The weather is nice today.",
  "I love programming and machine learning.",
  "What time is it?",
  "Can you help me with this?",
  "Thank you very much!",
  "Where is the nearest restaurant?",
  "I'm learning Spanish.",
  "Have a great day!",
  "How much does this cost?",
];

// Initialize suggestions
function initializeSuggestions() {
  const suggestionsGrid = document.getElementById("suggestions-grid");
  if (!suggestionsGrid) {
    console.error("Suggestions grid not found");
    return;
  }
  
  suggestions.forEach((suggestion) => {
    const chip = document.createElement("button");
    chip.className = "suggestion-chip";
    chip.textContent = suggestion;
    chip.type = "button";
    chip.addEventListener("click", () => {
      englishInput.value = suggestion;
      englishInput.focus();
      // Optionally auto-translate
      translate();
    });
    suggestionsGrid.appendChild(chip);
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    initializeSuggestions();
  });
} else {
  // DOM is already loaded
  checkHealth();
  initializeSuggestions();
}
