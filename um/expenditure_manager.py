import um.ui.user_apps as user_apps
import um.ui.expenditure_apps as expenditure_apps
import um.ur.expenditure_requests as expenditure_requests
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


def retry_response(refresh_token: str):
    """Refreshes the current access token"""
    global access_token
    return_object = user_requests.refresh_access_token(refresh_token)
    if return_object[0] is False:
        return False

    else:
        access_token = return_object[1]
        return True


def manage_get_expenditure(access_token: str, refresh_token: str):
    """Management Function to construct the get expenditure app"""
    response = expenditure_requests.get_expenditure(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = expenditure_requests.get_expenditure(
                    access_token=access_token
                )
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = expenditure_apps.GetExpenditureApp()
                    expenditure_list, total_expenditure = response[0], response[1]
                    app.ROWS = expenditure_list
                    app.total_expenditure = total_expenditure
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = expenditure_apps.GetExpenditureApp()
        expenditure_list, total_expenditure = response[0], response[1]
        app.ROWS = expenditure_list
        app.total_expenditure = total_expenditure
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_expenditure(amount: str, expense, access_token: str, refresh_token: str):
    """Management function to add expenditure."""
    response = expenditure_requests.create_expenditure(
        amount=amount, expense=expense, access_token=access_token
    )
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = expenditure_requests.create_expenditure(
                    amount=amount, expense=expense, access_token=access_token
                )

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = expenditure_apps.AddExpenditureApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = expenditure_apps.AddExpenditureApp()
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_update_expenditure(
    amount: str | None,
    expense: str | None,
    expend_id: str | None,
    access_token: str,
    refresh_token: str,
):
    """Management function used to update expenditure"""
    response = expenditure_requests.get_expenditure(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = expenditure_requests.get_expenditure(
                    access_token=access_token
                )

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is None:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

                elif type(response) is list:
                    app = expenditure_apps.UpdateExpenditureApp()
                    app.ROWS = response[0]
                    if amount is None or expense is None or expend_id is None:
                        return app

                    update_response = expenditure_requests.update_expenditure(
                        id=expend_id,
                        amount=amount,
                        expense=expense,
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
                                    expenditure_requests.update_expenditure(
                                        id=expend_id,
                                        amount=amount,
                                        expense=expense,
                                        access_token=access_token,
                                    )
                                )

                                if type(update_response) is tuple:
                                    app = construct_error_app(response[1], response[2])
                                    return app

                                elif update_response is True:
                                    new_response = expenditure_requests.get_expenditure(
                                        access_token=access_token
                                    )
                                    app.ROWS = new_response[0]
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

                    elif update_response is True:
                        new_response = expenditure_requests.get_expenditure(
                            access_token=access_token
                        )
                        app.ROWS = new_response[0]
                        return app

                    else:
                        app = construct_error_app(
                            status_code=409, message="Could not process request"
                        )
                        return app

        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = expenditure_apps.UpdateExpenditureApp()
        app.ROWS = response[0]
        if amount is None or expense is None or expend_id is None:
            return app

        update_response = expenditure_requests.update_expenditure(
            id=expend_id, amount=amount, expense=expense, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response(refresh_token)
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = expenditure_requests.update_expenditure(
                        id=expend_id,
                        amount=amount,
                        expense=expense,
                        access_token=access_token,
                    )

                    if type(update_response) is tuple:
                        app = construct_error_app(response[1], response[2])
                        return app

                    elif update_response is True:
                        new_response = expenditure_requests.get_expenditure(
                            access_token=access_token
                        )
                        app.ROWS = new_response[0]
                        return app

                    else:
                        app = construct_error_app(
                            status_code=409, message="Could not process request"
                        )
                        return app

            app = construct_error_app(update_response[1], update_response[2])
            return app

        elif update_response is True:
            new_response = expenditure_requests.get_expenditure(
                access_token=access_token
            )
            app.ROWS = new_response[0]
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app
