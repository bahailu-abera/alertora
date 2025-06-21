from flask import Blueprint, request, jsonify
from app.services.notification_service import process_notification


notify_bp = Blueprint('notify', __name__)


@notify_bp.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    result = process_notification(data, token)
    return jsonify(result), result.get("status_code", 200)
