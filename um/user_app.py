import um.ui.user_apps as user_apps
import um.ui.income_apps as income_apps
import um.ui.expense_type_apps as expense_type_apps
import um.ui.expenditure_apps as expenditure_apps
import um.ui.account_apps as account_apps

import um.ur.user_requests as user_requests
import um.ur.authentication as authentication

import um.user_manager as user_manager
import um.income_manager as income_manager
import um.expense_type_manager as expense_type_manager
import um.expenditure_manager as expenditure_manager


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
    global access_token
    return_object = user_requests.refresh_access_token(refresh_token)
    if return_object[0] is False:
        return False

    else:
        access_token = return_object[1]
        return True


def manage_logout():
    """Management function to handle user logout."""
    response = authentication.logout(access_token=access_token)

    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    return None


refresh_token, access_token, account_id, user_id, role = None, None, None, None, None


def user_mode():
    """Function that calls the kallabox api in user mode."""
    login_success = False
    while not login_success:
        app = user_apps.LoginPageApp()
        reply = app.run()
        account_name, user_name, password = reply[0], reply[1], reply[2]
        response = authentication.login(
            account_name=account_name, user_name=user_name, password=password
        )
        boolean, value_1, value_2 = response[0], response[1], response[2]

        if not boolean:
            continue

        elif boolean:
            global refresh_token, access_token, account_id, user_id, role
            refresh_token, access_token, account_id, user_id, role = (
                value_1,
                value_2,
                response[3],
                response[4],
                response[5],
            )
            login_success = True

    user_interface_app = user_apps.UserInterfaceApp()
    account_admin_interface_app = user_apps.AccountAdminInterfaceApp()

    app_stack = [None]
    if role == "user":
        app_stack.append(user_interface_app)

    elif role == "account_admin":
        app_stack.append(account_admin_interface_app)

    if app_stack[-1] is not None:
        if app_stack[-1].name == "account_admin_interface_app":
            while app_stack:
                app = app_stack.pop()

                if app is None:
                    break

                response = app.run()

                if app.name == "account_admin_interface_app":
                    if response == "income":
                        new_app = income_apps.IncomeMenuApp()
                        app_stack.append(new_app)

                    elif response == "expenditure":
                        new_app = expenditure_apps.ExpenditureMenuApp()
                        app_stack.append(new_app)

                    elif response == "expense_type":
                        new_app = expense_type_apps.ExpenseTypeMenuApp()
                        app_stack.append(new_app)

                    elif response == "account":
                        new_app = account_apps.AccountMenuApp()
                        app_stack.append(new_app)

                    elif response == "logout":  ### To be changed
                        new_app = manage_logout()
                        app_stack.pop()
                        break

                elif app.name == "error_app":
                    if response == "back":
                        app_stack.append(user_apps.AccountAdminInterfaceApp())

                elif app.name == "income_menu_app":
                    if response == "add_income":
                        new_app = income_apps.AddIncomeApp()
                        app_stack.append(new_app)

                    elif response == "get_income":
                        new_app = income_manager.manage_get_income(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_income":
                        new_app = income_manager.manage_update_income(
                            income=None,
                            trans_id=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "back":
                        app_stack.append(user_apps.AccountAdminInterfaceApp())

                elif app.name == "expenditure_menu_app":
                    if response == "add_expend":
                        new_app = expenditure_apps.AddExpenditureApp()
                        app_stack.append(new_app)

                    elif response == "get_expend":
                        new_app = expenditure_manager.manage_get_expenditure(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_expend":
                        new_app = expenditure_manager.manage_update_expenditure(
                            amount=None,
                            expense=None,
                            expend_id=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "back":
                        app_stack.append(user_apps.AccountAdminInterfaceApp())

                elif app.name == "expense_type_menu_app":
                    if response == "add_expense":
                        new_app = expense_type_apps.AddExpenseTypeApp()
                        app_stack.append(new_app)

                    elif response == "get_expense":
                        new_app = expense_type_manager.manage_get_expense_type(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_expense":
                        new_app = expense_type_manager.manage_update_expense_type(
                            expense_type=None,
                            expense_id=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "back":
                        app_stack.append(user_apps.AccountAdminInterfaceApp())

                elif app.name == "add_income_app":
                    if response == "back":
                        app_stack.append(income_apps.IncomeMenuApp())

                    elif type(response) is tuple:
                        income, method = response[0], response[1]
                        new_app = income_manager.manage_add_income(
                            income=income,
                            payment_method=method,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_income_app":
                    if response == "back":
                        app_stack.append(income_apps.IncomeMenuApp())

                elif app.name == "update_income_app":
                    if response == "back":
                        app_stack.append(income_apps.IncomeMenuApp())

                    elif type(response) is tuple:
                        income, trans_id = response[0], response[1]
                        new_app = income_manager.manage_update_income(
                            income=income,
                            trans_id=trans_id,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "add_expenditure_app":
                    if response == "back":
                        app_stack.append(expenditure_apps.ExpenditureMenuApp())

                    elif type(response) is tuple:
                        amount, expense = response[0], response[1]
                        new_app = expenditure_manager.manage_add_expenditure(
                            amount=amount,
                            expense=expense,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_expenditure_app":
                    if response == "back":
                        app_stack.append(expenditure_apps.ExpenditureMenuApp())

                elif app.name == "update_expenditure_app":
                    if response == "back":
                        app_stack.append(expenditure_apps.ExpenditureMenuApp())

                    elif type(response) is tuple:
                        amount, expense, expend_id = (
                            response[0],
                            response[2],
                            response[1],
                        )
                        new_app = expenditure_manager.manage_update_expenditure(
                            amount=amount,
                            expense=expense,
                            expend_id=expend_id,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "add_expense_type_app":
                    if response == "back":
                        app_stack.append(expense_type_apps.ExpenseTypeMenuApp())

                    elif type(response) is str:
                        expense_type = response
                        new_app = expense_type_manager.manage_add_expense_type(
                            expense_type=expense_type,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_expense_type_app":
                    if response == "back":
                        app_stack.append(expense_type_apps.ExpenseTypeMenuApp())

                elif app.name == "update_expense_type_app":
                    if response == "back":
                        app_stack.append(expense_type_apps.ExpenseTypeMenuApp())

                    elif type(response) is tuple:
                        expense_id, expense_type = response[0], response[1]
                        new_app = expense_type_manager.manage_update_expense_type(
                            expense_type=expense_type,
                            expense_id=expense_id,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "account_menu_app":
                    if response == "back":
                        app_stack.append(user_apps.AccountAdminInterfaceApp())

                    elif response == "get_users":
                        new_app = user_manager.manage_get_users(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_user_role":
                        new_app = user_manager.manage_update_user_role(
                            user_name=None,
                            role=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "delete_user":
                        new_app = user_manager.manage_delete_user(
                            user_name=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "add_user":
                        new_app = account_apps.AddUserApp()
                        app_stack.append(new_app)

                elif app.name == "add_user_app":
                    if response == "back":
                        app_stack.append(account_apps.AccountMenuApp())

                    elif type(response) is tuple:
                        email, user_name, phone, password, role = (
                            response[0],
                            response[1],
                            response[2],
                            response[3],
                            response[4],
                        )
                        new_app = user_manager.manage_add_user(
                            email=email,
                            user_name=user_name,
                            phone=phone,
                            password=password,
                            role=role,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_users_app":
                    if response == "back":
                        app_stack.append(account_apps.AccountMenuApp())

                if app.name == "update_user_role_app":
                    if response == "back":
                        app_stack.append(account_apps.AccountMenuApp())

                    elif type(response) is tuple:
                        user_name, role = response[0], response[1]
                        new_app = user_manager.manage_update_user_role(
                            user_name=user_name,
                            role=role,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                if app.name == "delete_user_app":
                    if response == "back":
                        app_stack.append(account_apps.AccountMenuApp())

                    elif type(response) is str:
                        user_name = response
                        new_app = user_manager.manage_delete_user(
                            user_name=user_name,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

        elif app_stack[-1].name == "user_interface_app":
            while app_stack:
                app = app_stack.pop()

                if app is None:
                    break

                response = app.run()

                if app.name == "user_interface_app":
                    if response == "income":
                        new_app = income_apps.IncomeMenuApp()
                        app_stack.append(new_app)

                    elif response == "expenditure":
                        new_app = expenditure_apps.ExpenditureMenuApp()
                        app_stack.append(new_app)

                    elif response == "expense_type":
                        new_app = expense_type_apps.ExpenseTypeMenuApp()
                        app_stack.append(new_app)

                    elif response == "logout":  ### To be changed
                        app_stack.pop()
                        new_app = manage_logout()
                        app_stack.append(new_app)
                        break

                elif app.name == "error_app":
                    if response == "back":
                        app_stack.append(user_apps.UserInterfaceApp())

                elif app.name == "income_menu_app":
                    if response == "add_income":
                        new_app = income_apps.AddIncomeApp()
                        app_stack.append(new_app)

                    elif response == "get_income":
                        new_app = income_manager.manage_get_income(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_income":
                        new_app = income_manager.manage_update_income(
                            income=None,
                            trans_id=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "back":
                        app_stack.append(user_apps.UserInterfaceApp())

                elif app.name == "expenditure_menu_app":
                    if response == "add_expend":
                        new_app = expenditure_apps.AddExpenditureApp()
                        app_stack.append(new_app)

                    elif response == "get_expend":
                        new_app = expenditure_manager.manage_get_expenditure(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_expend":
                        new_app = expenditure_manager.manage_update_expenditure(
                            amount=None,
                            expense=None,
                            expend_id=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "back":
                        app_stack.append(user_apps.UserInterfaceApp())

                elif app.name == "expense_type_menu_app":
                    if response == "add_expense":
                        new_app = expense_type_apps.AddExpenseTypeApp()
                        app_stack.append(new_app)

                    elif response == "get_expense":
                        new_app = expense_type_manager.manage_get_expense_type(
                            access_token=access_token, refresh_token=refresh_token
                        )
                        app_stack.append(new_app)

                    elif response == "update_expense":
                        new_app = expense_type_manager.manage_update_expense_type(
                            expense_type=None,
                            expense_id=None,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                    elif response == "back":
                        app_stack.append(user_apps.UserInterfaceApp())

                elif app.name == "add_income_app":
                    if response == "back":
                        app_stack.append(income_apps.IncomeMenuApp())

                    elif type(response) is tuple:
                        income, method = response[0], response[1]
                        new_app = income_manager.manage_add_income(
                            income=income,
                            payment_method=method,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_income_app":
                    if response == "back":
                        app_stack.append(income_manager.IncomeMenuApp())

                elif app.name == "update_income_app":
                    if response == "back":
                        app_stack.append(income_manager.IncomeMenuApp())

                    elif type(response) is tuple:
                        income, trans_id = response[0], response[1]
                        new_app = income_manager.manage_update_income(
                            income=income,
                            trans_id=trans_id,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "add_expenditure_app":
                    if response == "back":
                        app_stack.append(expenditure_apps.ExpenditureMenuApp())

                    elif type(response) is tuple:
                        amount, expense = response[0], response[1]
                        new_app = expenditure_manager.manage_add_expenditure(
                            amount=amount,
                            expense=expense,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_expenditure_app":
                    if response == "back":
                        app_stack.append(expenditure_apps.ExpenditureMenuApp())

                elif app.name == "update_expenditure_app":
                    if response == "back":
                        app_stack.append(expenditure_apps.ExpenditureMenuApp())

                    elif type(response) is tuple:
                        amount, expend_id, expense = (
                            response[0],
                            response[1],
                            response[2],
                        )
                        new_app = expenditure_manager.manage_update_expenditure(
                            amount=amount,
                            expense=expense,
                            expend_id=expend_id,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "add_expense_type_app":
                    if response == "back":
                        app_stack.append(expense_type_apps.ExpenseTypeMenuApp())

                    elif type(response) is str:
                        expense_type = response
                        new_app = expense_type_manager.manage_add_expense_type(
                            expense_type=expense_type,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)

                elif app.name == "get_expense_type_app":
                    if response == "back":
                        app_stack.append(expense_type_apps.ExpenseTypeMenuApp())

                elif app.name == "update_expense_type_app":
                    if response == "back":
                        app_stack.append(expense_type_apps.ExpenseTypeMenuApp())

                    elif type(response) is tuple:
                        expense_id, expense_type = response[0], response[1]
                        new_app = expense_type_manager.manage_update_expense_type(
                            expense_type=expense_type,
                            expense_id=expense_id,
                            access_token=access_token,
                            refresh_token=refresh_token,
                        )
                        app_stack.append(new_app)
