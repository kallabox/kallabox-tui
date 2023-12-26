import user_interface
import user_requests as req

login_success = False

while not login_success:
    app = user_interface.LoginPageApp()
    reply = app.run()
    account_name, user_name, password = reply[0], reply[1], reply[2]
    response = req.login(
        account_name=account_name, user_name=user_name, password=password
    )
    boolean, value_1, value_2 = response[0], response[1], response[2]

    if not boolean:
        continue

    elif boolean:
        refresh_token, access_token, account_id, user_id, role = (
            value_1,
            value_2,
            response[3],
            response[4],
            response[5],
        )
        login_success = True

user_interface_app = user_interface.UserInterfaceApp()
account_admin_interface_app = user_interface.AccountAdminInterfaceApp()

app_stack = [None]
if role == "user":
    app_stack.append(user_interface_app)

elif role == "account_admin":
    app_stack.append(account_admin_interface_app)


def construct_error_app(status_code: int | str, message: str):
    """Error app constructor function"""
    if "detail" in message:
        index = message.find("detail")
        start_index = index + 8
        message = message[start_index:-1]

    app = user_interface.ErrorApp()
    app.status_code = status_code
    app.message = message
    return app


def retry_response():
    """Refreshes the current access token"""
    global access_token
    return_object = req.refresh_access_token(refresh_token)
    if return_object[0] is False:
        return False

    else:
        access_token = return_object[1]
        return True


def manage_get_income():
    """Management Function to construct the get income app"""
    response = req.get_income(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_income(access_token=access_token)

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.GetIncomeApp()
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
        app = user_interface.GetIncomeApp()
        income_list, total_income = response[0], response[1]
        app.ROWS = income_list
        app.total_income = total_income
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_expenditure():
    """Management Function to construct the get expenditure app"""
    response = req.get_expenditure(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_expenditure(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.GetExpenditureApp()
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
        app = user_interface.GetExpenditureApp()
        expenditure_list, total_expenditure = response[0], response[1]
        app.ROWS = expenditure_list
        app.total_expenditure = total_expenditure
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_expense_type():
    """Management Function to get the expense types"""
    response = req.get_expense_type(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_expense_type(access_token=access_token)

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.GetExpenseTypeApp()
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
        app = user_interface.GetExpenseTypeApp()
        app.ROWS = response
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_get_users():
    """Management Function to get users."""
    response = req.get_users(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_users(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.GetUsersApp()
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
        app = user_interface.GetUsersApp()
        app.ROWS = response
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_income(income, payment_method):
    """Management function to add income."""
    response = req.add_income(
        amount=income, method=payment_method, access_token=access_token
    )
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.add_income(
                    amount=income, method=payment_method, access_token=access_token
                )

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = user_interface.AddIncomeApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = user_interface.AddIncomeApp()
        return app

    elif not response:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_logout():
    """Management function to handle user logout."""
    response = req.logout(access_token=access_token)

    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    return None


def manage_add_expenditure(amount, expense):
    """Management function to add expenditure."""
    response = req.create_expenditure(
        amount=amount, expense=expense, access_token=access_token
    )
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.create_expenditure(
                    amount=amount, expense=expense, access_token=access_token
                )

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = user_interface.AddExpenditureApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = user_interface.AddExpenditureApp()
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_expense_type(expense_type):
    """Management function to add expense types."""
    response = req.create_expense_type(
        expense_type=expense_type, access_token=access_token
    )
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.create_expense_type(
                    expense_type=expense_type, access_token=access_token
                )
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is True:
                    app = user_interface.AddExpenseTypeApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif response is True:
        app = user_interface.AddExpenseTypeApp()
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_add_user(email, user_name, phone, password, role):
    """Management function to add user."""
    response = req.create_user(
        email=email,
        user_name=user_name,
        phone=phone,
        password=password,
        role=role,
        access_token=access_token,
    )

    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.create_user(
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
                    app = user_interface.AddUserApp()
                    return app

                else:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is dict:
        app = user_interface.AddUserApp()
        return app

    else:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app


def manage_update_income(income=None, trans_id=None):
    """Management function used to update income."""
    response = req.get_income(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_income(access_token=access_token)

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is None:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

                elif type(response) is list:
                    app = user_interface.UpdateIncomeApp()
                    app.ROWS = response[0]

                    if income is None and trans_id is None:
                        return app

                    update_response = req.update_income(
                        amount=income, id=trans_id, access_token=access_token
                    )
                    if type(update_response) is tuple:
                        if update_response[1] == 401:
                            refreshed_access_token = retry_response()
                            if not refreshed_access_token:
                                app = construct_error_app(
                                    update_response[1], update_response[2]
                                )
                                return app

                            elif refreshed_access_token:
                                update_response = req.update_income(
                                    amount=income,
                                    id=trans_id,
                                    access_token=access_token,
                                )
                                if type(update_response) is tuple:
                                    app = construct_error_app(response[1], response[2])
                                    return app

                                elif update_response is True:
                                    new_response = req.get_income(
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
                        new_response = req.get_income(access_token=access_token)
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
        app = user_interface.UpdateIncomeApp()
        app.ROWS = response[0]

        if income is None or trans_id is None:
            return app

        update_response = req.update_income(
            amount=income, id=trans_id, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response()
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = req.update_income(
                        amount=income, id=trans_id, access_token=access_token
                    )
                    if type(update_response) is tuple:
                        app = construct_error_app(response[1], response[2])
                        return app

                    elif update_response is True:
                        new_response = req.get_income(access_token=access_token)
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
            new_response = req.get_income(access_token=access_token)
            app.ROWS = new_response[0]
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_update_expenditure(amount=None, expense=None, expend_id=None):
    """Management function used to update expenditure"""
    response = req.get_expenditure(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_expenditure(access_token=access_token)

                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif response is None:
                    app = construct_error_app(
                        status_code=409, message="Could not process request"
                    )
                    return app

                elif type(response) is list:
                    app = user_interface.UpdateExpenditureApp()
                    app.ROWS = response[0]
                    if amount is None or expense is None or expend_id is None:
                        return app

                    update_response = req.update_expenditure(
                        id=expend_id,
                        amount=amount,
                        expense=expense,
                        access_token=access_token,
                    )
                    if type(update_response) is tuple:
                        if update_response[1] == 401:
                            refreshed_access_token = retry_response()
                            if not refreshed_access_token:
                                app = construct_error_app(
                                    update_response[1], update_response[2]
                                )
                                return app

                            elif refreshed_access_token:
                                update_response = req.update_expenditure(
                                    id=expend_id,
                                    amount=amount,
                                    expense=expense,
                                    access_token=access_token,
                                )

                                if type(update_response) is tuple:
                                    app = construct_error_app(response[1], response[2])
                                    return app

                                elif update_response is True:
                                    new_response = req.get_expenditure(
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
                        new_response = req.get_expenditure(access_token=access_token)
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
        app = user_interface.UpdateExpenditureApp()
        app.ROWS = response[0]
        if amount is None or expense is None or expend_id is None:
            return app

        update_response = req.update_expenditure(
            id=expend_id, amount=amount, expense=expense, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response()
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = req.update_expenditure(
                        id=expend_id,
                        amount=amount,
                        expense=expense,
                        access_token=access_token,
                    )

                    if type(update_response) is tuple:
                        app = construct_error_app(response[1], response[2])
                        return app

                    elif update_response is True:
                        new_response = req.get_expenditure(access_token=access_token)
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
            new_response = req.get_expenditure(access_token=access_token)
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


def manage_update_expense_type(expense_type=None, expense_id=None):
    """Management function to update expense types"""
    response = req.get_expense_type(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_expense_type(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.UpdateExpenseTypeApp()
                    app.ROWS = response
                    if expense_type is None or expense_id is None:
                        return app

                    update_response = req.update_expense_type(
                        id=expense_id,
                        expense_type=expense_type,
                        access_token=access_token,
                    )
                    if type(update_response) is tuple:
                        if update_response[1] == 401:
                            refreshed_access_token = retry_response()
                            if not refreshed_access_token:
                                app = construct_error_app(
                                    update_response[1], update_response[2]
                                )
                                return app

                            elif refreshed_access_token:
                                update_response = req.update_expense_type(
                                    id=expense_id,
                                    expense_type=expense_type,
                                    access_token=access_token,
                                )
                                if type(update_response) is tuple:
                                    app = construct_error_app(response[1], response[2])
                                    return app

                                elif update_response:
                                    new_response = req.get_expense_type(
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
                            update_response[1], update_response[2]
                        )
                        return app

                    elif update_response:
                        new_response = req.get_expense_type(access_token=access_token)
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
        app = user_interface.UpdateExpenseTypeApp()
        app.ROWS = response
        if expense_type is None or expense_id is None:
            return app

        update_response = req.update_expense_type(
            id=expense_id, expense_type=expense_type, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response()
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = req.update_expense_type(
                        id=expense_id,
                        expense_type=expense_type,
                        access_token=access_token,
                    )
                    if type(update_response) is tuple:
                        app = construct_error_app(response[1], response[2])
                        return app

                    elif update_response:
                        new_response = req.get_expense_type(access_token=access_token)
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
            new_response = req.get_expense_type(access_token=access_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_update_user_role(user_name=None, role=None):
    """Management function to update user role"""
    response = req.get_users(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_users(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.UpdateUserRoleApp()
                    app.ROWS = response

                    if user_name is None or role is None:
                        return app

                    update_response = req.update_user_role(
                        user_name=user_name, role=role, access_token=access_token
                    )
                    if type(update_response) is tuple:
                        if update_response[1] == 401:
                            refreshed_access_token = retry_response()
                            if not refreshed_access_token:
                                app = construct_error_app(
                                    update_response[1], update_response[2]
                                )
                                return app

                            elif refreshed_access_token:
                                update_response = req.update_user_role(
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
                                    new_response = req.get_users(
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
                        new_response = req.get_users(access_token=access_token)
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
        app = user_interface.UpdateUserRoleApp()
        app.ROWS = response

        if user_name is None or role is None:
            return app

        update_response = req.update_user_role(
            user_name=user_name, role=role, access_token=access_token
        )
        if type(update_response) is tuple:
            if update_response[1] == 401:
                refreshed_access_token = retry_response()
                if not refreshed_access_token:
                    app = construct_error_app(update_response[1], update_response[2])
                    return app

                elif refreshed_access_token:
                    update_response = req.update_user_role(
                        user_name=user_name, role=role, access_token=access_token
                    )

                    if type(update_response) is tuple:
                        app = construct_error_app(
                            update_response[1], update_response[2]
                        )
                        return app

                    elif update_response:
                        new_response = req.get_users(access_token=access_token)
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
            new_response = req.get_users(access_token=access_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


def manage_delete_user(user_name=None):
    """Management function to delete user"""
    response = req.get_users(access_token=access_token)
    if type(response) is tuple:
        if response[1] == 401:
            refreshed_access_token = retry_response()
            if not refreshed_access_token:
                app = construct_error_app(response[1], response[2])
                return app

            elif refreshed_access_token:
                response = req.get_users(access_token=access_token)
                if type(response) is tuple:
                    app = construct_error_app(response[1], response[2])
                    return app

                elif type(response) is list:
                    app = user_interface.DeleteUserApp()
                    app.ROWS = response

                    if user_name is None:
                        return app

                    delete_response = req.delete_user(
                        user_name=user_name, access_token=access_token
                    )
                    if type(delete_response) is tuple:
                        if delete_response[1] == 401:
                            refreshed_access_token = retry_response()
                            if not refreshed_access_token:
                                app = construct_error_app(
                                    delete_response[1], delete_response[2]
                                )
                                return app

                            elif refreshed_access_token:
                                delete_response = req.delete_user(
                                    user_name=user_name, access_token=access_token
                                )

                                if type(delete_response) is tuple:
                                    app = construct_error_app(
                                        delete_response[1], delete_response[2]
                                    )
                                    return app

                                elif delete_response:
                                    new_response = req.get_users(
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
                        new_response = req.get_users(access_token=access_token)
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
        app = user_interface.DeleteUserApp()
        app.ROWS = response

        if user_name is None:
            return app

        delete_response = req.delete_user(
            user_name=user_name, access_token=access_token
        )
        if type(delete_response) is tuple:
            if delete_response[1] == 401:
                refreshed_access_token = retry_response()
                if not refreshed_access_token:
                    app = construct_error_app(delete_response[1], delete_response[2])
                    return app

                elif refreshed_access_token:
                    delete_response = req.delete_user(
                        user_name=user_name, access_token=access_token
                    )

                    if type(delete_response) is tuple:
                        app = construct_error_app(
                            delete_response[1], delete_response[2]
                        )
                        return app

                    elif delete_response:
                        new_response = req.get_users(access_token=access_token)
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
            new_response = req.get_users(access_token=access_token)
            app.ROWS = new_response
            return app

        else:
            app = construct_error_app(
                status_code=409, message="Could not process request"
            )
            return app


# Running the app stack

if app_stack[-1] is not None:
    if app_stack[-1].name == "account_admin_interface_app":
        while app_stack:
            app = app_stack.pop()

            if app is None:
                break

            response = app.run()

            if app.name == "account_admin_interface_app":
                if response == "income":
                    new_app = user_interface.IncomeMenuApp()
                    app_stack.append(new_app)

                elif response == "expenditure":
                    new_app = user_interface.ExpenditureMenuApp()
                    app_stack.append(new_app)

                elif response == "expense_type":
                    new_app = user_interface.ExpenseTypeMenuApp()
                    app_stack.append(new_app)

                elif response == "account":
                    new_app = user_interface.AccountMenuApp()
                    app_stack.append(new_app)

                elif response == "logout":  ### To be changed
                    new_app = manage_logout()
                    app_stack.pop()
                    break

            elif app.name == "error_app":
                if response == "back":
                    app_stack.append(user_interface.AccountAdminInterfaceApp())

            elif app.name == "income_menu_app":
                if response == "add_income":
                    new_app = user_interface.AddIncomeApp()
                    app_stack.append(new_app)

                elif response == "get_income":
                    new_app = manage_get_income()
                    app_stack.append(new_app)

                elif response == "update_income":
                    new_app = manage_update_income()
                    app_stack.append(new_app)

                elif response == "back":
                    app_stack.append(user_interface.AccountAdminInterfaceApp())

            elif app.name == "expenditure_menu_app":
                if response == "add_expend":
                    new_app = user_interface.AddExpenditureApp()
                    app_stack.append(new_app)

                elif response == "get_expend":
                    new_app = manage_get_expenditure()
                    app_stack.append(new_app)

                elif response == "update_expend":
                    new_app = manage_update_expenditure()
                    app_stack.append(new_app)

                elif response == "back":
                    app_stack.append(user_interface.AccountAdminInterfaceApp())

            elif app.name == "expense_type_menu_app":
                if response == "add_expense":
                    new_app = user_interface.AddExpenseTypeApp()
                    app_stack.append(new_app)

                elif response == "get_expense":
                    new_app = manage_get_expense_type()
                    app_stack.append(new_app)

                elif response == "update_expense":
                    new_app = manage_update_expense_type()
                    app_stack.append(new_app)

                elif response == "back":
                    app_stack.append(user_interface.AccountAdminInterfaceApp())

            elif app.name == "add_income_app":
                if response == "back":
                    app_stack.append(user_interface.IncomeMenuApp())

                elif type(response) is tuple:
                    income, method = response[0], response[1]
                    new_app = manage_add_income(income=income, payment_method=method)
                    app_stack.append(new_app)

            elif app.name == "get_income_app":
                if response == "back":
                    app_stack.append(user_interface.IncomeMenuApp())

            elif app.name == "update_income_app":
                if response == "back":
                    app_stack.append(user_interface.IncomeMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_income(response[0], response[1])
                    print(response[0], response[1])
                    app_stack.append(new_app)

            elif app.name == "add_expenditure_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenditureMenuApp())

                elif type(response) is tuple:
                    new_app = manage_add_expenditure(response[0], response[1])
                    app_stack.append(new_app)

            elif app.name == "get_expenditure_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenditureMenuApp())

            elif app.name == "update_expenditure_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenditureMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_expenditure(
                        response[0], response[2], response[1]
                    )
                    app_stack.append(new_app)

            elif app.name == "add_expense_type_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenseTypeMenuApp())

                elif type(response) is str:
                    new_app = manage_add_expense_type(response)
                    app_stack.append(new_app)

            elif app.name == "get_expense_type_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenseTypeMenuApp())

            elif app.name == "update_expense_type_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenseTypeMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_expense_type(
                        expense_type=response[1], expense_id=response[0]
                    )
                    app_stack.append(new_app)

            elif app.name == "account_menu_app":
                if response == "back":
                    app_stack.append(user_interface.AccountAdminInterfaceApp())

                elif response == "get_users":
                    new_app = manage_get_users()
                    app_stack.append(new_app)

                elif response == "update_user_role":
                    new_app = manage_update_user_role()
                    app_stack.append(new_app)

                elif response == "delete_user":
                    new_app = manage_delete_user()
                    app_stack.append(new_app)

                elif response == "add_user":
                    new_app = user_interface.AddUserApp()
                    app_stack.append(new_app)

            elif app.name == "add_user_app":
                if response == "back":
                    app_stack.append(user_interface.AccountMenuApp())

                elif type(response) is tuple:
                    new_app = manage_add_user(
                        response[0], response[1], response[2], response[3], response[4]
                    )
                    app_stack.append(new_app)

            elif app.name == "get_users_app":
                if response == "back":
                    app_stack.append(user_interface.AccountMenuApp())

            if app.name == "update_user_role_app":
                if response == "back":
                    app_stack.append(user_interface.AccountMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_user_role(response[0], response[1])
                    app_stack.append(new_app)

            if app.name == "delete_user_app":
                if response == "back":
                    app_stack.append(user_interface.AccountMenuApp())

                elif type(response) is str:
                    new_app = manage_delete_user(response)
                    app_stack.append(new_app)

    elif app_stack[-1].name == "user_interface_app":
        while app_stack:
            app = app_stack.pop()

            if app is None:
                break

            response = app.run()

            if app.name == "user_interface_app":
                if response == "income":
                    new_app = user_interface.IncomeMenuApp()
                    app_stack.append(new_app)

                elif response == "expenditure":
                    new_app = user_interface.ExpenditureMenuApp()
                    app_stack.append(new_app)

                elif response == "expense_type":
                    new_app = user_interface.ExpenseTypeMenuApp()
                    app_stack.append(new_app)

                elif response == "logout":  ### To be changed
                    app_stack.pop()
                    new_app = manage_logout()
                    app_stack.append(new_app)
                    break

            elif app.name == "error_app":
                if response == "back":
                    app_stack.append(user_interface.UserInterfaceApp())

            elif app.name == "income_menu_app":
                if response == "add_income":
                    new_app = user_interface.AddIncomeApp()
                    app_stack.append(new_app)

                elif response == "get_income":
                    new_app = manage_get_income()
                    app_stack.append(new_app)

                elif response == "update_income":
                    new_app = manage_update_income()
                    app_stack.append(new_app)

                elif response == "back":
                    app_stack.append(user_interface.UserInterfaceApp())

            elif app.name == "expenditure_menu_app":
                if response == "add_expend":
                    new_app = user_interface.AddExpenditureApp()
                    app_stack.append(new_app)

                elif response == "get_expend":
                    new_app = manage_get_expenditure()
                    app_stack.append(new_app)

                elif response == "update_expend":
                    new_app = manage_update_expenditure()
                    app_stack.append(new_app)

                elif response == "back":
                    app_stack.append(user_interface.UserInterfaceApp())

            elif app.name == "expense_type_menu_app":
                if response == "add_expense":
                    new_app = user_interface.AddExpenseTypeApp()
                    app_stack.append(new_app)

                elif response == "get_expense":
                    new_app = manage_get_expense_type()
                    app_stack.append(new_app)

                elif response == "update_expense":
                    new_app = manage_update_expense_type()
                    app_stack.append(new_app)

                elif response == "back":
                    app_stack.append(user_interface.UserInterfaceApp())

            elif app.name == "add_income_app":
                if response == "back":
                    app_stack.append(user_interface.IncomeMenuApp())

                elif type(response) is tuple:
                    income, method = response[0], response[1]
                    new_app = manage_add_income(income=income, payment_method=method)
                    app_stack.append(new_app)

            elif app.name == "get_income_app":
                if response == "back":
                    app_stack.append(user_interface.IncomeMenuApp())

            elif app.name == "update_income_app":
                if response == "back":
                    app_stack.append(user_interface.IncomeMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_income(response[0], response[1])
                    app_stack.append(new_app)

            elif app.name == "add_expenditure_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenditureMenuApp())

                elif type(response) is tuple:
                    new_app = manage_add_expenditure(response[0], response[1])
                    app_stack.append(new_app)

            elif app.name == "get_expenditure_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenditureMenuApp())

            elif app.name == "update_expenditure_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenditureMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_expenditure(
                        response[0], response[2], response[1]
                    )
                    app_stack.append(new_app)

            elif app.name == "add_expense_type_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenseTypeMenuApp())

                elif type(response) is str:
                    new_app = manage_add_expense_type(response)
                    app_stack.append(new_app)

            elif app.name == "get_expense_type_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenseTypeMenuApp())

            elif app.name == "update_expense_type_app":
                if response == "back":
                    app_stack.append(user_interface.ExpenseTypeMenuApp())

                elif type(response) is tuple:
                    new_app = manage_update_expense_type(
                        expense_type=response[1], expense_id=response[0]
                    )
                    app_stack.append(new_app)
