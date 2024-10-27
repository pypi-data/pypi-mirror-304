from PySide6.QtWidgets import QDialog

from fluentui.widgets import LineEdit
from src.fluentui.widgets import Application, Widget

if __name__ == '__main__':
    print('---------------------')
    app = Application()

    w = Widget()
    edit = QDialog(w)

    print(w.children())
    print(edit.parentWidget())

    # f = ScrollArea(hor_scroll_bar_policy=)

    w.show()
    app.exec()
