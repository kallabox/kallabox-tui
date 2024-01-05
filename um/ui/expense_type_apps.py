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
