import requests
from requests.auth import AuthBase
from requests.exceptions import HTTPError
from pydantic import PositiveInt, UUID4, EmailStr


class TokenAuth(AuthBase):
    """Token class to construct the access token in the required format"""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


base_url = "http://127.0.0.1:8000/api"  # Need to be changed

# User Abstractions


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


# Account Admin Abstractions


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


# Income Abstractions


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


# Expenditure abstractions


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


### Expense Type Abstractions


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
