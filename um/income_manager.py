import um.ui.user_apps as user_apps
import um.ui.income_apps as income_apps
import um.ur.user_requests as user_requests
import um.ur.income_requests as income_requests


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


def manage_get_income(access_token: str, refresh_token: str):
    """Management Function to construct the get income app"""
    response = income_requests.get_income(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = income_requests.get_income(access_token=access_token)

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = income_apps.GetIncomeApp()
                    income_list, total_income = response[0], response[1]
                    app.ROWS = income_list
                    app.total_income = total_income
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = income_apps.GetIncomeApp()
        income_list, total_income = response[0], response[1]
        app.ROWS = income_list
        app.total_income = total_income
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_income(
    income: str, payment_method: str, access_token: str, refresh_token: str
):
    """Management function to add income."""
    response = income_requests.add_income(
        amount=income, method=payment_method, access_token=access_token
    )
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = income_requests.add_income(
                    amount=income, method=payment_method, access_token=access_token
                )

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = income_apps.AddIncomeApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = income_apps.AddIncomeApp()
        return app

    elif not response:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_update_income(
    income: None | str, trans_id: str | None, access_token: str, refresh_token: str
):
    """Management function used to update income."""
    response = income_requests.get_income(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response(refresh_token)
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = income_requests.get_income(access_token=access_token)

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is None:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

                elif type(response) is list:
                    app = income_apps.UpdateIncomeApp()
                    app.ROWS = response[0]

                    if income is None and trans_id is None:
                        return app

                    update_response = income_requests.update_income(
                        amount=income, id=trans_id, access_token=access_token
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
                                update_response = income_requests.update_income(
                                    amount=income,
                                    id=trans_id,
                                    access_token=access_token,
                                )
                                if type(update_response) is tuple:
                                    app = construct_error_app(response[1], response[2])
                                    return app

                                elif update_response is True:
                                    new_response = income_requests.get_income(
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
                        new_response = income_requests.get_income(
                            access_token=access_token
                        )
                        app.ROWS = new_response[0]
                        return app

                    elif update_response is None:
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
        app = income_apps.UpdateIncomeApp()
        app.ROWS = response[0]

        if income is None or trans_id is None:
            return app

        update_response = income_requests.update_income(
            amount=income, id=trans_id, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response(refresh_token)
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = income_requests.update_income(
                        amount=income, id=trans_id, access_token=access_token
                    )
                    if type(update_response) is tuple:
                        app = construct_error_app(response[1], response[2])
                        return app

                    elif update_response is True:
                        new_response = income_requests.get_income(
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
            new_response = income_requests.get_income(access_token=access_token)
            app.ROWS = new_response[0]
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app
