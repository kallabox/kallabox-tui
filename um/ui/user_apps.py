from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Static,
    Input,
    Label,
)


class Login(Static):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Label("Account"),
                Input("", placeholder="Enter your account name", id="account_name"),
            ),
            Horizontal(
                Label("User Name"),
                Input(
                    "",
                    placeholder="Enter your username",
                    id="user_name",
                ),
            ),
            Horizontal(
                Label("Password"),
                Input("", placeholder="Enter your password", id="password"),
            ),
        )


class LoginPageApp(App):
    account_name = reactive(str)
    user_name = reactive(str)
    password = reactive(str)
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 13;
        }

        Input {
    width: 60;
    padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Login()
        yield Button(label="Login!", variant="success", id="login")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "login":
            self.exit((self.account_name, self.user_name, self.password))

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "user_name":
                self.user_name = component

            elif event.input.id == "password":
                self.password = component

            elif event.input.id == "account_name":
                self.account_name = component


class UserInterfaceApp(App):
    name = reactive("user_interface_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 13;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Income", variant="default", id="income")
        yield Button(label="Expenditure", variant="primary", id="expenditure")
        yield Button(label="Expense Type", variant="success", id="expense_type")
        yield Button(label="Logout", variant="error", id="logout")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "income":
            self.exit("income")

        elif event.button.id == "expenditure":
            self.exit("expenditure")

        elif event.button.id == "expense_type":
            self.exit("expense_type")

        elif event.button.id == "logout":
            self.exit("logout")


class AccountAdminInterfaceApp(App):
    name = "account_admin_interface_app"
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 30;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Income", variant="default", id="income")
        yield Button(label="Expenditure", variant="primary", id="expenditure")
        yield Button(label="Expense Type", variant="success", id="expense_type")
        yield Button(label="Account", variant="warning", id="account")
        yield Button(label="Logout", variant="error", id="logout")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "income":
            self.exit("income")

        elif event.button.id == "expenditure":
            self.exit("expenditure")

        elif event.button.id == "expense_type":
            self.exit("expense_type")

        elif event.button.id == "account":
            self.exit("account")

        elif event.button.id == "logout":
            self.exit("logout")


class ErrorApp(App):
    status_code = reactive(int)
    message = reactive(str)
    name = reactive("error_app")
    CSS = """
        Button {
        width: 20;
        }

        Label {
        width: 30;
        }
    """

    def compose(self) -> ComposeResult:
        yield Label("Error")
        yield Label(f"Status Code : {self.status_code}")
        yield Label(f"Detail : {self.message}")
        yield Button(label="Back", variant="success", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")
