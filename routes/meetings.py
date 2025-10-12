# routes/meetings.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Meeting

meetings_bp = Blueprint("meetings", __name__)

# Lấy tất cả meetings
@meetings_bp.route("/", methods=["GET"])
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

# Tạo meeting mới
@meetings_bp.route("/", methods=["POST"])
def create_meeting():
    data = request.json
    new_meeting = Meeting(
        host_id=data.get("host_id"),
        title=data.get("title"),
        meeting_code=data.get("meeting_code"),
        status=data.get("status"),
        scheduled_at=data.get("scheduled_at")
    )
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify({"message": "Meeting created", "id": new_meeting.id})

# Lấy meeting theo id
@meetings_bp.route("/<int:meeting_id>", methods=["GET"])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return jsonify({
        "id": meeting.id,
        "title": meeting.title,
        "host_id": meeting.host_id,
        "meeting_code": meeting.meeting_code,
        "status": meeting.status,
        "scheduled_at": meeting.scheduled_at
    })
