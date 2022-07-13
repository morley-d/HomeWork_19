"""Здесь бизнес-логика, в виде классов или методов."""

import calendar
import datetime

import jwt
from flask_restx import abort

from app.constants import JWT_SECRET, JWT_ALGO
from app.service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)
        if user is None:
            raise abort(404)
        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        # 30 minutes for access token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        # 130 days for refresh token
        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, ref_token):
        data = jwt.decode(ref_token, JWT_SECRET, algorithms=[JWT_ALGO])
        usernmae = data["username"]
        return self.generate_tokens(usernmae, None, is_refresh=True)
