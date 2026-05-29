from flask import Blueprint, request, render_template
from app.data.services.user_service import UserService

user_bp = Blueprint("users", __name__, template_folder="templates")


@user_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()

    try:
        user = UserService.create_user(
            name=data["name"]
        )

        return user.to_dict(), 201
    except Exception:
        return {}, 400


@user_bp.route("/delete", methods=["POST"])
def delete_user():
    data = request.get_json()

    try:
        UserService.delete_user(
            id=data["id"]
        )
        return {}, 201
    except Exception:
        return {}, 400


@user_bp.route("/register", methods=["GET"])
def register_user():
    return render_template("index.html")
