import os

from flask_sqlalchemy import SQLAlchemy

from ..app import app
from ..src.utils.config_utils import get_system_config

env = os.getenv("FLASK_ENV")
db_config = get_system_config(env)['db']

db_connection = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
    database=db_config['database']
)

app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 30
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 300
app.config["SQLALCHEMY_MAX_OVERFLOW"] = -1
db = SQLAlchemy(app)
