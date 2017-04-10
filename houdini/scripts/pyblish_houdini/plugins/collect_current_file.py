import pyblish.api

import hou


class CollectCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context"""

    label = "Current File"
    hosts = ["houdini"]
    order = pyblish.api.CollectorOrder

    def process(self, context):
        """inject the current working file"""
        context.data["currentFile"] = hou.hipFile.path()
