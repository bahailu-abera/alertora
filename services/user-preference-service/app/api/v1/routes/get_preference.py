from flask import Blueprint, request, jsonify
from app.services.preference_query_service import get_user_preference
from app.utils.jwt_utils import decode_user_pref_token
from app.services.preference_metadata_service import (
    get_allowed_types_by_client_id
)


preference_get_bp = Blueprint("preference_get", __name__)


@preference_get_bp.route("/preferences", methods=["GET"])
def get_preference():
    user_id = request.args.get("user_id")
    client_id = request.args.get("client_id")

    if not user_id or not client_id:
        return jsonify({"error": "Missing user_id or client_id"}), 400

    result, status_code = get_user_preference(
        user_id=user_id, client_id=client_id
    )

    return jsonify(result), status_code


@preference_get_bp.route("/preferences/metadata", methods=["GET"])
def get_preference_metadata():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        payload = decode_user_pref_token(token)
        client_id = payload["client_id"]
    except Exception:
        return jsonify({"error": "Invalid or expired token"}), 401

    allowed_types = get_allowed_types_by_client_id(client_id)
    if allowed_types is None:
        return jsonify({"error": "Client not found"}), 404

    return jsonify({
        "allowed_types": allowed_types
    }), 200
