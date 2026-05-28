from flask import Blueprint, request
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("/create_users", methods=["POST"])
def create_user():
    data = request.get_json()

    try:
        user = UserService.create_user(
            name=data["name"]
        )

        return user.to_dict(), 201
    except Exception:
        return {}, 400


@user_bp.route("/delete_users", methods=["POST"])
def delete_user():
    data = request.get_json()

    try:
        UserService.delete_user(
            id=data["id"]
        )
        return {}, 201
    except Exception:
        return {}, 400
