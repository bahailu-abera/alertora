from flask import Blueprint, request, jsonify
from app.services.preference_update_service import update_user_preference


preference_update_bp = Blueprint("preference_update", __name__)


@preference_update_bp.route("/preferences", methods=["POST"])
def update_preference():
    data = request.get_json()
    user_id = data.get("user_id")
    client_id = data.get("client_id")
    channels = data.get("channels")
    allowed_types = data.get("allowed_types")

    if not user_id or not client_id or not channels or not allowed_types:
        return jsonify({"error": "Missing fields"}), 400

    result, status_code = update_user_preference(
        user_id, client_id, channels, allowed_types
    )
    return jsonify(result), status_code
