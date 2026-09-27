import os
import secrets

from dotenv import load_dotenv

# Load env FIRST before any other imports that need env vars
load_dotenv()

from flask import Flask, render_template, session
from config import Config
from database.db import db
from routes.chat_routes import chat_bp
from pypdf import PdfReader
from services.rag_service import collection_has_data, add_document
from flask_login import LoginManager, login_required
from database.models import User
from auth.auth_routes import auth_bp


# ---------------------------------------------------
# Flask App Setup
# ---------------------------------------------------

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "mysupersecretkey123")
app.config.from_object(Config)


# ---------------------------------------------------
# Initialize Database
# ---------------------------------------------------

db.init_app(app)

# ---------------------------------------------------
# Flask Login Setup
# ---------------------------------------------------

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------------------
# Register Blueprints
# ---------------------------------------------------

app.register_blueprint(chat_bp)
app.register_blueprint(auth_bp)


# ---------------------------------------------------
# Home Route
# ---------------------------------------------------

@app.route("/")
@login_required
def home():
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")


# ---------------------------------------------------
# Auto PDF Ingestion
# ---------------------------------------------------

if not collection_has_data():
    pdf_path = "mental_health_guide.pdf"
    if os.path.exists(pdf_path):
        print("Loading PDF knowledge base...")
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        chunks = text.split(".")
        for idx, chunk in enumerate(chunks):
            chunk = chunk.strip()
            if len(chunk) > 50:
                add_document(str(idx), chunk)
        print("PDF embeddings created successfully")


# ---------------------------------------------------
# Create Database
# ---------------------------------------------------

with app.app_context():
    db.create_all()


# ---------------------------------------------------
# Run App
# ---------------------------------------------------

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=True)
