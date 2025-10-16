from extensions import socketio
from flask_socketio import emit, join_room, leave_room
from flask import request

rooms_users_video = {}  # Lưu user_id theo room cho video

# Khi user join camera
@socketio.on("join_camera")
def handle_join_camera(data):
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")

    join_room(meeting_code)

    if meeting_code not in rooms_users_video:
        rooms_users_video[meeting_code] = set()

    # Thêm user mới trước khi emit
    rooms_users_video[meeting_code].add(user_id)
    existing_users = [uid for uid in rooms_users_video[meeting_code] if uid != user_id]

    print(f"[Camera] Existing users in room {meeting_code}: {existing_users}")
    emit("existing_users_in_room_camera", {"user_ids": existing_users}, room=request.sid)

    emit("user_joined_camera", {"user_id": user_id}, room=meeting_code, include_self=False)
    print(f"[Camera] User {user_id} joined camera room {meeting_code}")

# Forward offer cho peer khác
@socketio.on("offer_camera")
def handle_offer_camera(data):
    meeting_code = data.get("meeting_code")
    emit("offer_camera", data, room=meeting_code, include_self=False)
    print(f"[Camera] Offer in room {meeting_code}")

# Forward answer cho peer khác
@socketio.on("answer_camera")
def handle_answer_camera(data):
    meeting_code = data.get("meeting_code")
    emit("answer_camera", data, room=meeting_code, include_self=False)
    print(f"[Camera] Answer in room {meeting_code}")

# Forward ICE candidate
@socketio.on("ice_candidate_camera")
def handle_ice_candidate_camera(data):
    meeting_code = data.get("meeting_code")
    emit("ice_candidate_camera", data, room=meeting_code, include_self=False)
    print(f"[Camera] ICE candidate in room {meeting_code}")

# Khi user leave camera
@socketio.on("leave_camera")
def handle_leave_camera(data):
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")
    leave_room(meeting_code)
    emit("user_left_camera", {"user_id": user_id}, room=meeting_code)
    print(f"[Camera] User {user_id} left camera room {meeting_code}")
