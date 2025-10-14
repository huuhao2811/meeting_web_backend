from flask import Blueprint, request, jsonify
from extensions import db
from models import Message, Meeting

messages_bp = Blueprint("messages", __name__)

@messages_bp.route("/history/<meeting_code>", methods=["GET"])
def get_message_history(meeting_code):
    messages = Message.query.join(Meeting).filter(Meeting.meeting_code == meeting_code).order_by(Message.send_at.asc()).all()
    return jsonify([
        {
            "user_id": message.user_id,
            "username": message.user.username,
            "content": message.content,
            "send_at": message.send_at.isoformat()
        }
        for message in messages
    ])
