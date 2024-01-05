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


def get_expenditure(access_token: str):
    """Function to get expenditures."""
    url = base_url + "/expenditure/view"

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
            (
                "S.No",
                "Account",
                "User",
                "Expend ID",
                "Amount",
                "Expense Type ID",
                "Status",
                "Timestamp",
            )
        ]

        total_expenditure = 0

        for i, json_response in enumerate(json_responses):
            account_name = json_response["account_name"]
            user_name = json_response["user_name"]
            expend_id = json_response["expend_id"]
            amount = json_response["amount"]
            expense_type_id = json_response["expense_type_id"]
            status = json_response["status"]
            timestamp = json_response["timestamp"]

            total_expenditure += float(amount)  # Calculating the total expenditure

            json_list.append(
                (
                    str(i + 1),
                    account_name,
                    user_name,
                    expend_id,
                    amount,
                    expense_type_id,
                    status,
                    timestamp,
                )
            )

        return [json_list, total_expenditure]

    return None


def create_expenditure(amount: int, expense: str, access_token: str):
    """Function to create an expenditure entry in the database."""
    url = base_url + "/expenditure/add"
    json_data = {"amount": amount, "expense": expense}  # Constructing the json data

    try:
        response = requests.post(url=url, auth=TokenAuth(access_token), json=json_data)
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 201:  # Request is successful
        print("Expenditure added successfully")
        return True

    return False


def update_expenditure(id: str, amount: int, expense: str, access_token: str):
    """Function to update an existing expenditure in the database."""
    url = base_url + "/expenditure/edit/"
    json_data = {
        "expend_id": id,
        "amount": amount,
        "expense": expense,
    }  # Constructing the json data

    try:
        response = requests.put(url=url, json=json_data, auth=TokenAuth(access_token))
        response.raise_for_status()  # Trying the request

    except HTTPError as e:
        print("HTTPError")
        print(str(response.status_code) + " : " + e.response.text)
        return (False, response.status_code, e.response.text)

    if response.status_code == 200:  # Request is successful
        print("Expense Changed")
        return True

    return False
