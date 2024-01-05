import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from pydantic import PositiveInt, UUID4
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


def get_income(access_token: str):
    """Function to get incomes."""
    url = base_url + "/income/view"

    try:
        response = requests.get(url=url, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # If request is successful
        json_responses = response.json()
        json_list = [
            (
                "S.No",
                "Account",
                "User",
                "Transacation ID",
                "Amount",
                "Method",
                "Status",
                "Timestamp",
            )
        ]

        total_income = 0

        for i, json_response in enumerate(json_responses):
            account_name = json_response["account_name"]
            user_name = json_response["user_name"]
            trans_id = json_response["trans_id"]
            amount = json_response["amount"]
            method = json_response["method"]
            status = json_response["status"]
            timestamp = json_response["timestamp"]

            total_income += float(amount)  # Calculating total income

            json_list.append(
                (
                    str(i + 1),
                    account_name,
                    user_name,
                    trans_id,
                    amount,
                    method,
                    status,
                    timestamp,
                )
            )

        return [json_list, total_income]

    return None


def add_income(amount: PositiveInt, method: str, access_token: str):
    """Function to add income to the database."""
    url = base_url + "/income/add"
    json_data = {"amount": amount, "method": method}  # Constructing the json data

    try:
        response = requests.post(url=url, json=json_data, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 201:  # Request is successful
        print("Amount added successfully")
        return True

    return False


def update_income(amount: PositiveInt, id: UUID4, access_token: str):
    """Function to update income in the database"""
    url = base_url + "/income/edit/"

    json_data = {"trans_id": id, "amount": amount}  # Constructing the json data

    try:
        response = requests.put(url=url, json=json_data, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        json_response = response.json()
        new_amount = json_response["amount"]

        print(f"Amount successfully changed to {new_amount}")
        return True

    return False
