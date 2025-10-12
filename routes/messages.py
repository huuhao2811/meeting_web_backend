# routes/messages.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Message

messages_bp = Blueprint("messages", __name__)

# Lấy tất cả messages
@messages_bp.route("/", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    result = []
    for m in messages:
        result.append({
            "id": m.id,
            "meeting_id": m.meeting_id,
            "user_id": m.user_id,
            "content": m.content,
            "send_at": m.send_at
        })
    return jsonify(result)

# Tạo message mới
@messages_bp.route("/", methods=["POST"])
def create_message():
    data = request.json
    new_msg = Message(
        meeting_id=data.get("meeting_id"),
        user_id=data.get("user_id"),
        content=data.get("content")
    )
    db.session.add(new_msg)
    db.session.commit()
    return jsonify({"message": "Message sent", "id": new_msg.id})

# Lấy message theo id
@messages_bp.route("/<int:msg_id>", methods=["GET"])
def get_message(msg_id):
    msg = Message.query.get_or_404(msg_id)
    return jsonify({
        "id": msg.id,
        "meeting_id": msg.meeting_id,
        "user_id": msg.user_id,
        "content": msg.content,
        "send_at": msg.send_at
    })
