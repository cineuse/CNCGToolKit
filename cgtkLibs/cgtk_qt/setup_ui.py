# coding=utf8
import os

# Set preferred binding
os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(['PySide', 'PyQt4'])

from Qt import QtWidgets, load_ui


def setup_ui(uifile, base_instance=None):
    """Load a Qt Designer .ui file and returns an instance of the user interface
    Args:
        uifile (str): Absolute path to .ui file
        base_instance (QWidget): The widget into which UI widgets are loaded
    Returns:
        QWidget: the base instance
    """
    ui = load_ui(uifile)  # Qt.py mapped function
    if not base_instance:
        return ui
    else:
        for member in dir(ui):
            if not member.startswith('__') and \
               member is not 'staticMetaObject':
                setattr(base_instance, member, getattr(ui, member))
        return ui


if __name__ == "__main__":
    pass
