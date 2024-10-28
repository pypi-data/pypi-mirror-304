'''Boilerplate code for testing purposes'''
from textual.app import App, ComposeResult
from textual_englyph import EnGlyph

class Test(App):
    '''Test CSS and console markup styling the basic englyph use case'''
    DEFAULT_CSS = """
    EnGlyph {
        color: green;
        text-style: underline;
        }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyph("Hello [blue]Textual!")

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
