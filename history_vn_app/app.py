import os
from flask import Flask
from flask_cors import CORS

from history_vn_app.src.utils.config_utils import get_system_config

app = Flask(__name__)
CORS(app)
env = os.getenv("FLASK_ENV")
config_data = get_system_config(env)
app.config["SYS"] = config_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
