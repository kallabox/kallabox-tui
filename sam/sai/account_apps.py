from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Static,
    Input,
    Label,
    DataTable,
)


class SuperAdminAccountInterfaceApp(App):
    name = reactive("super_admin_account_interface_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        padding-top: 10;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Get Accounts", variant="primary", id="get_accounts")
        yield Button(label="Create Account", variant="success", id="create_account")
        yield Button(label="Delete Account", variant="warning", id="delete_account")
        yield Button(label="Purge Account", variant="default", id="purge_account")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")

        elif event.button.id == "create_account":
            self.exit("create_account")

        elif event.button.id == "delete_account":
            self.exit("delete_account")

        elif event.button.id == "purge_account":
            self.exit("purge_account")

        elif event.button.id == "get_accounts":
            self.exit("get_accounts")


class SACreateAccount(Static):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Label("Account Name"),
                Input(
                    "",
                    placeholder="Enter the account name (must start with lowercase and only contain alphanumeric characters)",
                    id="account_name",
                ),
            ),
            Horizontal(
                Label("User Name"),
                Input("", placeholder="Enter the user name", id="user_name"),
            ),
            Horizontal(
                Label("Email"),
                Input("", placeholder="Enter the email address", id="email"),
            ),
            Horizontal(
                Label("Phone"),
                Input(
                    "",
                    placeholder="Enter the phone number (must contain only integers)",
                    id="phone",
                ),
            ),
            Horizontal(
                Label("Password"),
                Input("", placeholder="Enter the password", id="password"),
            ),
        )


class SACreateAccountApp(App):
    name = reactive("super_admin_create_account_app")
    account_name = reactive(str)
    user_name = reactive(str)
    email = reactive(str)
    phone = reactive(str)
    password = reactive(str)

    CSS = """
    Button {
    width: 20;
    }

    Label {
    width: 15;
    padding: 1;
    }

    Input {
    width: 60;
    padding: 1;
    }
"""

    def compose(self) -> ComposeResult:
        yield SACreateAccount()
        yield Button(label="Create Account", variant="success", id="create_account")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "create_account":
            self.exit(
                (
                    self.account_name,
                    self.user_name,
                    self.email,
                    self.phone,
                    self.password,
                )
            )

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "email":
                self.email = component

            elif event.input.id == "password":
                self.password = component

            elif event.input.id == "account_name":
                self.account_name = component

            elif event.input.id == "user_name":
                self.user_name = component

            elif event.input.id == "phone":
                self.phone = component


class SAPurgeAccountApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_purge_account_app")
    account_name = reactive(str)
    CSS = """
        DataTable {
        width: 175;
        padding: 2;
        }

        Label {
    width: 20;
    padding: 1;
    }

    Input {
    width: 60;
    padding: 1;
    }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Vertical(
            Horizontal(
                Label("Account Name"),
                Input("", placeholder="Enter the Account Name", id="account_name"),
            ),
        )
        yield Button(label="Delete", variant="warning", id="purge_account")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "purge_account":
            self.exit(self.account_name)

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "account_name":
                self.account_name = component


class SADeleteAccountApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_delete_account_app")
    account_name = reactive(str)
    CSS = """
        DataTable {
        width: 175;
        padding: 2;
        }

        Label {
    width: 20;
    padding: 1;
    }

    Input {
    width: 60;
    padding: 1;
    }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Vertical(
            Horizontal(
                Label("Account Name"),
                Input("", placeholder="Enter the Account Name", id="account_name"),
            ),
        )
        yield Button(label="Delete", variant="warning", id="delete_account")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "delete_account":
            self.exit(self.account_name)

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "account_name":
                self.account_name = component


class SAGetAccountsApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_get_accounts_app")
    CSS = """
        DataTable {
        width: 150;
        padding: 2;
        }

"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")
