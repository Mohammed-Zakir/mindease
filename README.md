# 🧠 MindEase — AI Mental Health Companion

> A compassionate AI chatbot powered by **Claude (Anthropic)** that provides real mental wellness conversations, emotional support, and health information. Not keyword-based — actual AI that understands you.

---

## ✨ Features

- **Real AI Conversations** — Powered by Claude claude-3-5-haiku, not hardcoded responses
- **Conversation Memory** — Remembers what you said earlier in the session
- **Crisis Detection** — AI is trained to detect distress and provide emergency helplines
- **New Chat Button** — Reset the session anytime
- **Medical Disclaimers** — Clear, visible throughout the UI
- **Mobile Responsive** — Works on all screen sizes
- **XSS-Safe** — All DOM manipulation uses textContent, never innerHTML injection
- **Session-based History** — No data stored to disk or database

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- An Anthropic API key → get one free at [console.anthropic.com](https://console.anthropic.com)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/mindease.git
cd mindease

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Open .env and paste your Anthropic API key

# 5. Run
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 🔑 Getting Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Click **API Keys** → **Create Key**
4. Copy it into your `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

> **Free tier available** — Anthropic gives new accounts free credits to start.

---

## 📁 Project Structure

```
mindease/
├── app.py                  # Flask backend — Claude API integration, session history
├── requirements.txt        # Python dependencies (flask, requests)
├── .env.example            # Environment variable template
├── .gitignore              # Keeps secrets and venv out of git
├── README.md
├── templates/
│   └── index.html          # Jinja2 HTML template
└── static/
    ├── style.css           # Full responsive styling
    ├── script.js           # Frontend — AI response handler, XSS-safe DOM
    └── favicon.svg
```

---

## 🛠️ Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3, Flask                     |
| AI Model  | Claude claude-3-5-haiku (Anthropic API)    |
| HTTP      | requests library                    |
| Frontend  | Vanilla HTML5, CSS3, JavaScript     |
| Fonts     | Google Fonts — DM Serif + DM Sans   |
| Sessions  | Flask server-side sessions          |

---

## ⚕️ Medical Disclaimer

> **MindEase is not a medical application.** It provides general wellness information for educational purposes only. It does **not** diagnose, treat, or replace professional medical advice. Always consult a licensed healthcare professional.

**Crisis Resources:**
- 🇮🇳 iCall (India): **9152987821**
- 🌐 Vandrevala Foundation: **1860-2662-345** (24/7)
- 🌍 iSafetyline: [isafeline.org](https://www.isafeline.org)

---

## 🔒 Security

- No `innerHTML` injection — all DOM uses `textContent` / `createElement`
- API key stored in `.env` (never committed to git)
- `debug=True` controlled via environment variable only
- Session history stored server-side only, cleared on new chat

---

## 🗺️ Future Improvements

- [ ] Persistent chat history with SQLite
- [ ] Mood tracker with charts
- [ ] Multilingual support (Hindi, Telugu)
- [ ] Deploy to Render / Railway
- [ ] Voice input support

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [your-linkedin](https://linkedin.com/in/yourprofile)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
