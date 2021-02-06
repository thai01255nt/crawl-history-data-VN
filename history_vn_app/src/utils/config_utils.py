from configparser import ConfigParser
from history_vn_app import settings


def get_system_config(env, sections=('db', 'port', 'encrypt_secret')):
    # create a parser
    env = env if env else 'dev'
    parser = ConfigParser()

    # read config file
    filename = f'{settings.BASE_DIR}/configs/{env}.ini'
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    for section in sections:
        _config = {}
        if parser.has_section(section):
            options = parser.items(section)
            for option in options:
                _config[option[0]] = option[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        config[section] = _config
    return config
