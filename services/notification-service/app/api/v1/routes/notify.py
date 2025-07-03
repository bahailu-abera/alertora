from flask import Blueprint, request, jsonify
from app.services.notification_service import process_notification


notify_bp = Blueprint('notify', __name__)


@notify_bp.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    print("From notify route", data)
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    result, status_code = process_notification(data, token)
    return jsonify(result), status_code
