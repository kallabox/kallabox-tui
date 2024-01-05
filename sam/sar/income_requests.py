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


def get_income_sa(signup_token: str):
    """Function to get incomes in the database."""
    url = base_url + "/admin/income"
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
            (
                "S.No",
                "Account",
                "User",
                "Transaction ID",
                "Amount",
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
            status = json_response["status"]
            timestamp = json_response["timestamp"]

            total_income += float(
                amount
            )  # Calculating the total income of all users in the database

            json_list.append(
                (
                    str(i + 1),
                    account_name,
                    user_name,
                    trans_id,
                    amount,
                    status,
                    timestamp,
                )
            )

        return [json_list, total_income]

    return None
