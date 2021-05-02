import json


def get_json_body(request):
    request_header = request_body = {}

    if request.query_string != b"":
        request_header = request.args.to_dict()
    if request.data != b"":
        request_body = json.loads(request.data)

    return request_header, request_body


def get_param(key: str, request_body: dict):
    if key in request_body:
        return request_body[key]
    return ""
