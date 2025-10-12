# routes/recordings.py
from flask import Blueprint, request, jsonify
from extensions import db
from models import Recording
from datetime import datetime

recordings_bp = Blueprint("recordings", __name__)

# Lấy tất cả recordings
@recordings_bp.route("/", methods=["GET"])
def get_recordings():
    recs = Recording.query.all()
    result = []
    for r in recs:
        result.append({
            "id": r.id,
            "meeting_id": r.meeting_id,
            "file_url": r.file_url,
            "created_at": r.created_at
        })
    return jsonify(result)

# Thêm recording
@recordings_bp.route("/", methods=["POST"])
def add_recording():
    data = request.json
    new_r = Recording(
        meeting_id=data.get("meeting_id"),
        file_url=data.get("file_url"),
        created_at=data.get("created_at") or datetime.utcnow()
    )
    db.session.add(new_r)
    db.session.commit()
    return jsonify({"message": "Recording added", "id": new_r.id})

# Lấy recording theo id
@recordings_bp.route("/<int:r_id>", methods=["GET"])
def get_recording(r_id):
    r = Recording.query.get_or_404(r_id)
    return jsonify({
        "id": r.id,
        "meeting_id": r.meeting_id,
        "file_url": r.file_url,
        "created_at": r.created_at
    })
