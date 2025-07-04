from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.utils.jwt_utils import decode_user_pref_token
from app.services.preference_update_service import update_user_preference
from app.extensions import mongo_database
from app.utils.constants import VALID_CHANNELS


web_bp = Blueprint("web_bp", __name__)


@web_bp.route("/preferences", methods=["GET", "POST"])
def preference_page():
    token = request.args.get("token") or request.form.get("token")
    if not token:
        flash("Missing token")
        return render_template("preference_form.html", token=None, channels=[], types=[])

    try:
        payload = decode_user_pref_token(token)
        user_id = payload["sub"]
        client_id = payload["client_id"]
    except Exception:
        flash("Invalid or expired token")
        return render_template("preference_form.html", token=None, channels=[], types=[])

    client_doc = mongo_database.clients.find_one({"client_id": client_id})
    if not client_doc:
        flash("Client not found")
        return render_template("preference_form.html", token=token, channels=[], types=[])

    allowed_types = [t["name"] for t in client_doc.get("notification_types", [])]

    if request.method == "POST":
        selected_channels = request.form.getlist("channels")
        selected_types = request.form.getlist("allowed_types")

        if not selected_channels or not selected_types:
            flash("All fields are required")
        else:
            result, status = update_user_preference(user_id, client_id, selected_channels, selected_types)
            flash("Preferences updated!" if status == 200 else result.get("error", "Update failed"))

        return render_template(
            "preference_form.html",
            token=token,
            channels=VALID_CHANNELS,
            types=allowed_types
        )

    return render_template(
        "preference_form.html",
        token=token,
        channels=VALID_CHANNELS,
        types=allowed_types
    )
