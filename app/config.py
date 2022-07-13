"""Это файл конфигурации приложения, здесь может хранится путь к БД, ключ шифрования, что-то еще.
    Чтобы добавить новую настройку, допишите ее в класс."""

class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
