from extensions import socketio
from flask_socketio import join_room, leave_room, emit

@socketio.on("join_room")
def handle_join_room(data):
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")
    username = data.get("username")

    join_room(meeting_code)
    emit("participant_joined", {
        "meeting_code": meeting_code,
        "user_id": user_id,
        "username": username,
    }, room=meeting_code, include_self=False)

@socketio.on("leave_room")
def handle_leave_room(data):
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")

    leave_room(meeting_code)
    emit("participant_left", {
        "meeting_code": meeting_code,
        "user_id": user_id,
        "username": data.get("username"),
    }, room=meeting_code, include_self=False)
