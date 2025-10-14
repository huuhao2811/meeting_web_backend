from flask import Blueprint, request, jsonify
from extensions import db
from models import Meeting, MeetingParticipant, User
from datetime import datetime
participants_bp = Blueprint("participants", __name__)

@participants_bp.route("/join", methods=["POST"])
def join_meeting():
    data = request.json
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Please login"}), 400
    meeting = Meeting.query.filter_by(meeting_code=meeting_code).first()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    if meeting.status != "ongoing":
        return jsonify({"error": "Meeting is not ongoing"}), 400
    participant = MeetingParticipant.query.filter_by(
        meeting_id=meeting.id, user_id=user_id, left_at=None
    ).first()
    if participant:
        return jsonify({"message": "You already joined", "participant_id": participant.id}), 200
    new_participant = MeetingParticipant(
        meeting_id=meeting.id,
        user_id=user_id,
        joined_at=datetime.utcnow(),
        left_at=None
    )
    db.session.add(new_participant)
    db.session.commit()
    return jsonify({
        "message": "User joined meeting",
        "participant": {
            "id": new_participant.id,
            "joined_at": new_participant.joined_at,
            "meeting_id": new_participant.meeting_id,
            "user_id": new_participant.user_id
        }
    }), 201

@participants_bp.route("/leave", methods=["POST"])
def leave_meeting():
    data = request.json
    meeting_code = data.get("meeting_code")
    user_id = data.get("user_id")

    if not meeting_code or not user_id:
        return jsonify({"error": "Missing meeting_code or user_id"}), 400

    # Lấy meeting_id từ meeting_code
    meeting = Meeting.query.filter_by(meeting_code=meeting_code).first()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    # Tìm participant chưa rời
    participant = MeetingParticipant.query.filter_by(
        meeting_id=meeting.id,
        user_id=user_id,
        left_at=None
    ).first()

    if not participant:
        return jsonify({"error": "You are not in this meeting"}), 400

    # Cập nhật thời điểm rời
    participant.left_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "message": "You have left the meeting",
        "participant_id": participant.id,
        "left_at": participant.left_at
    }), 200


@participants_bp.route("/<meeting_code>", methods=["GET"])
def get_participants(meeting_code: str):
    participants = (
        db.session.query(MeetingParticipant, User)
        .join(User, User.user_id == MeetingParticipant.user_id)
        .join(Meeting, Meeting.id == MeetingParticipant.meeting_id) 
        .filter(
            Meeting.meeting_code == meeting_code,
            MeetingParticipant.left_at == None
        )
        .all()
    )

    result = []
    for mp, user in participants:
        result.append({
            "participant_id": mp.id,
            "meeting_id": mp.meeting_id,
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "joined_at": mp.joined_at
        })
    return jsonify(result), 200