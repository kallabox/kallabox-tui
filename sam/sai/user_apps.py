from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Input,
    Label,
    DataTable,
)


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
