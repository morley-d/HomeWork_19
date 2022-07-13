from flask import request, make_response
from flask_restx import Resource, Namespace
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.dao.model.director import DirectorSchema
from app.decorators import auth_required, admin_required
from app.implemented import director_service

director_ns = Namespace('directors')

"""Роуты для режисеров"""

@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        """Получение всех режиссеров"""
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        """Добавление нового режиссера"""
        req_json = request.json
        new_director = director_service.create(req_json)
        response = make_response("", 201)
        response.headers['location'] = f"/{director_ns.path}/{new_director.id}"
        return response


@director_ns.route('/<int:dir_id>')
class DirectorView(Resource):
    @auth_required
    def get(self, dir_id: int):
        """Получение режиссера по id"""
        r = director_service.get_one(dir_id)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, dir_id: int):
        """Обновление режиссера"""
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = dir_id
        director_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, dir_id: int):
        """Удаление режиссера по id"""
        try:
            director_service.delete(dir_id)
        except UnmappedInstanceError:
            return "Такого режиссера нет", 404
        return "", 204
