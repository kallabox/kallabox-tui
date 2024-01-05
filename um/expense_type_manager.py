import um.ui.user_apps as user_apps
import um.ui.expense_type_apps as expense_type_apps
import um.ur.user_requests as user_requests
import um.ur.expense_type_requests as expense_type_requests


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


def retry_response(refresh_token: str):
    """Refreshes the current access token"""
    global access_token
    return_object = user_requests.refresh_access_token(refresh_token)
    if return_object[0] is False:
        return False

    else:
        access_token = return_object[1]
        return True


def manage_get_expense_type(access_token: str, refresh_token: str):
    """Management Function to get the expense types"""
    response = expense_type_requests.get_expense_type(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = expense_type_requests.get_expense_type(
                    access_token=access_token
                )

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = expense_type_apps.GetExpenseTypeApp()
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
        app = expense_type_apps.GetExpenseTypeApp()
        app.ROWS = response
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_expense_type(expense_type: str, access_token: str, refresh_token: str):
    """Management function to add expense types."""
    response = expense_type_requests.create_expense_type(
        expense_type=expense_type, access_token=access_token
    )
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = expense_type_requests.create_expense_type(
                    expense_type=expense_type, access_token=access_token
                )
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = expense_type_apps.AddExpenseTypeApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = expense_type_apps.AddExpenseTypeApp()
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_update_expense_type(
    expense_type: str | None,
    expense_id: str | None,
    access_token: str,
    refresh_token: str,
):
    """Management function to update expense types"""
    response = expense_type_requests.get_expense_type(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = expense_type_requests.get_expense_type(
                    access_token=access_token
                )
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = expense_type_apps.UpdateExpenseTypeApp()
                    app.ROWS = response
                    if expense_type is None or expense_id is None:
                        return app

                    update_response = expense_type_requests.update_expense_type(
                        id=expense_id,
                        expense_type=expense_type,
                        access_token=access_token,
                    )
                    if type(update_response) is tuple:
                        if update_response[1] == 401:
                            refreshed_access_token = retry_response(refresh_token)
                            if not refreshed_access_token:
                                app = construct_error_app(
                                    update_response[1], update_response[2]
                                )
                                return app

                            elif refreshed_access_token:
                                update_response = (
                                    expense_type_requests.update_expense_type(
                                        id=expense_id,
                                        expense_type=expense_type,
                                        access_token=access_token,
                                    )
                                )
                                if type(update_response) is tuple:
                                    app = construct_error_app(response[1], response[2])
                                    return app

                                elif update_response:
                                    new_response = (
                                        expense_type_requests.get_expense_type(
                                            access_token=access_token
                                        )
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
                            update_response[1], update_response[2]
                        )
                        return app

                    elif update_response:
                        new_response = expense_type_requests.get_expense_type(
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
        app = expense_type_apps.UpdateExpenseTypeApp()
        app.ROWS = response
        if expense_type is None or expense_id is None:
            return app

        update_response = expense_type_requests.update_expense_type(
            id=expense_id, expense_type=expense_type, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response(refresh_token)
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = expense_type_requests.update_expense_type(
                        id=expense_id,
                        expense_type=expense_type,
                        access_token=access_token,
                    )
                    if type(update_response) is tuple:
                        app = construct_error_app(response[1], response[2])
                        return app

                    elif update_response:
                        new_response = expense_type_requests.get_expense_type(
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
            new_response = expense_type_requests.get_expense_type(
                access_token=access_token
            )
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app
