import time
import socket

import pyblish.api


def start(gui, hosts=[]):
    """ This starts the supplied gui.

    Loops through 5 attempts to show the gui, due to qml server nature.
    It also registers any hosts along with it self "standalone".

    Args:
        gui (module): Module that has a "show" method.
        hosts (list): List of host names to register before starting.
    """

    pyblish.api.register_host("standalone")
    for host in hosts:
        pyblish.api.register_host(host)

    max_tries = 5
    while True:
        try:
            time.sleep(0.5)
            gui.show()
        except socket.error as e:
            if max_tries <= 0:
                raise Exception("Couldn't run Pyblish QML: %s" % e)
            else:
                print("%s tries left.." % max_tries)
                max_tries -= 1
        else:
            break

    print("Launching Pyblish..")


def stop():
    """ Called when shutting down. """
    try:
        import pyblish_aftereffects
        pyblish_aftereffects.stop_server()
    except:
        pass
