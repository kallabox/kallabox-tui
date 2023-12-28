import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from pydantic import EmailStr
import config


class TokenAuth(AuthBase):
    """Token Constructor class for valid token format."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


base_url = config.get_base_url()


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


def purge_account(account_name: str, signup_token: str):
    """Function to purge an account."""
    url = base_url + "/admin/account"
    json_data = {"account_name": account_name}  # Constructing the json data

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
        print("Account purged successfully")
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


def get_expenditure_sa(signup_token: str):
    """Function to get expenditures from the database."""
    url = base_url + "/admin/expenditure"
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
                "Expense ID",
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
