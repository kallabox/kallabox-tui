import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from pydantic import EmailStr
import sam.sar.req_base_url as rbu

base_url = rbu.req_get_base_url()


class TokenAuth(AuthBase):
    """Token Constructor class for valid token format."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


def create_account(
    account_name: str,
    user_name: str,
    email: EmailStr,
    phone: str,
    password: str,
    signup_token: str,
):
    """Function to create an account"""
    url = base_url + "/admin/account/create"
    json_data = {
        "account_name": account_name,
        "user_name": user_name,
        "email": email,
        "phone": phone,
        "password": password,
    }  # Constructing the json data

    try:
        response = requests.post(url=url, json=json_data, auth=TokenAuth(signup_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        print("Account Created Successfully")
        return True

    return False


def get_accounts_sa(signup_token: str):
    """Function to get accounts from the database."""
    url = base_url + "/admin/account"
    try:
        response = requests.get(url=url, auth=TokenAuth(signup_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        json_responses = response.json()

        json_list = [("S.No", "Account ID", "Account", "Status", "Timestamp")]
        for i, json_response in enumerate(json_responses):
            account_id = json_response["account_id"]
            account_name = json_response["account_name"]
            status = json_response["status"]
            timestamp = json_response["timestamp"]

            json_list.append((str(i + 1), account_id, account_name, status, timestamp))

        return json_list

    return None


def delete_account(account_name: str, signup_token: str):
    """Function to delete an account from the database."""
    url = base_url + "/admin/account"
    json_data = {"account_name": account_name}

    try:
        response = requests.delete(
            url=url, json=json_data, auth=TokenAuth(signup_token)
        )
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 204:  # Deletion is successful
        return True

    else:
        raise Exception("Could not process request")
