from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import Reactive, reactive
from textual.widgets import Input, Label, Static

from posting.collection import RequestModel
from posting.widgets.text_area import PostingTextArea
from posting.widgets.variable_input import VariableInput


class RequestMetadata(VerticalScroll):
    DEFAULT_CSS = """
    RequestMetadata {
        padding: 0 2;
        & Input {
            width: 1fr;
            margin-bottom: 1;
        }
        & PostingTextArea {
            max-height: 3;
            margin-bottom: 1;
        }
        & Button {
            dock: bottom;
            width: 1fr;
        }
        & #request-path {
            color: $text-muted;
        }
    }
    """

    request: Reactive[RequestModel | None] = reactive(None, init=False)

    def watch_request(self, request: RequestModel | None) -> None:
        """When the request changes, update the form."""
        if request is None:
            self.request_name_input.value = ""
            self.request_description_textarea.text = ""
            self.request_path_label.update("")
        else:
            self.request_name_input.value = request.name or ""
            self.request_description_textarea.text = request.description
            self.request_path_label.update(str(request.path) or "")

    def compose(self) -> ComposeResult:
        self.can_focus = False
        yield Label("Name [dim]optional[/dim]")
        yield VariableInput(placeholder="Enter a name...", id="name-input")
        yield Label("Description [dim]optional[/dim]")
        yield PostingTextArea(id="description-textarea")

        yield Static("", id="request-path")

    @property
    def request_name_input(self) -> Input:
        return self.query_one("#name-input", Input)

    @property
    def request_description_textarea(self) -> PostingTextArea:
        return self.query_one("#description-textarea", PostingTextArea)

    @property
    def request_path_label(self) -> Static:
        return self.query_one("#request-path", Static)

    @property
    def request_name(self) -> str:
        return self.request_name_input.value

    @property
    def description(self) -> str:
        return self.request_description_textarea.text
