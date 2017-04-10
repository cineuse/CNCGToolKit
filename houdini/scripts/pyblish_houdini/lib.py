# Standard library
import os
import sys
import contextlib

# Pyblish libraries
import pyblish.api

# Host libraries
import hou

# Local libraries
from . import plugins

self = sys.modules[__name__]
self._has_been_setup = False
self._registered_gui = None


def setup(console=False, port=None):
    """Setup integration

    Register plug-ins and integrate into the host

    Arguments:
        console (bool): DEPRECATED
        port (int, optional): DEPRECATED

    """

    if self._has_been_setup:
        teardown()

    register_plugins()
    register_host()

    self._has_been_setup = True
    print("pyblish: Pyblish loaded successfully.")


def show():
    """Try showing the most desirable GUI

    This function cycles through the currently registered
    graphical user interfaces, if any, and presents it to
    the user.

    """

    return (_discover_gui() or _show_no_gui)()


def _discover_gui():
    """Return the most desirable of the currently registered GUIs"""

    # Prefer last registered
    guis = reversed(pyblish.api.registered_guis())

    for gui in guis:
        try:
            gui = __import__(gui).show
        except (ImportError, AttributeError):
            continue
        else:
            return gui


def teardown():
    """Remove integration"""
    if not self._has_been_setup:
        return

    deregister_plugins()
    deregister_host()

    self._has_been_setup = False
    print("pyblish: Integration torn down successfully")


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("hython")
    pyblish.api.register_host("hpython")
    pyblish.api.register_host("houdini")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)


def deregister_host():
    pyblish.api.deregister_host("hpython")
    pyblish.api.deregister_host("houdini")


def deregister_plugins():
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.deregister_plugin_path(plugin_path)


@contextlib.contextmanager
def maintained_selection():
    """Maintain selection during context

    Example:
        >>> with maintained_selection():
        ...     # Modify selection
        ...     node.setSelected(on=False, clear_all_selected=True)
        >>> # Selection restored

    """

    previous_selection = hou.selectedNodes()
    try:
        yield
    finally:
        if previous_selection:
            for node in previous_selection:
                node.setSelected(on=True)
        else:
            for node in previous_selection:
                node.setSelected(on=False)


def _show_no_gui():
    """Popup with information about how to register a new GUI

    In the event of no GUI being registered or available,
    this information dialog will appear to guide the user
    through how to get set up with one.

    """

    try:
        from .vendor.Qt import QtWidgets, QtGui
    except ImportError:
        raise ImportError("Pyblish requires either PySide or PyQt bindings.")

    messagebox = QtWidgets.QMessageBox()
    messagebox.setIcon(messagebox.Warning)
    messagebox.setWindowIcon(QtGui.QIcon(os.path.join(
        os.path.dirname(pyblish.__file__),
        "icons",
        "logo-32x32.svg"))
    )

    spacer = QtWidgets.QWidget()
    spacer.setMinimumSize(400, 0)
    spacer.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                         QtWidgets.QSizePolicy.Expanding)

    layout = messagebox.layout()
    layout.addWidget(spacer, layout.rowCount(), 0, 1, layout.columnCount())

    messagebox.setWindowTitle("Uh oh")
    messagebox.setText("No registered GUI found.")

    if not pyblish.api.registered_guis():
        messagebox.setInformativeText(
            "In order to show you a GUI, one must first be registered. "
            "Press \"Show details...\" below for information on how to "
            "do that.")

        messagebox.setDetailedText(
            "Pyblish supports one or more graphical user interfaces "
            "to be registered at once, the next acting as a fallback to "
            "the previous."
            "\n"
            "\n"
            "For example, to use Pyblish Lite, first install it:"
            "\n"
            "\n"
            "$ pip install pyblish-lite"
            "\n"
            "\n"
            "Then register it, like so:"
            "\n"
            "\n"
            ">>> import pyblish.api\n"
            ">>> pyblish.api.register_gui(\"pyblish_lite\")"
            "\n"
            "\n"
            "The next time you try running this, Lite will appear."
            "\n"
            "See http://api.pyblish.com/register_gui.html for "
            "more information.")

    else:
        messagebox.setInformativeText(
            "None of the registered graphical user interfaces "
            "could be found."
            "\n"
            "\n"
            "Press \"Show details\" for more information.")

        messagebox.setDetailedText(
            "These interfaces are currently registered."
            "\n"
            "%s" % "\n".join(pyblish.api.registered_guis()))

    messagebox.setStandardButtons(messagebox.Ok)
    messagebox.exec_()
