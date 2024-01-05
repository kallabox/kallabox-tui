import sam.sai.user_apps as user_apps
import sam.sai.interface_app as interface_app
import sam.sar.user_requests as user_requests


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


def manage_get_users(signup_token: str):
    """Management function to get users"""
    response = user_requests.get_users_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = user_apps.SAGetUsersApp()
        app.ROWS = response
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_delete_user(
    account_name: None | str, user_name: None | str, signup_token: str
):
    """Management function to delete an user."""
    response = user_requests.get_users_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = user_apps.SADeleteUserApp()
        app.ROWS = response

        if account_name is None and user_name is None:
            return app

        delete_response = user_requests.delete_user_sa(
            account_name=account_name, user_name=user_name, signup_token=signup_token
        )
        if type(delete_response) is tuple:
            app = construct_error_app(delete_response[1], delete_response[2])
            return app

        elif delete_response is True:
            new_response = user_requests.get_users_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_update_user_role(
    account_name: None | str, user_name: None | str, role: None | str, signup_token: str
):
    """Management function to update user role"""
    response = user_requests.get_users_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = user_apps.SAUpdateUserRoleApp()
        app.ROWS = response

        if account_name is None and user_name is None and role is None:
            return app

        update_response = user_requests.update_user_role_sa(
            user_name=user_name,
            account_name=account_name,
            role=role,
            signup_token=signup_token,
        )

        if type(update_response) is tuple:
            app = construct_error_app(update_response[1], update_response[2])
            return app

        elif update_response is True:
            new_response = user_requests.get_users_sa(signup_token=signup_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app
