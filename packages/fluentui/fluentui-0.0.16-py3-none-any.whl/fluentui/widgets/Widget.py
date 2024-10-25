from typing import Callable

from PySide6.QtCore import Qt, Signal, QMetaMethod
from PySide6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLayout

from .layout import Layout
from ..core import ObjectMix
from ..gui import Font

if (__widget := object) is None:
    __widget = QWidget


class WidgetMix(ObjectMix, Layout, __widget):
    on_close = Signal()
    on_key_enter_pressed = Signal()
    on_clicked = Signal(QWidget, QMouseEvent)

    def __init__(
            # a、b、c、d、e、f、g、h、i、j、k、l、m、n、o、p、q、r、s、t、u、v、w、x、y、z
            self, *args,
            attrs: Qt.WidgetAttribute | set[Qt.WidgetAttribute | set[Qt.WidgetAttribute]] = None,
            children: QLayout = None,
            drop_shadow_effect: QGraphicsDropShadowEffect = None,
            font: Font = None,
            key='',
            mouse_tracking: bool = None,
            parent: QWidget = None,

            size: tuple[int, int] | int = None,
            width: int = None,
            height: int = None,
            fixed_size: tuple[int, int] | int = None,
            fixed_width: int = None,
            fixed_height: int = None,

            win_title='',
            win_flags: Qt.WindowType = None,

            closed: Callable = None,
            clicked: Callable[[QWidget], QMouseEvent] = None,
            key_enter_pressed: Callable = None,
            **kwargs
    ):
        self.__is_pressed = False

        super().__init__(parent=parent, *args, **kwargs)
        self.setObjectName(key)
        self.setWindowTitle(win_title)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        if closed: self.on_close.connect(closed)
        if clicked: self.on_clicked.connect(clicked)
        if key_enter_pressed: self.on_key_enter_pressed.connect(key_enter_pressed)

        if font is not None: self.setFont(font)
        if win_flags is not None: self.setWindowFlags(win_flags)
        if mouse_tracking is not None: self.setMouseTracking(mouse_tracking)
        if drop_shadow_effect is not None: self.setGraphicsEffect(drop_shadow_effect)

        if attrs is not None:
            for x in attrs if isinstance(attrs, set) else {attrs}:
                if isinstance(x, set):
                    for a in x: self.setAttribute(a, False)
                    continue
                self.setAttribute(x)

        self.__init_size(size, width, height, fixed_size, fixed_width, fixed_height)
        if children is not None:
            self.setLayout(children)

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)
        self.on_close.emit()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        if e.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.on_key_enter_pressed.emit()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.__is_pressed = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        super().mouseReleaseEvent(e)
        if self.__is_pressed:
            self.__is_pressed = False
            if self.isSignalConnected(QMetaMethod.fromSignal(self.on_clicked)):
                self.on_clicked.emit(self, e)

    def __init_size(self, size: tuple[int, int] | int = None,
                    width: int = None,
                    height: int = None,
                    fixed_size: tuple[int, int] | int = None,
                    fixed_width: int = None,
                    fixed_height: int = None
                    ):
        if size is not None:
            if isinstance(size, int): size = (size, size)
            self.resize(*size)
        elif all(x is not None for x in (width, height)):
            self.resize(width, height)
        elif width is not None:
            self.resize(width, self.height())
        elif height is not None:
            self.resize(self.width(), height)

        if fixed_size is not None:
            if isinstance(fixed_size, int): fixed_size = (fixed_size, fixed_size)
            self.setFixedSize(fixed_size)
        elif all(x is not None for x in (fixed_width, fixed_height)):
            self.setFixedSize(fixed_width, fixed_height)
        elif fixed_width is not None:
            self.setFixedWidth(fixed_width)
        elif fixed_height is not None:
            self.setFixedHeight(fixed_height)


class Widget(WidgetMix, QWidget):
    ...
