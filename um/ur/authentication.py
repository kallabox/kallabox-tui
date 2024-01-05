import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
import um.ur.req_base_url as rbu

base_url = rbu.req_get_base_url()


class TokenAuth(AuthBase):
    """Token class to construct the access token in the required format"""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


def refresh_access_token(refresh_token: str):
    """Function used to refresh access tokens."""

    url = base_url + "/refresh"

    try:
        response = requests.get(url=url, auth=TokenAuth(refresh_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # If request is successful
        json_response = response.json()
        access_token = json_response["access_token"]
        user_id = json_response["user_id"]
        account_id = json_response["account_id"]
        role = json_response["role"]
        return (True, access_token, account_id, user_id, role)


def login(account_name: str, user_name: str, password: str):
    """Function used to login the user."""

    url = base_url + "/login"

    json_data = {
        "account_name": account_name,
        "user_name": user_name,
        "password": password,
    }  # Constructing the json data
    try:
        response = requests.post(url=url, json=json_data)
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # If request is successful
        json_response = response.json()
        refresh_token = json_response["refresh_token"]

        return_object = refresh_access_token(refresh_token=refresh_token)

        if not return_object[0]:
            return return_object

        elif return_object[0]:
            access_token, account_id, user_id, role = (
                return_object[1],
                return_object[2],
                return_object[3],
                return_object[4],
            )

        return (True, refresh_token, access_token, account_id, user_id, role)


def logout(access_token: str):
    """Function used to logout the user."""
    url = base_url + "/logout"

    try:
        response = requests.get(url=url, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    return True
