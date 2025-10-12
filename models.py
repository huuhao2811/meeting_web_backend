from extensions import db
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = "user"   
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password = db.Column("password", db.String, nullable=False)
    avatar_url = db.Column(db.String)
    role = db.Column(db.String)  # bạn có thể dùng Enum nếu muốn
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meetings_hosted = db.relationship("Meeting", backref="host", lazy=True)
    messages = db.relationship("Message", backref="user", lazy=True)
    participants = db.relationship("MeetingParticipant", backref="user", lazy=True)
    verified = db.Column(db.Boolean, nullable=False, default=False) 

class Meeting(db.Model):
    __tablename__ = "meetings"
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String)
    meeting_code = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    status = db.Column(db.String)
    scheduled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    participants = db.relationship("MeetingParticipant", backref="meeting", lazy=True)
    messages = db.relationship("Message", backref="meeting", lazy=True)
    recordings = db.relationship("Recording", backref="meeting", lazy=True)

class MeetingParticipant(db.Model):
    __tablename__ = "meeting_participants"
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    joined_at = db.Column(db.DateTime)
    left_at = db.Column(db.DateTime)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    content = db.Column(db.Text)
    send_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recording(db.Model):
    __tablename__ = "recordings"
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable=False)
    file_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserOTP(db.Model):
    __tablename__ = "user_otps"

    otp_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    otp_expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=10))
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("otps", lazy=True))