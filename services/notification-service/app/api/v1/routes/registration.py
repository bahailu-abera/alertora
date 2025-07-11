from flask import Blueprint, request, jsonify
from app.services.registration_service import register_client


registration_bp = Blueprint("registration", __name__)


@registration_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    result = register_client(data)
    return jsonify(result), 201
