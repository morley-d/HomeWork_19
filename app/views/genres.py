from flask import request, make_response
from flask_restx import Resource, Namespace
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.dao.model.genre import GenreSchema
from app.decorators import auth_required, admin_required
from app.implemented import genre_service

genre_ns = Namespace('genres')

"""Роуты для жанров"""

@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        """Получение всех жанров"""
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        """Добавление нового жанра"""
        req_json = request.json
        new_genre = genre_service.create(req_json)
        response = make_response("", 201)
        response.headers['location'] = f"/{genre_ns.path}/{new_genre.id}"
        return response


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    @auth_required
    def get(self, genre_id: int):
        """Получение одного жанра по id"""
        r = genre_service.get_one(genre_id)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, genre_id: int):
        """Обновление жанра"""
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = genre_id
        genre_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, genre_id: int):
        """Удаление жанра по id"""
        try:
            genre_service.delete(genre_id)
        except UnmappedInstanceError:
            return "Такого жанра нет", 404
        return "", 204
