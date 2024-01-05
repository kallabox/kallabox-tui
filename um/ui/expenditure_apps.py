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
