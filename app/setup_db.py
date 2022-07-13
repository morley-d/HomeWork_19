"""Создаём объект SQLAlchemy, который далее будет импортироваться
    в другие модули"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
