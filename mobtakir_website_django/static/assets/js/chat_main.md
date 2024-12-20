```js
/*
getting the api url from an optional text field for it or from a hidden input 
*/
var API_BASE_URL = "";

let chatHistory = [];

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

document.addEventListener("DOMContentLoaded", function () {
  const fileUpload = document.getElementById("file-upload");
  const chatInput = document.getElementById("chat-input");
  const sendButton = document.getElementById("send-button");
  const clearButton = document.getElementById("clear-button");
  const statusText = document.getElementById("status-text");

  fileUpload.addEventListener("change", handleFileUpload);
  sendButton.addEventListener("click", handleChat);
  clearButton.addEventListener("click", clearChat);
});

async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    updateStatus("Uploading document...");
    const response = await fetch(`${API_BASE_URL}/api/document/upload`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Upload failed");

    document.getElementById(
      "context-info"
    ).innerHTML = `<b>Context ID:</b> ${result.context_id}`;

    const successHtml = `
            <div class="success-message">
                <h4 style="color: #4CAF50; margin: 0 0 10px 0;">✓ Document Upload Successful</h4>
                <p><strong>Filename:</strong> ${file.name}</p>
                <p><strong>Context ID:</strong> ${result.context_id}</p>
                <p><strong>Type:</strong> ${result.metadata.type}</p>
                <p><strong>Size:</strong> ${result.metadata.size} bytes</p>
                <div style="margin-top: 10px;">
                    <strong>Content Preview:</strong>
                    <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-top: 5px;">${
                      result.content.length > 500
                        ? result.content.substring(0, 500) + "..."
                        : result.content
                    }</pre>
                </div>
            </div>
        `;
    document.getElementById("system-output").innerHTML = successHtml;
    updateStatus("Ready");
  } catch (error) {
    document.getElementById("system-output").innerHTML = `
            <div class="error-message">
                <h4 style="color: #f44336; margin: 0 0 10px 0;">✗ Upload Error</h4>
                <p>${error.message}</p>
            </div>
        `;
    updateStatus("Error occurred");
  }

  event.target.value = "";
}

function addCopyButtons() {
  document.querySelectorAll("pre code").forEach((codeBlock) => {
    const container = codeBlock.parentElement;
    const header = document.createElement("div");
    header.className = "code-block-header";

    const copyButton = document.createElement("button");
    copyButton.className = "copy-button";
    copyButton.textContent = "Copy";

    header.appendChild(copyButton);
    container.insertBefore(header, codeBlock);

    copyButton.addEventListener("click", async () => {
      try {
        // Try using navigator.clipboard first
        await navigator.clipboard.writeText(codeBlock.textContent);
        copyButton.textContent = "Copied!";
        copyButton.classList.add("copied");
      } catch (err) {
        // Fallback to textarea method
        const textarea = document.createElement("textarea");
        textarea.value = codeBlock.textContent;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand("copy");
          copyButton.textContent = "Copied!";
          copyButton.classList.add("copied");
        } catch (err) {
          copyButton.textContent = "Failed to copy";
        }
        document.body.removeChild(textarea);
      }

      // Reset button after 2 seconds
      setTimeout(() => {
        copyButton.textContent = "Copy";
        copyButton.classList.remove("copied");
      }, 2000);
    });
  });
}

async function handleChat() {
  API_BASE_URL =
    document.getElementById("api-url")?.value ||
    document.getElementById("api-url-hidden")?.value;

  console.log("API Base URL: " + API_BASE_URL);
  const chatInput = document.getElementById("chat-input");
  const message = chatInput.value.trim();
  if (!message) return;

  try {
    updateStatus("Processing...");

    const contextId = document
      .getElementById("context-info")
      .innerText.includes("None")
      ? null
      : document
          .getElementById("context-info")
          .innerText.split("Context ID: ")[1];

    chatHistory.push({ role: "user", content: message });

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: chatHistory,
        context_id: contextId,
      }),
    });

    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Chat failed");

    chatHistory.push({ role: "assistant", content: result.response });
    updateChatDisplay();

    chatInput.value = "";
    updateStatus("Ready");
  } catch (error) {
    document.getElementById("chat-output").innerHTML += `
            <div class="error-message">Error: ${error.message}</div>
        `;
    updateStatus("Error occurred");
  }
}

async function clearChat() {
  try {
    const contextId = document
      .getElementById("context-info")
      .innerText.includes("None")
      ? null
      : document
          .getElementById("context-info")
          .innerText.split("Context ID: ")[1];

    if (contextId) {
      const response = await fetch(`${API_BASE_URL}/api/clear/${contextId}`, {
        method: "POST",
      });
      const result = await response.json();

      if (!response.ok) throw new Error(result.message || "Clear failed");
    }

    chatHistory = [];
    document.getElementById("chat-output").innerHTML = "";
    document.getElementById("context-info").innerHTML =
      "<b>Context ID:</b> None";
    document.getElementById("chat-output").innerHTML = "Chat history cleared.";
  } catch (error) {
    document.getElementById("chat-output").innerHTML += `
            <div class="error-message">Error clearing chat: ${error.message}</div>
        `;
  }
}

function addCopyButtons() {
  document.querySelectorAll("pre code").forEach((codeBlock) => {
    const container = codeBlock.parentElement;
    const header = document.createElement("div");
    header.className = "code-block-header";

    const copyButton = document.createElement("button");
    copyButton.className = "copy-button";
    copyButton.textContent = "Copy";

    header.appendChild(copyButton);
    container.insertBefore(header, codeBlock);

    copyButton.addEventListener("click", async () => {
      try {
        // Try using navigator.clipboard first
        await navigator.clipboard.writeText(codeBlock.textContent);
        copyButton.textContent = "Copied!";
        copyButton.classList.add("copied");
      } catch (err) {
        // Fallback to textarea method
        const textarea = document.createElement("textarea");
        textarea.value = codeBlock.textContent;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand("copy");
          copyButton.textContent = "Copied!";
          copyButton.classList.add("copied");
        } catch (err) {
          copyButton.textContent = "Failed to copy";
        }
        document.body.removeChild(textarea);
      }

      // Reset button after 2 seconds
      setTimeout(() => {
        copyButton.textContent = "Copy";
        copyButton.classList.remove("copied");
      }, 2000);
    });
  });
}

function updateChatDisplay() {
  const chatOutput = document.getElementById("chat-output");
  chatOutput.innerHTML = "";

  chatHistory.forEach((msg) => {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${msg.role}-message`;

    let content;
    if (msg.role === "assistant") {
      try {
        content = marked.parse(msg.content);
      } catch (e) {
        content = msg.content;
        console.error("Markdown parsing error:", e);
      }
    } else {
      content = msg.content;
    }

    messageDiv.innerHTML = `
            <div class="message-header">${
              msg.role === "user" ? "You" : "Assistant"
            }:</div>
            <div class="message-content">${content}</div>
        `;
    chatOutput.appendChild(messageDiv);

    // Apply syntax highlighting to code blocks
    messageDiv.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightBlock(block);
    });
  });
  // After the hljs.highlightBlock line:
  addCopyButtons();

  chatOutput.scrollTop = chatOutput.scrollHeight;
}

function updateStatus(text) {
  document.getElementById("status-text").textContent = text;
}
```
