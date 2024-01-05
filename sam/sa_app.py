import sam.sai.interface_app as interface_app
import sam.sai.account_apps as account_apps
import sam.sai.user_apps as user_apps
import sam.account_manager as account_manager
import sam.user_manager as user_manager
import sam.expenditure_manager as expenditure_manager
import sam.expense_type_manager as expense_type_manager
import sam.income_manager as income_manager
from sam.req_service_token import req_get_service_token


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


signup_token = req_get_service_token()
if signup_token is None:
    new_app = construct_error_app(status_code="", message="Token not found")
    new_app.run()

else:
    new_app = interface_app.SuperAdminInterfaceApp()


app_stack = [None, new_app]


def service_mode():
    """Function that calls the kallabox api in service mode."""
    while app_stack:
        app = app_stack.pop()

        if app is None:
            break

        response = app.run()

        if app.name == "super_admin_interface_app":
            if response == "user":
                new_app = user_apps.SuperAdminUserInterfaceApp()
                app_stack.append(new_app)

            elif response == "account":
                new_app = account_apps.SuperAdminAccountInterfaceApp()
                app_stack.append(new_app)

            elif response == "get_income":
                new_app = income_manager.manage_get_income(signup_token=signup_token)
                app_stack.append(new_app)

            elif response == "get_expenditure":
                new_app = expenditure_manager.manage_get_expenditure(
                    signup_token=signup_token
                )
                app_stack.append(new_app)

            elif response == "get_expense_types":
                new_app = expense_type_manager.manage_get_expense_types(
                    signup_token=signup_token
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_account_interface_app":
            if response == "back":
                new_app = interface_app.SuperAdminInterfaceApp()
                app_stack.append(new_app)

            elif response == "get_accounts":
                new_app = account_manager.manage_get_accounts(signup_token=signup_token)
                app_stack.append(new_app)

            elif response == "create_account":
                new_app = account_apps.SACreateAccountApp()
                app_stack.append(new_app)

            elif response == "delete_account":
                new_app = account_manager.manage_delete_account(
                    account_name=None, signup_token=signup_token
                )
                app_stack.append(new_app)

            elif response == "purge_account":
                new_app = account_manager.manage_purge_account(
                    account_name=None, signup_token=signup_token
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_user_interface_app":
            if response == "back":
                new_app = interface_app.SuperAdminInterfaceApp()
                app_stack.append(new_app)

            elif response == "update_user_role":
                new_app = user_manager.manage_update_user_role(
                    account_name=None,
                    user_name=None,
                    role=None,
                    signup_token=signup_token,
                )
                app_stack.append(new_app)

            elif response == "delete_user":
                new_app = user_manager.manage_delete_user(
                    account_name=None, user_name=None, signup_token=signup_token
                )
                app_stack.append(new_app)

            elif response == "get_users":
                new_app = user_manager.manage_get_users(signup_token=signup_token)
                app_stack.append(new_app)

        elif app.name == "super_admin_update_user_role_app":
            if response == "back":
                new_app = user_apps.SuperAdminUserInterfaceApp()
                app_stack.append(new_app)

            elif type(response) is tuple:
                user_name, account_name, role = response[0], response[1], response[2]
                new_app = user_manager.manage_update_user_role(
                    account_name=account_name,
                    user_name=user_name,
                    role=role,
                    signup_token=signup_token,
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_delete_user_app":
            if response == "back":
                new_app = user_apps.SuperAdminUserInterfaceApp()
                app_stack.append(new_app)

            elif type(response) is tuple:
                account_name, user_name = response[0], response[1]
                new_app = user_manager.manage_delete_user(
                    account_name=account_name,
                    user_name=user_name,
                    signup_token=signup_token,
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_get_users_app":
            if response == "back":
                new_app = user_apps.SuperAdminUserInterfaceApp()
                app_stack.append(new_app)

        elif app.name == "super_admin_get_accounts_app":
            if response == "back":
                new_app = account_apps.SuperAdminAccountInterfaceApp()
                app_stack.append(new_app)

        elif app.name == "super_admin_create_account_app":
            if response == "back":
                new_app = account_apps.SuperAdminAccountInterfaceApp()
                app_stack.append(new_app)

            elif type(response) is tuple:
                account_name, user_name, email, phone, password = (
                    response[0],
                    response[1],
                    response[2],
                    response[3],
                    response[4],
                )
                new_app = account_manager.manage_create_account(
                    account_name=account_name,
                    user_name=user_name,
                    email=email,
                    phone=phone,
                    password=password,
                    signup_token=signup_token,
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_delete_account_app":
            if response == "back":
                new_app = account_apps.SuperAdminAccountInterfaceApp()
                app_stack.append(new_app)

            else:
                account_name = response
                new_app = account_manager.manage_delete_account(
                    account_name=account_name, signup_token=signup_token
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_purge_account_app":
            if response == "back":
                new_app = account_apps.SuperAdminAccountInterfaceApp()
                app_stack.append(new_app)

            else:
                account_name = response
                new_app = account_manager.manage_purge_account(
                    account_name=account_name, signup_token=signup_token
                )
                app_stack.append(new_app)

        elif app.name == "super_admin_get_income_app":
            if response == "back":
                new_app = interface_app.SuperAdminInterfaceApp()
                app_stack.append(new_app)

        elif app.name == "super_admin_get_expenditure_app":
            if response == "back":
                new_app = interface_app.SuperAdminInterfaceApp()
                app_stack.append(new_app)

        elif app.name == "super_admin_get_expense_type_app":
            if response == "back":
                new_app = interface_app.SuperAdminInterfaceApp()
                app_stack.append(new_app)

        elif app.name == "error_app":
            if response == "back":
                new_app = interface_app.SuperAdminInterfaceApp()
                app_stack.append(new_app)
