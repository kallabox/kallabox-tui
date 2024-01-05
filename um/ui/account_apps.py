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


class AccountMenuApp(App):
    name = reactive("account_menu_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 30;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Add User", variant="default", id="add_user")
        yield Button(label="Get Users", variant="primary", id="get_users")
        yield Button(label="Update User Role", variant="success", id="update_user_role")
        yield Button(label="Delete User", variant="warning", id="delete_user")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_user":
            self.exit("add_user")

        elif event.button.id == "get_users":
            self.exit("get_users")

        elif event.button.id == "update_user_role":
            self.exit("update_user_role")

        elif event.button.id == "delete_user":
            self.exit("delete_user")

        elif event.button.id == "back":
            self.exit("back")


class AddUser(Static):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Label("Email"),
                Input(
                    "", placeholder="Enter the email address of the user", id="email"
                ),
            ),
            Horizontal(
                Label("User Name"),
                Input("", placeholder="Enter the username for user", id="user_name"),
            ),
            Horizontal(
                Label("Phone"),
                Input("", placeholder="Enter the phone number for user", id="phone"),
            ),
            Horizontal(
                Label("Password"),
                Input("", placeholder="Enter the password for the user", id="password"),
            ),
            Horizontal(
                Label("Role"),
                Input(
                    "", placeholder="Enter the role (user or account_admin)", id="role"
                ),
            ),
        )


class AddUserApp(App):
    name = reactive("add_user_app")
    email = reactive(str)
    user_name = reactive(str)
    phone = reactive(str)
    password = reactive(str)
    role = reactive(str)
    CSS = """
        Label {
    width: 20;
    padding: 1;
    }

    Input {
    width: 60;
    padding: 1;
    }

    Button {
        width: 30;
        }
"""

    def compose(self) -> ComposeResult:
        yield AddUser()
        yield Button(label="Add User", variant="success", id="add_user")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_user":
            self.exit(
                (self.email, self.user_name, self.phone, self.password, self.role)
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

            elif event.input.id == "user_name":
                self.user_name = component

            elif event.input.id == "phone":
                self.phone = component

            elif event.input.id == "role":
                self.role = component


class GetUsersApp(App):
    ROWS = reactive(list)
    name = reactive("get_users_app")
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


class UpdateUserRoleApp(App):
    ROWS = reactive(list)
    user_name = reactive(str)
    role = reactive(str)
    name = reactive("update_user_role_app")
    CSS = """
    DataTable {
        width: 150;
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

    Button {
        width: 30;
        }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Vertical(
            Horizontal(
                Label("User Name"),
                Input("", placeholder="Enter the user name", id="user_name"),
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
            self.exit((self.user_name, self.role))

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

            elif event.input.id == "role":
                self.role = component


class DeleteUserApp(App):
    ROWS = reactive(list)
    user_name = reactive(str)
    name = reactive("delete_user_app")
    CSS = """
    DataTable {
        width: 150;
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

    Button {
        width: 30;
        }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Vertical(
            Horizontal(
                Label("User Name"),
                Input("", placeholder="Enter the username", id="user_name"),
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
            self.exit(self.user_name)

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
