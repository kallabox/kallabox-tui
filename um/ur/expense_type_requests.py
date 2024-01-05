import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from pydantic import UUID4
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


def get_expense_type(access_token: str):
    """Function to get expense types from the database."""
    url = base_url + "/expense/view"

    try:
        response = requests.get(url=url, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        json_responses = response.json()
        json_list = [
            ("S.No", "Account", "User", "Expense Type ID", "Expense Type", "Timestamp")
        ]

        for i, json_response in enumerate(json_responses):
            account_name = json_response["account_name"]
            user_name = json_response["user_name"]
            expense_type_id = json_response["expense_type_id"]
            expense_type = json_response["expense_type"]
            timestamp = json_response["timestamp"]

            json_list.append(
                (
                    str(i + 1),
                    account_name,
                    user_name,
                    expense_type_id,
                    expense_type,
                    timestamp,
                )
            )

        return json_list

    return None


def create_expense_type(expense_type: str, access_token: str):
    """Function to create an expense type in the database."""
    url = base_url + "/expense/add"
    json_data = {"expense_type": expense_type}  # Constructing the json data

    try:
        response = requests.post(url=url, json=json_data, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 201:  # Request is successful
        print("Expense Type Created Successfully")
        return True

    return False


def update_expense_type(id: UUID4, expense_type: str, access_token: str):
    """Function to update an existing expense type in the database."""
    url = base_url + "/expense/edit/"
    json_data = {
        "expense_type_id": id,
        "expense_type": expense_type,
    }  # Constructing the json data

    try:
        response = requests.put(url=url, json=json_data, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        print("Expense Type Updated Successfully")
        return True

    return False
