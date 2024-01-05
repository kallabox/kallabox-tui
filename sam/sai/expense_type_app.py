from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
)


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
