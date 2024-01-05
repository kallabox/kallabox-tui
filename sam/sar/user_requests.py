import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
import sam.sar.req_base_url as rbu

base_url = rbu.req_get_base_url()


class TokenAuth(AuthBase):
    """Token Constructor class for valid token format."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


def update_user_role_sa(
    user_name: str, account_name: str, role: str, signup_token: str
):
    """Function to update user role."""
    url = base_url + "/admin/account/user"
    json_data = {
        "user_name": user_name,
        "account_name": account_name,
        "role": role,
    }  # Constructing the json data

    try:
        response = requests.put(url=url, json=json_data, auth=TokenAuth(signup_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        print("User role updated successfully")
        return True

    return False


def delete_user_sa(account_name: str, user_name: str, signup_token: str):
    """Function to delete an user."""
    url = base_url + "/admin/account/user"
    json_data = {
        "account_name": account_name,
        "user_name": user_name,
    }  # Constructing the json data

    try:
        response = requests.delete(
            url=url, json=json_data, auth=TokenAuth(signup_token)
        )
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 204:  # Request is successful
        print("User Deleted Successfully")
        return True

    return False


def get_users_sa(signup_token: str):
    """Function to get the users from the database."""
    url = base_url + "/admin/users"
    try:
        response = requests.get(url=url, auth=TokenAuth(signup_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        json_responses = response.json()

        json_list = [("S.No", "Account", "User", "Email", "Timestamp", "Role")]

        for i, json_response in enumerate(json_responses):
            account_name = json_response["account_name"]
            user_name = json_response["user_name"]
            email = json_response["email"]
            timestamp = json_response["timestamp"]
            role = json_response["role"]
            json_list.append(
                (str(i + 1), account_name, user_name, email, timestamp, role)
            )

        return json_list

    return None
