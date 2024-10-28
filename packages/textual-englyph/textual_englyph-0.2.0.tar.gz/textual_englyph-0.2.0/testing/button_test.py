from textual_englyph import EnGlyph
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Vertical

class Test(App):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button( "Button" )
            yield EnGlyph("+")
            yield EnGlyph("Hello Textual!", basis=(2,3), pips=True)
            yield EnGlyph("=")
            yield Button( str(EnGlyph("Hello Textual!", basis=(2,3), pips=True )) )

if __name__ == "__main__":
    Test().run()
