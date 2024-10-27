from typing import Callable

from PySide6.QtCore import Qt, Signal, QMetaMethod
from PySide6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLayout, QSizePolicy

from ..core import ObjectMix
from ..gui import Font


class WidgetMix(ObjectMix):
    on_close = Signal()
    on_key_enter_pressed = Signal()
    on_clicked = Signal(QWidget, QMouseEvent)

    def __init__(
            # a、b、c、d、e、f、g、h、i、j、k、l、m、n、o、p、q、r、s、t、u、v、w、x、y、z
            self, *args,
            attrs: Qt.WidgetAttribute | set[Qt.WidgetAttribute | set[Qt.WidgetAttribute]] = None,
            drop_shadow_effect: QGraphicsDropShadowEffect = None,
            font: Font = None,
            layout: QLayout = None,
            mouse_tracking: bool = None,
            parent: QWidget = None,

            size: tuple[int, int] | int = None,
            width: int | str = None,
            height: int | str = None,
            fixed_size: tuple[int, int] | int = None,
            fixed_width: int = None,
            fixed_height: int = None,

            row_span: int = 1,
            column_span: int = 1,
            self_align=Qt.AlignmentFlag(0),

            win_title='',
            win_flags: Qt.WindowType = None,

            closed: Callable = None,
            clicked: Callable[[QWidget], QMouseEvent] = None,
            key_enter_pressed: Callable = None,
            **kwargs
    ):
        self.__is_pressed = False
        self.row_span = row_span
        self.column_span = column_span
        self.self_align = self_align

        super().__init__(parent=parent, *args, **kwargs)
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
        if layout is not None:
            self.setLayout(layout)

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
                    w: int | str = None,
                    h: int | str = None,
                    fixed_size: tuple[int, int] | int = None,
                    fixed_w: int = None,
                    fixed_h: int = None
                    ):
        if isinstance(w, str) or isinstance(h, str):
            policy = self.sizePolicy()
            if w is not None:
                policy.setHorizontalPolicy(QSizePolicy.Policy.MinimumExpanding)
            if h is not None:
                policy.setVerticalPolicy(QSizePolicy.Policy.MinimumExpanding)
            self.setSizePolicy(policy)

        if size is not None:
            if isinstance(size, int): size = (size, size)
            self.resize(*size)
        elif isinstance(w, int) or isinstance(h, int):
            self.resize(w or self.width(), h or self.height())

        if fixed_size is not None:
            if isinstance(fixed_size, int): fixed_size = (fixed_size, fixed_size)
            self.setFixedSize(fixed_size)
        elif isinstance(fixed_w, int) or isinstance(fixed_h, int):
            if fixed_w is not None and fixed_h is not None:
                self.setFixedSize(fixed_w, fixed_h)
            elif fixed_w is not None:
                self.setFixedWidth(fixed_w)
            elif fixed_h is not None:
                self.setFixedHeight(fixed_h)


class Widget(WidgetMix, QWidget):
    ...
