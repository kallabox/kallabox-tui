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
