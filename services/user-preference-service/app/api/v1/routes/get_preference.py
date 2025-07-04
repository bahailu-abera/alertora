from flask import Blueprint, request, jsonify
from app.services.preference_query_service import get_user_preference


preference_get_bp = Blueprint('preference_get', __name__)


@preference_get_bp.route('/preferences', methods=['GET'])
def get_preference():
    user_id = request.args.get('user_id')
    client_id = request.args.get('client_id')

    if not user_id or not client_id:
        return jsonify({"error": "Missing user_id or client_id"}), 400

    result, status_code = get_user_preference(user_id=user_id, client_id=client_id)

    return jsonify(result), status_code
