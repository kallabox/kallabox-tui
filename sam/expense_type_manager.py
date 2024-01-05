import sam.sai.expense_type_app as expense_type_app
import sam.sai.interface_app as interface_app
import sam.sar.expense_type_requests as expense_type_requests


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


def manage_get_expense_types(signup_token: str):
    """Manangement function to get expense types"""
    response = expense_type_requests.get_expense_types_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = expense_type_app.SAGetExpenseTypeApp()
        app.ROWS = response
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app
