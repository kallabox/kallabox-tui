from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Label,
)


class SuperAdminInterfaceApp(App):
    name = reactive("super_admin_interface_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        padding-top: 10;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Account", variant="success", id="account")
        yield Button(label="User", variant="default", id="user")
        yield Button(label="Get Income", variant="primary", id="get_income")
        yield Button(label="Get Expenditure", variant="warning", id="get_expenditure")
        yield Button(label="Get Expense Types", variant="error", id="get_expense_types")
        yield Label("Press Ctrl + C to quit")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "account":
            self.exit("account")

        elif event.button.id == "user":
            self.exit("user")

        elif event.button.id == "get_income":
            self.exit("get_income")

        elif event.button.id == "get_expenditure":
            self.exit("get_expenditure")

        elif event.button.id == "get_expense_types":
            self.exit("get_expense_types")


class ErrorApp(App):
    status_code = reactive(int)
    message = reactive(str)
    name = reactive("error_app")
    CSS = """
        Button {
        width: 20;
        }

        Label {
        padding-top: 6;
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
