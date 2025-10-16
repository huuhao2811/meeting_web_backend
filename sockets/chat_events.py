from flask_socketio import emit
from extensions import socketio, db
from models import Message
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

@socketio.on("send_message")
def handle_send_message(data):
    try:
        meeting_id = data.get("meeting_id")
        meeting_code = data.get("meeting_code")
        user_id = data.get("user_id")
        content = data.get("message")
        username = data.get("username")

        new_message = Message(
            meeting_id=meeting_id,
            user_id=user_id,
            content=content,
            send_at=datetime.utcnow(),
        )
        db.session.add(new_message)
        db.session.commit()

        emit("receive_message", {
            "id": new_message.id,
            "user_id": user_id,
            "username": username,
            "content": content,
            "send_at": new_message.send_at.replace(microsecond=0).isoformat() + "Z"  
        }, room=meeting_code)

    except SQLAlchemyError as e:
        db.session.rollback()
        emit("error", {"message": "Failed to send message."})
        print(f"[Error] send_message: {str(e)}")

@socketio.on("load_messages")
def handle_load_messages(data):
    meeting_id = data.get("meeting_id")
    messages = Message.query.filter_by(meeting_id=meeting_id).order_by(Message.send_at).all()
    message_list = [
        {
            "id": m.id,
            "user_id": m.user_id,
            "username": m.user.username if m.user else "Unknown",
            "content": m.content,
            "send_at": m.send_at.isoformat() + "Z"  
        }
        for m in messages
    ]
    emit("load_messages_response", message_list)