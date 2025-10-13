# routes/meetings.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Meeting
import uuid
from datetime import datetime
meetings_bp = Blueprint("meetings", __name__)

@meetings_bp.route("", methods=["GET"])
def get_meetings():
    meetings = Meeting.query.all()
    result = []
    for m in meetings:
        result.append({
            "id": m.id,
            "title": m.title,
            "host_id": m.host_id,
            "meeting_code": m.meeting_code,
            "status": m.status,
            "scheduled_at": m.scheduled_at,
        })
    return jsonify(result)

@meetings_bp.route("", methods=["POST"])
def create_meeting():
    data = request.json
    meeting_code = str(uuid.uuid4())[:8]
    print(data)
    print(meeting_code)
    if not data.get("host_id"):
        return jsonify({"error": "Missing host_id or meeting_code"}), 400

    if Meeting.query.filter_by(meeting_code=meeting_code).first():
        return jsonify({"error": "Meeting code already exists"}), 400
    new_meeting = Meeting(
        host_id=data.get("host_id"),
        title=data.get("title"),
        meeting_code=meeting_code,
        status=data.get("status", "scheduled"),
        scheduled_at=data.get("scheduled_at"),
        created_at=datetime.utcnow()
    )
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify({
        "message": "Meeting created",
        "meeting": {
            "id": new_meeting.id,
            "title": new_meeting.title,
            "meeting_code": new_meeting.meeting_code,
            "status": new_meeting.status,
        }
    }), 201

@meetings_bp.route("/<int:meeting_id>", methods=["GET"])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return jsonify({
        "id": meeting.id,
        "title": meeting.title,
        "host_id": meeting.host_id,
        "meeting_code": meeting.meeting_code,
        "status": meeting.status,
        "scheduled_at": meeting.scheduled_at,
        "created_at": meeting.created_at,
    })

@meetings_bp.route("/code/<string:meeting_code>", methods=["GET"])
def get_meeting_by_code(meeting_code):
    meeting = Meeting.query.filter_by(meeting_code=meeting_code).first_or_404()
    return jsonify({
        "id": meeting.id,
        "title": meeting.title,
        "host_id": meeting.host_id,
        "meeting_code": meeting.meeting_code,
        "status": meeting.status,
        "scheduled_at": meeting.scheduled_at
    })

