from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


from views_planilha import *

from views_user import *

from views import *


if __name__ == '__main__':
    app.run(debug=True)
