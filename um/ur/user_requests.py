import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from pydantic import EmailStr
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


def get_users(access_token: str):
    """Function used to get users."""
    url = base_url + "/account/admin/users/view"

    try:
        response = requests.get(url=url, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # If request is successful
        json_responses = response.json()

        json_list = [("S.No", "Account", "User", "Email", "Role", "Timestamp")]

        for i, json_response in enumerate(json_responses):
            account_name = json_response["account_name"]
            user_name = json_response["user_name"]
            email = json_response["email"]
            timestamp = json_response["timestamp"]
            role = json_response["role"]
            json_list.append(
                (str(i + 1), account_name, user_name, email, role, timestamp)
            )

        return json_list


def update_user_role(user_name: str, role: str, access_token: str):
    """Function to update user role."""
    url = base_url + "/account/admin/user/role"
    json_data = {"user_name": user_name, "role": role}  # Constructing the json data

    try:
        response = requests.put(url=url, auth=TokenAuth(access_token), json=json_data)
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # If request is successful
        json_response = response.json()
        return json_response

    else:
        raise Exception("Could not process request")


def create_user(
    email: EmailStr,
    user_name: str,
    phone: str,
    password: str,
    role: str,
    access_token: str,
):
    """Function to create an user"""
    url = base_url + "/account/create/user"
    json_data = {
        "user_name": user_name,
        "email": email,
        "phone": phone,
        "password": password,
        "role": role,
    }  # Constructing the json data

    try:
        response = requests.post(url=url, auth=TokenAuth(access_token), json=json_data)
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 201:  # If request is successful
        json_response = response.json()
        return json_response

    else:
        raise Exception("Could not process request")


def delete_user(user_name: str, access_token: str):
    """Function to delete an user."""
    url = base_url + "/account/remove/user"
    json_data = {"user_name": user_name}  # Constructing the json data

    try:
        response = requests.delete(
            url=url, json=json_data, auth=TokenAuth(access_token)
        )
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 204:  # if request is successful
        return True

    else:
        raise Exception("Could not process request")
