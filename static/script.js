/* ═══════════════════════════════════════
   MindEase — script.js
   Real AI responses via Claude API
   ═══════════════════════════════════════ */

const chatBox   = document.getElementById("chat-box");
const chatForm  = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const sendBtn   = document.getElementById("sendBtn");
const typingInd = document.getElementById("typingIndicator");
const chipArea  = document.getElementById("suggestionChips");

// ── Append a message bubble (XSS-safe) ──
function appendMessage(text, sender) {
    const row = document.createElement("div");
    row.className = `msg-row ${sender}`;

    const avatarEl = document.createElement("div");
    avatarEl.className = "msg-avatar";
    avatarEl.setAttribute("aria-hidden", "true");
    avatarEl.textContent = sender === "user" ? "👤" : "🧠";

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble";

    // Render line breaks but keep it XSS-safe
    text.split("\n").forEach((line, i, arr) => {
        bubble.appendChild(document.createTextNode(line));
        if (i < arr.length - 1) bubble.appendChild(document.createElement("br"));
    });

    row.appendChild(avatarEl);
    row.appendChild(bubble);
    chatBox.appendChild(row);
    scrollToBottom();
}

// ── Typing indicator ──
function showTyping() { typingInd.classList.add("active"); scrollToBottom(); }
function hideTyping()  { typingInd.classList.remove("active"); }

function scrollToBottom() { chatBox.scrollTop = chatBox.scrollHeight; }

function hideChips() { if (chipArea) chipArea.style.display = "none"; }

// ── Send message to Flask → Claude ──
async function sendMessage(text) {
    if (!text || !text.trim()) return;

    hideChips();
    appendMessage(text, "user");
    userInput.value = "";
    sendBtn.disabled = true;
    showTyping();

    try {
        const res = await fetch("/get_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
        });

        if (!res.ok) throw new Error("Server error");

        const data = await res.json();
        hideTyping();
        appendMessage(data.reply || "I'm here. Could you tell me more?", "bot");

    } catch (err) {
        hideTyping();
        appendMessage("I'm having trouble connecting right now. Please try again in a moment. 🙏", "bot");
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// ── New Chat ──
window.newChat = async function() {
    try {
        await fetch("/clear", { method: "POST" });
    } catch (_) {}
    chatBox.innerHTML = "";
    if (chipArea) chipArea.style.display = "flex";
    appendMessage(
        "Hello again! 👋 I've cleared our conversation. How are you feeling today?",
        "bot"
    );
};

// ── Chip suggestion ──
window.sendSuggestion = function(text) {
    userInput.value = text;
    sendMessage(text);
};

// ── Form submit ──
chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(userInput.value.trim());
});

// ── Disclaimer close ──
window.closeDisclaimer = function() {
    document.getElementById("disclaimerBar").classList.add("hidden");
    document.querySelector(".app-shell").style.paddingTop = "0";
};

// ── Welcome message ──
window.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        appendMessage(
            "Hello! 👋 I'm Dr. MindEase, your AI mental wellness companion.\n\n" +
            "I'm here to listen, support, and share information about mental health and wellbeing. " +
            "You can talk to me like you'd talk to a trusted friend.\n\n" +
            "How are you feeling today?",
            "bot"
        );
    }, 400);
});
