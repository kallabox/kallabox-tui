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


class IncomeMenuApp(App):
    name = reactive("income_menu_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 30;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Add Income", variant="default", id="add_income")
        yield Button(label="Get Income", variant="primary", id="get_income")
        yield Button(label="Update Income", variant="success", id="update_income")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_income":
            self.exit("add_income")

        elif event.button.id == "get_income":
            self.exit("get_income")

        elif event.button.id == "update_income":
            self.exit("update_income")

        elif event.button.id == "back":
            self.exit("back")


class ExpenditureMenuApp(App):
    name = "expenditure_menu_app"
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 30;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Add Expenditure", variant="default", id="add_expend")
        yield Button(label="Get Expenditure", variant="primary", id="get_expend")
        yield Button(label="Update Expenditure", variant="success", id="update_expend")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_expend":
            self.exit("add_expend")

        elif event.button.id == "get_expend":
            self.exit("get_expend")

        elif event.button.id == "update_expend":
            self.exit("update_expend")

        elif event.button.id == "back":
            self.exit("back")


class ExpenseTypeMenuApp(App):
    name = reactive("expense_type_menu_app")
    CSS = """
        Button {
        width: 30;
        }

        Label {
        width: 30;
        }
    """

    def compose(self) -> ComposeResult:
        yield Button(label="Add Expense Type", variant="default", id="add_expense")
        yield Button(label="Get Expense Type", variant="primary", id="get_expense")
        yield Button(
            label="Update Expense Type", variant="success", id="update_expense"
        )
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_expense":
            self.exit("add_expense")

        elif event.button.id == "get_expense":
            self.exit("get_expense")

        elif event.button.id == "update_expense":
            self.exit("update_expense")

        elif event.button.id == "back":
            self.exit("back")


class AddIncome(Static):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("Amount"),
            Input(
                "", placeholder="Enter the income as a positive integer", id="income"
            ),
        )


class AddIncomeApp(App):
    income = reactive(int)
    name = reactive("add_income_app")
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
        yield AddIncome()
        yield Button(label="Cash", variant="success", id="cash")
        yield Button(label="UPI", variant="default", id="upi")
        yield Button(label="POS", variant="primary", id="pos")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cash":
            self.exit((self.income, "Cash"))

        elif event.button.id == "upi":
            self.exit((self.income, "UPI"))

        elif event.button.id == "pos":
            self.exit((self.income, "POS"))

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "income":
                self.income = component


class GetIncomeApp(App):
    ROWS = reactive(list)
    total_income = reactive(str)
    name = reactive("get_income_app")
    CSS = """
    DataTable {
        width: 150;
        padding: 2;
        }

        Label {
    width: 60;
    padding: 1;
    }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Label(f"Total Income is {self.total_income}")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")


class UpdateIncomeApp(App):
    ROWS = reactive(list)
    name = "update_income_app"
    row_number = reactive(int)
    amount = reactive(int)
    trans_id = reactive(str)
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
                Label("S.No"),
                Input(
                    "",
                    placeholder="Enter the Serial Number of Income to be updated",
                    id="row_number",
                ),
            ),
            Horizontal(
                Label("Amount"),
                Input(
                    "",
                    placeholder="Enter the Amount as a Positive Integer",
                    id="amount",
                ),
            ),
        )
        yield Button(label="Update", variant="success", id="update_income")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update_income":
            self.trans_id = self.ROWS[int(self.row_number)][3]
            self.exit((self.amount, self.trans_id))

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "row_number":
                self.row_number = component

            elif event.input.id == "amount":
                self.amount = component


class AddExpenditure(Static):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Label("Amount"),
                Input(
                    "",
                    placeholder="Enter the expenditure as a positive integer",
                    id="expend",
                ),
            ),
            Horizontal(
                Label("Expense"),
                Input(
                    "",
                    placeholder="Enter the expense (e.g. coffee, tea, etc.)",
                    id="expense",
                ),
            ),
        )


class AddExpenditureApp(App):
    amount = reactive(int)
    expense = reactive(str)
    name = reactive("add_expenditure_app")
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
        yield AddExpenditure()
        yield Button(label="Add", variant="success", id="add_expend")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_expend":
            self.exit((self.amount, self.expense))

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "expend":
                self.amount = component

            elif event.input.id == "expense":
                self.expense = component


class GetExpenditureApp(App):
    ROWS = reactive(list)
    total_expenditure = reactive(str)
    name = reactive("get_expenditure_app")
    CSS = """
    DataTable {
        width: 175;
        padding: 2;
        }

        Label {
    width: 60;
    padding: 1;
    }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Label(f"Total Expenditure is {self.total_expenditure}")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.exit("back")


class UpdateExpenditureApp(App):
    ROWS = reactive(list)
    name = reactive("update_expenditure_app")
    row_number = reactive(int)
    amount = reactive(int)
    expense = reactive(str)
    expense_id = reactive(str)
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

    Button {
        width: 30;
        }
"""

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Vertical(
            Horizontal(
                Label("S.No"),
                Input(
                    "",
                    placeholder="Enter the Serial Number of the Expenditure to be Updated",
                    id="row_number",
                ),
            ),
            Horizontal(
                Label("Amount"),
                Input(
                    "",
                    placeholder="Enter the amount as a positive integer",
                    id="amount",
                ),
            ),
            Horizontal(
                Label("Expense"),
                Input(
                    "",
                    placeholder="Enter the expense (e.g. coffee, tea, etc.)",
                    id="expense",
                ),
            ),
        )
        yield Button(label="Update", variant="success", id="update_expense")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update_expense":
            self.expense_id = self.ROWS[int(self.row_number)][3]
            self.exit((self.amount, self.expense_id, self.expense))

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "row_number":
                self.row_number = component

            elif event.input.id == "amount":
                self.amount = component

            elif event.input.id == "expense":
                self.expense = component


class AddExpenseType(Static):
    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("Expense Type"),
            Input(
                "",
                placeholder="Enter the expense type (e.g. coffee, tea, etc.)",
                id="expense_type",
            ),
        )


class AddExpenseTypeApp(App):
    expense_type = reactive(str)
    name = reactive("add_expense_type_app")
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
        yield AddExpenseType()
        yield Button(label="Add", variant="success", id="add_expense_type")
        yield Button(label="Back", variant="error", id="back")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_expense_type":
            self.exit(self.expense_type)

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "expense_type":
                self.expense_type = component


class GetExpenseTypeApp(App):
    ROWS = reactive(list)
    name = reactive("get_expense_type_app")
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


class UpdateExpenseTypeApp(App):
    ROWS = reactive(list)
    name = reactive("update_expense_type_app")
    row_number = reactive(int)
    expense_type = reactive(str)
    expense_type_id = reactive(str)
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
                Label("S.No"),
                Input(
                    "",
                    placeholder="Enter the Serial Number of the Expense Type to be updated",
                    id="row_number",
                ),
            ),
            Horizontal(
                Label("Expense Type"),
                Input(
                    "",
                    placeholder="Enter the expense type (e.g. coffee, tea, etc.)",
                    id="expense",
                ),
            ),
        )
        yield Button(label="Update", variant="success", id="update_expense")
        yield Button(label="Back", variant="error", id="back")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.ROWS[0])
        table.add_rows(self.ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update_expense":
            self.expense_type_id = self.ROWS[int(self.row_number)][3]
            self.exit((self.expense_type_id, self.expense_type))

        elif event.button.id == "back":
            self.exit("back")

    def on_input_changed(self, event: Input.Changed):
        try:
            component = str(event.value)

        except ValueError:
            raise ValueError

        else:
            if event.input.id == "row_number":
                self.row_number = component

            elif event.input.id == "expense":
                self.expense_type = component


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
