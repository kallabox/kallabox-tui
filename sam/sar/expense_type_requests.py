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


def get_expense_types_sa(signup_token: str):
    """Function to get the expense types from the database."""
    url = base_url + "/admin/expense"
    try:
        response = requests.get(url=url, auth=TokenAuth(signup_token))
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
