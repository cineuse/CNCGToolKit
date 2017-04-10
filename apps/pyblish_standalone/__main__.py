import os
import sys
import argparse

import executable
import pyblish_standalone


def cli():
    parser = argparse.ArgumentParser(prog="pyblish_standalone")

    parser.add_argument("file", nargs="?",
                        help="Pass file to Context as `currentFile`")
    parser.add_argument("-d", "--data", nargs=2, action="append",
                        metavar=("key", "value"),
                        help=("Append data to context, "
                              "can be called multiple times."))
    parser.add_argument("--path", action="append",
                        help=("Append path to PYBLISHPLUGINPATH, "
                              "can be called multiple times"))
    parser.add_argument("-rh", "--register-host", action="append",
                        help=("Register host name before "
                              "starting the Pyblish."))
    parser.add_argument("-rg", "--register-gui", action="append",
                        help=("Validates and uses the gui name "
                              "in the order specified."))
    parser.add_argument("--debug", action="store_true",
                        help=("Registers mock plugins for debugging."))

    kwargs = parser.parse_args(sys.argv[1:])

    # Store reference to keyword arguments, for Collection
    pyblish_standalone.kwargs = kwargs.__dict__

    plugins_path = os.path.join(os.path.dirname(__file__), "plugins")

    pyblish_path = os.environ.get("PYBLISHPLUGINPATH", "").split(os.pathsep)
    pyblish_path.append(plugins_path)
    pyblish_path.extend(kwargs.path or [])

    os.environ["PYBLISHPLUGINPATH"] = os.pathsep.join(pyblish_path)

    # debug mode
    if kwargs.debug:
        from . import mock
        import pyblish.api

        for Plugin in mock.plugins:
            pyblish.api.register_plugin(Plugin)

        print "Enter debug mode..."

    # collect hosts passed
    hosts = kwargs.__dict__["register_host"]
    if not hosts:
        hosts = []

    # register guis
    gui = None
    guis = []
    try:
        for g in kwargs.register_gui:
            gui = __import__(g)
            guis.append(g)
    except:
        import traceback
        print traceback.format_exc()
        pass

    if gui:
        print "Found gui: %s" % gui
    else:
        print "No valid guis registered in: %s" % guis
        return

    executable.start(gui, hosts=hosts)


if __name__ == "__main__":
    cli()
    executable.stop()
