from flask import Blueprint, request, jsonify
from extensions import db
from models import MeetingParticipant

participants_bp = Blueprint("participants", __name__)

@participants_bp.route("/", methods=["GET"])
def get_participants():
    participants = MeetingParticipant.query.all()
    result = []
    for p in participants:
        result.append({
            "id": p.id,
            "meeting_id": p.meeting_id,
            "user_id": p.user_id,
            "joined_at": p.joined_at,
            "left_at": p.left_at
        })
    return jsonify(result)

@participants_bp.route("/", methods=["POST"])
def add_participant():
    data = request.json
    new_p = MeetingParticipant(
        meeting_id=data.get("meeting_id"),
        user_id=data.get("user_id"),
        joined_at=data.get("joined_at"),
        left_at=data.get("left_at")
    )
    db.session.add(new_p)
    db.session.commit()
    return jsonify({"message": "Participant added", "id": new_p.id})

@participants_bp.route("/<int:p_id>", methods=["GET"])
def get_participant(p_id):
    p = MeetingParticipant.query.get_or_404(p_id)
    return jsonify({
        "id": p.id,
        "meeting_id": p.meeting_id,
        "user_id": p.user_id,
        "joined_at": p.joined_at,
        "left_at": p.left_at
    })
