from flask import request
from flask_restx import Namespace, Resource

from app.implemented import auth_service

auth_ns = Namespace("auth")


"""Роуты для авторизации"""
@auth_ns.route('/')
class AuthsView(Resource):
    def post(self):
        """Авторизация по имени и паролю"""
        data = request.json
        username = data.get("username", None)
        password = data.get("password", None)
        if None in [username, password]:
            return "Не задано имя или пароль", 401
        tokens = auth_service.generate_tokens(username, password)
        return tokens, 201

    def put(self):
        """Авторизация по refresh_token"""
        data = request.json
        ref_token = data.get("refresh_token")
        if not ref_token:
            return "Не задан токен", 401
        tokens = auth_service.approve_refresh_token(ref_token)
        return tokens, 201
