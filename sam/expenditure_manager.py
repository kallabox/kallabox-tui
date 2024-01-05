import sam.sai.expenditure_app as expenditure_app
import sam.sai.interface_app as interface_app
import sam.sar.expenditure_requests as expenditure_requests


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


def manage_get_expenditure(signup_token: str):
    """Management function to get expenditures"""
    response = expenditure_requests.get_expenditure_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = expenditure_app.SAGetExpenditureApp()
        expenditure_list = response[0]
        total_expenditure = response[1]
        app.ROWS = expenditure_list
        app.total_expenditure = total_expenditure
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app
