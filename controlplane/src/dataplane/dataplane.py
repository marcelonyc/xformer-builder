import requests
import config.app_config as app_config
from flask_login import current_user
import json

config = app_config.AppConfig()


def dataplane_get(endpoint: str, headers: dict = None, auth: bool = True):
    if auth:
        default_headers = {"Authorization": f"Bearer {current_user.id}"}
    else:
        default_headers = {}

    if headers is not None:
        headers = {**headers, **default_headers}
    else:
        headers = default_headers

    response = requests.get(config.dataplane_url + endpoint, headers=headers)
    return response.json()


def dataplane_get_file(endpoint: str, headers: dict = None, auth: bool = True):
    if auth:
        default_headers = {"Authorization": f"Bearer {current_user.id}"}
    else:
        default_headers = {}

    if headers is not None:
        headers = {**headers, **default_headers}
    else:
        headers = default_headers

    response = requests.get(config.dataplane_url + endpoint, headers=headers)
    return response


def dataplane_post(
    endpoint: str,
    data: dict = None,
    auth: bool = True,
    files: dict = None,
    headers: dict = None,
):
    if auth:
        default_headers = {"Authorization": f"Bearer {current_user.id}"}
    else:
        default_headers = {}

    if headers is not None:
        headers = {**headers, **default_headers}
    else:
        headers = default_headers

    try:
        if files is not None:
            response = requests.post(
                config.dataplane_url + endpoint,
                data=data,
                headers=headers,
                files=files,
            )
        else:
            response = requests.post(
                config.dataplane_url + endpoint,
                data=json.dumps(data),
                headers=headers,
            )
    except Exception as e:
        return {"error": str(e)}

    if response.status_code != 200:
        return {"error": f"{response.status_code} - {response.text}"}
    return response.json()


def dataplane_login(app_token: str):
    header = {"Authorization": f"Bearer {app_token}"}
    response = dataplane_get("/login", headers=header, auth=False)

    return response
