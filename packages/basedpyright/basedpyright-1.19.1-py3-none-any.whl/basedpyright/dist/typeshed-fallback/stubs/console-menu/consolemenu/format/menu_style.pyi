from consolemenu.format.menu_borders import MenuBorderStyle as MenuBorderStyle, MenuBorderStyleFactory as MenuBorderStyleFactory
from consolemenu.format.menu_margins import MenuMargins as MenuMargins
from consolemenu.format.menu_padding import MenuPadding as MenuPadding

class MenuStyle:
    def __init__(
        self,
        margins: MenuMargins | None = None,
        padding: MenuPadding | None = None,
        border_style: MenuBorderStyle | None = None,
        border_style_type: int | None = None,
        border_style_factory: MenuBorderStyleFactory | None = None,
    ) -> None: ...
    @property
    def margins(self) -> MenuMargins: ...
    @margins.setter
    def margins(self, margins: MenuMargins) -> None: ...
    @property
    def padding(self) -> MenuPadding: ...
    @padding.setter
    def padding(self, padding: MenuPadding) -> None: ...
    @property
    def border_style(self) -> MenuBorderStyle: ...
    @border_style.setter
    def border_style(self, border_style: MenuBorderStyle) -> None: ...
    @property
    def border_style_factory(self) -> MenuBorderStyleFactory: ...
    @border_style_factory.setter
    def border_style_factory(self, border_style_factory: MenuBorderStyleFactory) -> None: ...
