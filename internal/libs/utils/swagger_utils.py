import json


class SwaggerUtils:
    @staticmethod
    def replace_host(path, host):
        with open(path, 'r') as fp:
            swagger_dict = json.load(fp)
        swagger_dict['host'] = host
        with open(path, 'w') as fp:
            json.dump(swagger_dict, fp)
        return
