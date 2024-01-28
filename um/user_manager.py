import um.ui.user_apps as user_apps
import um.ui.account_apps as account_apps
import um.ur.user_requests as user_requests


def construct_error_app(status_code: int | str, message: str):
    """Error app constructor function"""
    if "detail" in message:
        index = message.find("detail")
        start_index = index + 8
        message = message[start_index:-1]

    app = user_apps.ErrorApp()
    app.status_code = status_code
    app.message = message
    return app


def retry_response(refresh_token):
    """Refreshes the current access token"""
    return_object = user_requests.refresh_access_token(refresh_token)
    if return_object[0] is False:
        return (False, None)

    else:
        access_token = return_object[1]
        return (True, access_token)


def manage_get_users(access_token: str, refresh_token: str):
    """Management Function to get users."""
    response = user_requests.get_users(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token_status, access_token = retry_response(refresh_token)
            if not refreshed_access_token_status:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token_status:
                response = user_requests.get_users(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_apps.GetUsersApp()
                    app.ROWS = response
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = account_apps.GetUsersApp()
        app.ROWS = response
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_user(
    email, user_name, phone, password, role, access_token: str, refresh_token: str
):
    """Management function to add user."""
    response = user_requests.create_user(
        email=email,
        user_name=user_name,
        phone=phone,
        password=password,
        role=role,
        access_token=access_token,
    )

    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token_status, access_token = retry_response(refresh_token)
            if not refreshed_access_token_status:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token_status:
                response = user_requests.create_user(
                    email=email,
                    user_name=user_name,
                    phone=phone,
                    password=password,
                    role=role,
                    access_token=access_token,
                )
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = account_apps.AddUserApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is dict:
        app = account_apps.AddUserApp()
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_update_user_role(
    user_name: str | None, role: str | None, access_token: str, refresh_token: str
):
    """Management function to update user role"""
    response = user_requests.get_users(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token_status, access_token = retry_response(refresh_token)
            if not refreshed_access_token_status:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token_status:
                response = user_requests.get_users(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = account_apps.UpdateUserRoleApp()
                    app.ROWS = response

                    if user_name is None or role is None:
                        return app

                    update_response = user_requests.update_user_role(
                        user_name=user_name, role=role, access_token=access_token
                    )
                    if type(update_response) is tuple:
                        if update_response[1] == 401:
                            (
                                refreshed_access_token_status,
                                access_token,
                            ) = retry_response(refresh_token)
                            if not refreshed_access_token_status:
                                app = construct_error_app(
                                    update_response[1], update_response[2]
                                )
                                return app

                            elif refreshed_access_token_status:
                                update_response = user_requests.update_user_role(
                                    user_name=user_name,
                                    role=role,
                                    access_token=access_token,
                                )

                                if type(update_response) is tuple:
                                    app = construct_error_app(
                                        update_response[1], update_response[2]
                                    )
                                    return app

                                elif update_response:
                                    new_response = user_requests.get_users(
                                        access_token=access_token
                                    )
                                    app.ROWS = new_response
                                    return app

                                else:
                                    app = construct_error_app(
                                        status_code=409,
                                        message="Could not process request",
                                    )
                                    return app

                    elif update_response:
                        new_response = user_requests.get_users(
                            access_token=access_token
                        )
                        app.ROWS = new_response
                        return app

                    else:
                        app = construct_error_app(
                            status_code=409, message="Could not process request"
                        )
                        return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = account_apps.UpdateUserRoleApp()
        app.ROWS = response

        if user_name is None or role is None:
            return app

        update_response = user_requests.update_user_role(
            user_name=user_name, role=role, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token_status, access_token = retry_response(
                    refresh_token
                )
                if not refreshed_access_token_status:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token_status:
                    update_response = user_requests.update_user_role(
                        user_name=user_name, role=role, access_token=access_token
                    )

                    if type(update_response) is tuple:
                        app = construct_error_app(
                            update_response[1], update_response[2]
                        )
                        return app

                    elif update_response:
                        new_response = user_requests.get_users(
                            access_token=access_token
                        )
                        app.ROWS = new_response
                        return app

                    else:
                        app = construct_error_app(
                            status_code=409, message="Could not process request"
                        )
                        return app

            app = construct_error_app(update_response[1], update_response[2])
            return app

        elif update_response:
            new_response = user_requests.get_users(access_token=access_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_delete_user(user_name: None | str, access_token: str, refresh_token: str):
    """Management function to delete user"""
    response = user_requests.get_users(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token_status, access_token = retry_response(refresh_token)
            if not refreshed_access_token_status:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token_status:
                response = user_requests.get_users(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = account_apps.DeleteUserApp()
                    app.ROWS = response

                    if user_name is None:
                        return app

                    delete_response = user_requests.delete_user(
                        user_name=user_name, access_token=access_token
                    )
                    if type(delete_response) is tuple:
                        if delete_response[1] == 401:
                            (
                                refreshed_access_token_status,
                                access_token,
                            ) = retry_response(refresh_token)
                            if not refreshed_access_token_status:
                                app = construct_error_app(
                                    delete_response[1], delete_response[2]
                                )
                                return app

                            elif refreshed_access_token_status:
                                delete_response = user_requests.delete_user(
                                    user_name=user_name, access_token=access_token
                                )

                                if type(delete_response) is tuple:
                                    app = construct_error_app(
                                        delete_response[1], delete_response[2]
                                    )
                                    return app

                                elif delete_response:
                                    new_response = user_requests.get_users(
                                        access_token=access_token
                                    )
                                    app.ROWS = new_response
                                    return app

                                else:
                                    app = construct_error_app(
                                        status_code=409,
                                        message="Could not process request",
                                    )
                                    return app

                        app = construct_error_app(
                            delete_response[1], delete_response[2]
                        )
                        return app

                    elif delete_response:
                        new_response = user_requests.get_users(
                            access_token=access_token
                        )
                        app.ROWS = new_response
                        return app

                    else:
                        app = construct_error_app(
                            status_code=409, message="Could not process request"
                        )
                        return app

            else:
                app = construct_error_app(
                    status_code=409, message="Could not process request"
                )
            return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app

    elif type(response) is list:
        app = account_apps.DeleteUserApp()
        app.ROWS = response

        if user_name is None:
            return app

        delete_response = user_requests.delete_user(
            user_name=user_name, access_token=access_token
        )
        if type(delete_response) is tuple:
            if delete_response[1] == 401:
                refreshed_access_token_status, access_token = retry_response(
                    refresh_token
                )
                if not refreshed_access_token_status:
                    app = construct_error_app(delete_response[1], delete_response[2])
                    return app

                elif refreshed_access_token_status:
                    delete_response = user_requests.delete_user(
                        user_name=user_name, access_token=access_token
                    )

                    if type(delete_response) is tuple:
                        app = construct_error_app(
                            delete_response[1], delete_response[2]
                        )
                        return app

                    elif delete_response:
                        new_response = user_requests.get_users(
                            access_token=access_token
                        )
                        app.ROWS = new_response
                        return app

                    else:
                        app = construct_error_app(
                            status_code=409, message="Could not process request"
                        )
                        return app

            app = construct_error_app(delete_response[1], delete_response[2])
            return app

        elif delete_response:
            new_response = user_requests.get_users(access_token=access_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app
