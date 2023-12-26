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


class SuperAdminUserInterfaceApp(App):
    name = reactive("super_admin_user_interface_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        padding-top: 10;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Get Users", variant="primary", id="get_users")
        yield Button(label="Update User Role", variant="success", id="update_user_role")
        yield Button(label="Delete User", variant="default", id="delete_user")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")

        elif event.button.id == "update_user_role":
            self.exit("update_user_role")

        elif event.button.id == "delete_user":
            self.exit("delete_user")

        elif event.button.id == "get_users":
            self.exit("get_users")


class SAUpdateUserRoleApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_update_user_role_app")
    user_name = reactive(str)
    account_name = reactive(str)
    role = reactive(str)
    CSS = """
        DataTable {
        width: 105;
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
                Label("User Name"),
                Input("", placeholder="Enter the User Name", id="user_name"),
            ),
            Horizontal(
                Label("Account Name"),
                Input("", placeholder="Enter the account name", id="account_name"),
            ),
            Horizontal(
                Label("Role"),
                Input(
                    "",
                    placeholder="Enter the role for the user (user or account_admin)",
                    id="role",
                ),
            ),
        )
        yield Button(label="Update", variant="success", id="update_user_role")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update_user_role":
            self.exit((self.user_name, self.account_name, self.role))

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

            elif event.input.id == "role":
                self.role = component

            elif event.input.id == "user_name":
                self.user_name = component


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


class SADeleteUserApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_delete_user_app")
    account_name = reactive(str)
    user_name = reactive(str)
    CSS = """
        DataTable {
        width: 105;
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
            Horizontal(
                Label("User Name"),
                Input("", placeholder="Enter the User Name", id="user_name"),
            ),
        )
        yield Button(label="Delete", variant="warning", id="delete_user")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "delete_user":
            self.exit((self.account_name, self.user_name))

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "user_name":
                self.user_name = component

            elif event.input.id == "account_name":
                self.account_name = component


class SAPurgeAccountApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_purge_account_app")
    account_name = reactive(str)
    CSS = """
        DataTable {
        width: 105;
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
        width: 105;
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


class SAGetUsersApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_get_users_app")
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


class SAGetIncomeApp(App):
    ROWS = reactive(list)
    total_income = reactive(str)
    name = reactive("super_admin_get_income_app")
    CSS = """
        DataTable {
        width: 150;
        padding: 2;
        }

        Label {
    width: 60;
    padding: 2;
    }

"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Label(f"Total income is {self.total_income}")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")


class SAGetExpenditureApp(App):
    ROWS = reactive(list)
    total_expenditure = reactive(str)
    name = reactive("super_admin_get_expenditure_app")
    CSS = """
        DataTable {
        width: 175;
        padding: 2;
        }

        Label {
    width: 50;
    padding: 2;
    }

"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Label(f"Total expenditure is {self.total_expenditure}")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")


class SAGetExpenseTypeApp(App):
    ROWS = reactive(list)
    name = reactive("super_admin_get_expense_type_app")
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
