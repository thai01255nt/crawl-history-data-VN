from flask_mongoengine import MongoEngine
from internal.app import app
from internal.src.common.consts.database_consts import DbAliasType
config = app.config['SYS']

mongodb_settings = {
    'host': config['MONGODB_URI'],
    'alias':DbAliasType.API_HISTORY_DATA_VN
}

app.config['MONGODB_SETTINGS'] = mongodb_settings
db = MongoEngine(app)
