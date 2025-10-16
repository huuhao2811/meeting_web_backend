from extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request
rooms_users = {}  # Lưu user_id theo room

@socketio.on("join_voice")
def handle_join_voice(data):
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")

    join_room(meeting_code)

    if meeting_code not in rooms_users:
        rooms_users[meeting_code] = set()
    existing_users = list(rooms_users[meeting_code])
    rooms_users[meeting_code].add(user_id)
    emit("existing_users_in_room", {"user_ids": existing_users}, room=request.sid)

    emit("user_joined_voice", {"user_id": user_id}, room=meeting_code, include_self=False)

@socketio.on("offer")
def handle_offer(data):
    meeting_code = data.get("meeting_code")
    emit("offer", data, room=meeting_code, include_self=False)

@socketio.on("answer")
def handle_answer(data):
    meeting_code = data.get("meeting_code")
    emit("answer", data, room=meeting_code, include_self=False)

@socketio.on("ice_candidate")
def handle_ice_candidate(data):
    meeting_code = data.get("meeting_code")
    emit("ice_candidate", data, room=meeting_code, include_self=False)

@socketio.on("leave_voice")
def handle_leave_voice(data):
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")
    leave_room(meeting_code)
    emit("user_left_voice", {"user_id": user_id}, room=meeting_code)

