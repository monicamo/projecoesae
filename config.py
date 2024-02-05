import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:biju@localhost/planilhateca'
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'


UPLOAD_EXCEL_PATH = os.path.dirname(os.path.abspath(__file__)) + '/excels'