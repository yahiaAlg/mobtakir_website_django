const apiKey = "AIzaSyC-Aj1TmsnXKVlZJth-yL0s6tjLbPAt5D4";
const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${apiKey}`;

const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

// Configure marked options immediately since scripts are already loaded
marked.setOptions({
  highlight: function (code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  },
  breaks: true,
  gfm: true,
});

// Function to create and attach "Copy" buttons to code blocks
function addCopyButtons() {
  const codeBlocks = document.querySelectorAll(".markdown-content pre");

  codeBlocks.forEach((block) => {
    // Create the "Copy" button
    const copyButton = document.createElement("button");
    copyButton.textContent = "Copy";
    copyButton.className = "copy-button";

    // Add styling to the button
    copyButton.style.position = "absolute";
    copyButton.style.top = "10px";
    copyButton.style.right = "10px";
    copyButton.style.padding = "5px 10px";
    copyButton.style.fontSize = "12px";
    copyButton.style.border = "none";
    copyButton.style.borderRadius = "5px";
    copyButton.style.cursor = "pointer";
    copyButton.style.backgroundColor = "var(--primary-color)";
    copyButton.style.color = "#fff";

    // Create a container to wrap the block and button
    const wrapper = document.createElement("div");
    wrapper.style.position = "relative";

    // Append the original block to the wrapper
    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(block);
    wrapper.appendChild(copyButton);

    // Add event listener to copy button
    copyButton.addEventListener("click", () => {
      const code = block.innerText;

      // Copy the code to the clipboard
      navigator.clipboard
        .writeText(code)
        .then(() => {
          copyButton.textContent = "Copied!";

          // Revert the button text after 2 seconds
          setTimeout(() => {
            copyButton.textContent = "Copy";
          }, 2000);
        })
        .catch((err) => {
          console.error("Failed to copy: ", err);
        });
    });
  });
}

// Configure marked options
function configureMarked() {
  marked.setOptions({
    highlight: function (code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return hljs.highlightAuto(code).value;
    },
    breaks: true,
    gfm: true,
  });
}

// Wait for marked and hljs to load
function waitForDependencies() {
  return new Promise((resolve) => {
    const check = () => {
      if (window.marked && window.hljs) {
        configureMarked();
        resolve();
      } else {
        setTimeout(check, 100);
      }
    };
    check();
  });
}

let conversationHistory = [];

function createMessageBubble(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;
  const timeInnerDiv = document.createElement("div");
  timeInnerDiv.className = "message-time";
  const timeSpan = document.createElement("date");
  timeSpan.textContent = Date.now().toLocaleString();
  timeInnerDiv.appendChild(timeSpan);
  const bubble = document.createElement("div");
  bubble.className = "bubble markdown-content";

  // Parse markdown and render HTML directly
  bubble.innerHTML = marked.parse(text);
  // Apply syntax highlighting to code blocks
  bubble.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
  });

  messageDiv.appendChild(bubble);
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addToHistory(role, text) {
  conversationHistory.push({
    role: role,
    text: text,
  });

  const maxHistoryLength = 10;
  if (conversationHistory.length > maxHistoryLength) {
    conversationHistory = conversationHistory.slice(-maxHistoryLength);
  }
}

function formatHistoryForAPI() {
  const contents = [
    {
      role: "user",
      parts: [
        {
          text: conversationHistory
            .map((msg) => {
              const rolePrefix = msg.role === "user" ? "User: " : "Assistant: ";
              return `${rolePrefix}${msg.text}`;
            })
            .join("\n"),
        },
      ],
    },
  ];

  return contents;
}
function addWaitingDots() {
  let lastMessageElement = document.querySelector(".user-message:last-child");
  let waitingDots = document.createElement("div");
  const typingIndicator = lastMessageElement.insertAdjacentElement(
    "afterend",
    waitingDots
  );
  typingIndicator.classList.add("typing-indicator");
  typingIndicator.innerHTML = `
      <div class="typing-dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
  `;
}
function removeWaitingDots() {
  let typingIndicator = document.querySelector(".typing-indicator:last-child");
  typingIndicator.remove();
}
function handleMessage() {
  const userMessage = userInput.value.trim();
  if (!userMessage) return;

  createMessageBubble(userMessage, "user");
  console.log("created user message");
  addToHistory("user", userMessage);
  userInput.value = "";

  const data = {
    contents: formatHistoryForAPI(),
  };
  addWaitingDots();
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((result) => {
      const botMessage =
        result?.candidates?.[0]?.content?.parts?.[0]?.text ||
        "Sorry, I couldn't process that.";
      removeWaitingDots();
      createMessageBubble(botMessage, "bot");
      addToHistory("assistant", botMessage);
      addCopyButtons();
      if (!document.getElementById("clear-history")) {
        addClearHistoryButton();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      const errorMessage = "Oops! Something went wrong. Please try again.";
      createMessageBubble(errorMessage, "bot");
      addToHistory("assistant", errorMessage);
    });
}

function addClearHistoryButton() {
  const clearButton = document.createElement("button");
  clearButton.id = "clear-history";
  clearButton.textContent = "Clear Chat History";
  clearButton.className = "clear-history-btn";
  clearButton.addEventListener("click", clearHistory);

  // Add button above the chat messages
  chatMessages.parentElement.insertBefore(clearButton, chatMessages);

  // Add CSS for the button
  const style = document.createElement("style");
  style.textContent = `
    .clear-history-btn {
      margin: 10px;
      padding: 8px 16px;
      background-color: #ff4444;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s;
    }
    .clear-history-btn:hover {
      background-color: #cc0000;
    }
  `;
  document.head.appendChild(style);
}

function clearHistory() {
  conversationHistory = [];
  chatMessages.innerHTML = "";
  if (document.getElementById("clear-history")) {
    document.getElementById("clear-history").remove();
  }
}

sendButton.addEventListener("click", handleMessage);

userInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault(); // Prevents adding a new line
    handleMessage();
  } else if (event.key === "Enter" && event.shiftKey) {
    // Allows new line in the textarea
    event.preventDefault();
    const cursorPos = userInput.selectionStart;
    const text = userInput.value;
    userInput.value = text.slice(0, cursorPos) + "\n" + text.slice(cursorPos);
    userInput.selectionEnd = cursorPos + 1; // Move cursor after the newline
  }
});
