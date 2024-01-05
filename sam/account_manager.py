import sam.sai.account_apps as account_apps
import sam.sai.interface_app as interface_app
import sam.sar.account_requests as account_requests


def construct_error_app(status_code: int | str, message: str):
    """Error app constructor function"""
    if "detail" in message:
        index = message.find("detail")
        start_index = index + 8
        message = message[start_index:-1]
    app = interface_app.ErrorApp()
    app.status_code = status_code
    app.message = message
    return app


def manage_get_accounts(signup_token: str):
    """Management function to get accounts."""
    response = account_requests.get_accounts_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = account_apps.SAGetAccountsApp()
        app.ROWS = response
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_create_account(
    account_name: str,
    user_name: str,
    email: str,
    phone: str,
    password: str,
    signup_token: str,
):
    """Management function to create an account"""
    response = account_requests.create_account(
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
        app = account_apps.SACreateAccountApp()
        return app

    elif response is None or response is False:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_delete_account(account_name: None | str, signup_token: str):
    """Management function to delete an account."""
    response = account_requests.get_accounts_sa(signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = account_apps.SADeleteAccountApp()
        app.ROWS = response

        if account_name is None:
            return app

        delete_response = account_requests.delete_account(
            account_name=account_name, signup_token=signup_token
        )
        if type(delete_response) is tuple:
            app = construct_error_app(delete_response[1], delete_response[2])
            return app

        elif delete_response is True:
            new_response = account_requests.get_accounts_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        elif delete_response is None:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_purge_account(account_name: None | str, signup_token: str):
    """Management function to purge an account."""
    response = account_requests.get_accounts_sa(signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = account_apps.SAPurgeAccountApp()
        app.ROWS = response

        if account_name is None:
            return app

        purge_response = account_requests.purge_account(
            account_name=account_name, signup_token=signup_token
        )
        if type(purge_response) is tuple:
            app = construct_error_app(purge_response[1], purge_response[2])
            return app

        elif purge_response is True:
            new_response = account_requests.get_accounts_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        elif purge_response is None:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app
