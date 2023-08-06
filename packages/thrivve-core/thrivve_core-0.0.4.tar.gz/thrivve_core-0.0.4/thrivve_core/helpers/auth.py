import json
import requests
from flask import request

from app.helpers.auth.enums import Language
from .exceptions import AppValidationError, AppMissingAuthError
from flask import session

from .. import ThrivveCore


class Auth:
    def __init__(self):
        pass

    @staticmethod
    def set_user(user):

        user["is_admin"] = user.get("role") == "Administrator"

        if request.headers.get("Accept-Language") in ("ar", "en"):
            user["language"] = request.headers.get("Accept-Language")
        else:
            user["language"] = user.get("language", "ar")

        app = ThrivveCore.get_app()
        app.logger.debug(user)
        session["user"] = user

    @staticmethod
    def get_user():
        default_user_str = 'Guest'
        try:
            user = session.get("user", dict())
        except Exception:
            user = dict(user_id=default_user_str, email=default_user_str)

        return user

    @staticmethod
    def get_user_str():
        # app = ThrivveCore.get_app()
        # with app.test_request_context():
        user = Auth.get_user()

        if user.get('role') == 'captain':
            return "{} : {} : {}".format(
                user.get("captain_id"),
                user.get("full_name"),
                user.get("mobile"),
            )
        else:
            return user.get('email')


def verify_user_token(token, allowed_permissions=None, pre_login=False):
    app = ThrivveCore.get_app()

    url = f"{app.config.get('AUTH_SERVICE')}/api/v1/authenticate?token={token}"
    try:
        language = (
            request.headers["Accept-Language"].lower()
            if (
                    "Accept-Language" in request.headers
                    and request.headers["Accept-Language"]
            )
            else Auth.get_user().get("language")
        )
    except Exception:
        language = Language.AR.value

    response = requests.request(
        "GET", url, headers={"Accept-Language": language}, data=dict()
    )

    if response.status_code != 200:
        raise AppValidationError("Invalid Token")

    try:
        response = json.loads(response.text)
    except Exception:
        raise AppValidationError("Error in parsing auth response")

    if not pre_login:
        if not response["data"].get("is_logged"):
            raise AppValidationError("Not Logged Token, please complete login process")

    response["data"].update(token=token)
    user = response["data"]

    Auth.set_user(user)
    return user
