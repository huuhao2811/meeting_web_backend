from flask import Blueprint, request, jsonify
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, UserOTP
from datetime import datetime, timedelta
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config

users_bp = Blueprint("users", __name__)


def generate_otp():
    return f"{random.randint(100000, 999999)}"

def send_otp_email(to_email, otp_code):
    """Gửi em   ail OTP bằng SendGrid"""
    message = Mail(
        from_email=Config.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject="Verify Your Email",
        html_content=f"<strong>Your OTP code is: {otp_code}</strong><br>This code expires in 5 minutes."
    )
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        print("SendGrid response:", response.status_code)
        return True
    except Exception as e:
        print("SendGrid error:", str(e))
        raise e

@users_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp_code = data.get("otp_code")

    if not email or not otp_code:
        return jsonify({"error": "Missing email or OTP code"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    otp_entry = UserOTP.query.filter_by(
        user_id=user.user_id, 
        otp_code=otp_code, 
        is_used=False
    ).first()

    if not otp_entry:
        return jsonify({"error": "Invalid OTP"}), 400

    if otp_entry.otp_expires_at < datetime.utcnow():
        return jsonify({"error": "OTP has expired"}), 400

    user.verified = True
    otp_entry.is_used = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully!"}), 200

@users_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(
        username=username,
        email=email,
        _password=generate_password_hash(password),
        verified=False,
        role="user"
    )
    db.session.add(new_user)
    db.session.commit()

    # Sinh OTP và lưu
    otp_code = generate_otp()
    otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
    user_otp = UserOTP(
        user_id=new_user.user_id,
        otp_code=otp_code,
        otp_expires_at=otp_expires_at,
        is_used=False
    )
    db.session.add(user_otp)
    db.session.commit()

    # Gửi OTP email
    try:
        send_otp_email(email, otp_code)
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP email: {str(e)}"}), 500

    return jsonify({
        "message": "User created successfully. OTP sent to your email.",
        "user_id": new_user.user_id
    }), 201


@users_bp.route("/signin", methods=["POST"])
def signin():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user._password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.verified:
        return jsonify({"error": "Email not verified. Please verify your email first."}), 403

    access_token = create_access_token(identity=str(user.user_id))

    return jsonify({"access_token": access_token, "user": {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }}), 200


# ---------- PROTECTED ROUTE ----------
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "role": user.role
    })

