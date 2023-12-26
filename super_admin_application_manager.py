import super_admin_interface as sai
import super_admin_requests as req
from os import environ


base_url = "http://127.0.0.1:8000/api"


def construct_error_app(status_code, message):
    """Error app constructor function"""
    if "detail" in message:
        index = message.find("detail")
        start_index = index + 8
        message = message[start_index:-1]
    app = sai.ErrorApp()
    app.status_code = status_code
    app.message = message
    return app


try:
    signup_token = environ("SIGNUP_TOKEN")
except:
    new_app = construct_error_app(status_code="", message="Token not found")
    new_app.run()


if signup_token == "" or type(signup_token) is not str:
    new_app = construct_error_app(status_code="", message="Not a valid token")

else:
    new_app = sai.SuperAdminInterfaceApp()


app_stack = [None, new_app]


def manage_get_income():
    """Management function to get income."""
    response = req.get_income_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = sai.SAGetIncomeApp()
        income_list = response[0]
        total_income = response[1]
        app.ROWS = income_list
        app.total_income = total_income
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_expenditure():
    """Management function to get expenditures"""
    response = req.get_expenditure_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = sai.SAGetExpenditureApp()
        expenditure_list = response[0]
        total_expenditure = response[1]
        app.ROWS = expenditure_list
        app.total_expenditure = total_expenditure
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_expense_types():
    """Manangement function to get expense types"""
    response = req.get_expense_types_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = sai.SAGetExpenseTypeApp()
        app.ROWS = response
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_users():
    """Management function to get users"""
    response = req.get_users_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = sai.SAGetUsersApp()
        app.ROWS = response
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_accounts():
    """Management function to get accounts."""
    response = req.get_accounts_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = sai.SAGetAccountsApp()
        app.ROWS = response
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_create_account(
    account_name: str, user_name: str, email: str, phone: str, password: str
):
    """Management function to create an account"""
    response = req.create_account(
        account_name=account_name,
        user_name=user_name,
        email=email,
        phone=phone,
        password=password,
        signup_token=signup_token,
    )
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = sai.SACreateAccountApp()
        return app

    elif response is None or response is False:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_delete_account(account_name=None):
    """Management function to delete an account."""
    response = req.get_accounts_sa(signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = sai.SADeleteAccountApp()
        app.ROWS = response

        if account_name is None:
            return app

        delete_response = req.delete_account(
            account_name=account_name, signup_token=signup_token
        )
        if type(delete_response) is tuple:
            app = construct_error_app(delete_response[1], delete_response[2])
            return app

        elif delete_response is True:
            new_response = req.get_accounts_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        elif delete_response is None:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_purge_account(account_name=None):
    """Management function to purge an account."""
    response = req.get_accounts_sa(signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = sai.SAPurgeAccountApp()
        app.ROWS = response

        if account_name is None:
            return app

        purge_response = req.purge_account(
            account_name=account_name, signup_token=signup_token
        )
        if type(purge_response) is tuple:
            app = construct_error_app(purge_response[1], purge_response[2])
            return app

        elif purge_response is True:
            new_response = req.get_accounts_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        elif purge_response is None:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_delete_user(account_name=None, user_name=None):
    """Management function to delete an user."""
    response = req.get_users_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = sai.SADeleteUserApp()
        app.ROWS = response

        if account_name is None and user_name is None:
            return app

        delete_response = req.delete_user_sa(
            account_name=account_name, user_name=user_name, signup_token=signup_token
        )
        if type(delete_response) is tuple:
            app = construct_error_app(delete_response[1], delete_response[2])
            return app

        elif delete_response is True:
            new_response = req.get_users_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_update_user_role(account_name=None, user_name=None, role=None):
    """Management function to update user role"""
    response = req.get_users_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = sai.SAUpdateUserRoleApp()
        app.ROWS = response

        if account_name is None and user_name is None and role is None:
            return app

        update_response = req.update_user_role_sa(
            user_name=user_name,
            account_name=account_name,
            role=role,
            signup_token=signup_token,
        )

        if type(update_response) is tuple:
            app = construct_error_app(update_response[1], update_response[2])
            return app

        elif update_response is True:
            new_response = req.get_users_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


# Running the app stack

while app_stack:
    app = app_stack.pop()

    if app is None:
        break

    response = app.run()

    if app.name == "super_admin_interface_app":
        if response == "user":
            new_app = sai.SuperAdminUserInterfaceApp()
            app_stack.append(new_app)

        elif response == "account":
            new_app = sai.SuperAdminAccountInterfaceApp()
            app_stack.append(new_app)

        elif response == "get_income":
            new_app = manage_get_income()
            app_stack.append(new_app)

        elif response == "get_expenditure":
            new_app = manage_get_expenditure()
            app_stack.append(new_app)

        elif response == "get_expense_types":
            new_app = manage_get_expense_types()
            app_stack.append(new_app)

    elif app.name == "super_admin_account_interface_app":
        if response == "back":
            new_app = sai.SuperAdminInterfaceApp()
            app_stack.append(new_app)

        elif response == "get_accounts":
            new_app = manage_get_accounts()
            app_stack.append(new_app)

        elif response == "create_account":
            new_app = sai.SACreateAccountApp()
            app_stack.append(new_app)

        elif response == "delete_account":
            new_app = manage_delete_account()
            app_stack.append(new_app)

        elif response == "purge_account":
            new_app = manage_purge_account()
            app_stack.append(new_app)

    elif app.name == "super_admin_user_interface_app":
        if response == "back":
            new_app = sai.SuperAdminInterfaceApp()
            app_stack.append(new_app)

        elif response == "update_user_role":
            new_app = manage_update_user_role()
            app_stack.append(new_app)

        elif response == "delete_user":
            new_app = manage_delete_user()
            app_stack.append(new_app)

        elif response == "get_users":
            new_app = manage_get_users()
            app_stack.append(new_app)

    elif app.name == "super_admin_update_user_role_app":
        if response == "back":
            new_app = sai.SuperAdminUserInterfaceApp()
            app_stack.append(new_app)

        elif type(response) is tuple:
            user_name, account_name, role = response[0], response[1], response[2]
            new_app = manage_update_user_role(
                account_name=account_name, user_name=user_name, role=role
            )
            app_stack.append(new_app)

    elif app.name == "super_admin_delete_user_app":
        if response == "back":
            new_app = sai.SuperAdminUserInterfaceApp()
            app_stack.append(new_app)

        elif type(response) is tuple:
            account_name, user_name = response[0], response[1]
            new_app = manage_delete_user(account_name=account_name, user_name=user_name)
            app_stack.append(new_app)

    elif app.name == "super_admin_get_users_app":
        if response == "back":
            new_app = sai.SuperAdminUserInterfaceApp()
            app_stack.append(new_app)

    elif app.name == "super_admin_get_accounts_app":
        if response == "back":
            new_app = sai.SuperAdminAccountInterfaceApp()
            app_stack.append(new_app)

    elif app.name == "super_admin_create_account_app":
        if response == "back":
            new_app = sai.SuperAdminAccountInterfaceApp()
            app_stack.append(new_app)

        elif type(response) is tuple:
            account_name, user_name, email, phone, password = (
                response[0],
                response[1],
                response[2],
                response[3],
                response[4],
            )
            new_app = manage_create_account(
                account_name=account_name,
                user_name=user_name,
                email=email,
                phone=phone,
                password=password,
            )
            app_stack.append(new_app)

    elif app.name == "super_admin_delete_account_app":
        if response == "back":
            new_app = sai.SuperAdminAccountInterfaceApp()
            app_stack.append(new_app)

        else:
            account_name = response
            new_app = manage_delete_account(account_name=account_name)
            app_stack.append(new_app)

    elif app.name == "super_admin_purge_account_app":
        if response == "back":
            new_app = sai.SuperAdminAccountInterfaceApp()
            app_stack.append(new_app)

        else:
            account_name = response
            new_app = manage_purge_account(account_name=account_name)
            app_stack.append(new_app)

    elif app.name == "super_admin_get_income_app":
        if response == "back":
            new_app = sai.SuperAdminInterfaceApp()
            app_stack.append(new_app)

    elif app.name == "super_admin_get_expenditure_app":
        if response == "back":
            new_app = sai.SuperAdminInterfaceApp()
            app_stack.append(new_app)

    elif app.name == "super_admin_get_expense_type_app":
        if response == "back":
            new_app = sai.SuperAdminInterfaceApp()
            app_stack.append(new_app)

    elif app.name == "error_app":
        if response == "back":
            new_app = sai.SuperAdminInterfaceApp()
            app_stack.append(new_app)
