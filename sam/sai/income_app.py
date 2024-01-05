from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Label,
    DataTable,
)


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
