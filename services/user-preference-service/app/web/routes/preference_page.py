from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.utils.jwt_utils import decode_user_pref_token
from app.services.preference_update_service import update_user_preference


web_bp = Blueprint("web_bp", __name__)


@web_bp.route("/preferences", methods=["GET", "POST"])
def preference_page():
    token = request.args.get("token") or request.form.get("token")
    if not token:
        return "Missing token", 400

    try:
        payload = decode_user_pref_token(token)
        user_id = payload["sub"]
        client_id = payload["client_id"]
    except Exception:
        return "Invalid or expired token", 401

    if request.method == "POST":
        channels = request.form.getlist("channels")
        allowed_types = request.form.getlist("allowed_types")

        if not channels or not allowed_types:
            flash("All fields are required")
            return render_template("preference_form.html", token=token)

        result, status = update_user_preference(user_id, client_id, channels, allowed_types)
        flash("Preferences updated!" if status == 200 else result.get("error", "Update failed"))
        return render_template("preference_form.html", token=token)

    # GET
    return render_template("preference_form.html", token=token)
