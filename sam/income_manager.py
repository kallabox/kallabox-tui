import sam.sai.income_app as income_app
import sam.sai.interface_app as interface_app
import sam.sar.income_requests as income_requests


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


def manage_get_income(signup_token: str):
    """Management function to get income."""
    response = income_requests.get_income_sa(signup_token=signup_token)
    if type(response) is tuple:
        app = construct_error_app(response[1], response[2])
        return app

    elif type(response) is list:
        app = income_app.SAGetIncomeApp()
        income_list = response[0]
        total_income = response[1]
        app.ROWS = income_list
        app.total_income = total_income
        return app

    elif response is None:
        app = construct_error_app(status_code=409, message="Could not process request")
        return app
