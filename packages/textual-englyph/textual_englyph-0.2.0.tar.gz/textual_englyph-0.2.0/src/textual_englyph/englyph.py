'''Create large text output module for Textual with custom widget EnGlyph'''
# pylint: disable=R0913
# would greatly increase complexity in optional widget control
from textual.strip import Strip
from textual.widget import Widget

from rich.console import RenderableType
from rich.text import Text

from .toglyxels import ToGlyxels

class EnGlyph( Widget, inherit_bindings=False ):
    '''
    Textual widget to show a variety of large text outputs.

    Args:
        renderable: Rich renderable or string to display
        basis: cell glyph pixel in (x,y) tuple partitions
        pips: show glyph pixels (glyxels) in reduced density
        markup: Rich Text inline console styling bool, default is True
        name: Standard Textual Widget argument
        id: Standard Textual Widget argument
        classes: Standard Textual Widget argument
        disabled: Standard Textual Widget argument
    '''

    DEFAULT_CSS = """
    EnGlyph {
        height: auto;
        width: auto;
    }
    """

    def __init__( self,
                 renderable: RenderableType = "",
                 *,
                 basis = (2,4),
                 pips = False,
                 markup: bool = True,
                 name: str | None = None,
                 id = None,
                 classes: str | None = None,
                 disabled: bool = False,
                 ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.markup = markup
        self.basis = basis
        self.pips = pips
        self._enrender( renderable )
        #self.rich_style is not settled yet, trigger regenerate _strip_cache later
        self._encache()
        self._renderable = None

    def get_content_width(self,
                          container=None,
                          viewport=None):
        return self._strips_cache[0].cell_length

    def get_content_height(self,
                           container=None,
                           viewport=None,
                           width=None):
        return len( self._strips_cache )

    def _encache(self) -> None:
        self.renderable.stylize_before( self.rich_style )
        self._renderable = self.renderable
        self._strips_cache = ToGlyxels.from_renderable( self.renderable, self.basis, self.pips )

    def _enrender(self, renderable: RenderableType|None = None) -> None:
        if renderable is not None:
            self.renderable = renderable
            if isinstance(renderable, str):
                if self.markup:
                    self.renderable = Text.from_markup(renderable)
                else:
                    self.renderable = Text(renderable)

    def update( self,
               renderable: RenderableType|None = None,
               basis: tuple|None = None,
               pips: bool|None = None ) -> None:
        """New display input"""
        self.basis = basis or self.basis
        self.pips = pips or self.pips
        self._enrender( renderable )
        self._encache()
        self.refresh(layout=True)

    def render_line( self, y:int ) -> Strip:
        strip = Strip.blank(0)
        if self._renderable != self.renderable:
            self._encache()
        if y < self.get_content_height():
            strip = self._strips_cache[y]
        return strip

    def __str__(self) -> str:
        output = []
        for strip in self._strips_cache:
            output.append( strip.text )
        return "\n".join( output )
