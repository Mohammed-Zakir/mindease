from database.db import db

from flask_login import UserMixin

from datetime import datetime


# ---------------------------------------------------
# User Model
# ---------------------------------------------------

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    chats = db.relationship(
        "ChatHistory",
        backref="user",
        lazy=True
    )

    moods = db.relationship(
        "MoodLog",
        backref="user",
        lazy=True
    )


# ---------------------------------------------------
# Chat History Model
# ---------------------------------------------------

class ChatHistory(db.Model):

    __tablename__ = "chat_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    ai_response = db.Column(
        db.Text,
        nullable=False
    )

    sentiment = db.Column(
        db.String(50)
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ---------------------------------------------------
# Mood Log Model
# ---------------------------------------------------

class MoodLog(db.Model):

    __tablename__ = "mood_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    mood = db.Column(
        db.String(50)
    )

    score = db.Column(
        db.Integer
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )