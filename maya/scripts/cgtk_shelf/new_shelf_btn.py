# coding=utf8
# Copyright (c) 2016 CineUse
import os
import logging
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from Qt import QtCompat
import pymel.core as pm
import cgtk_log
import cgtk_qt

log = cgtk_log.cgtk_log(level=logging.INFO)
UI = os.path.join(os.environ.get("CGTKUIPATH"), "new_shelf_btn.ui")

if "PySide" not in QtCompat.__binding__:
    QtCore.Signal = QtCore.pyqtSignal


class NewShelfBtn(QtGui.QDialog):
    def __init__(self, current_shelf_name, parent=None):
        super(NewShelfBtn, self).__init__(parent)
        cgtk_qt.setup_ui(UI, self)

        # init current shelf name
        self.current_shelf_name = current_shelf_name
        old_value = self.current_shelf_name_label.text()
        current_shelf_name = old_value.replace("Null", current_shelf_name)
        self.current_shelf_name_label.setText(current_shelf_name)

        self.setupEditor()
        # add drop in event
        python_drop_in = cgtk_qt.dropable(self.code_edit_py)
        mel_drop_in = cgtk_qt.dropable(self.code_edit_mel)
        icon_drop_in = cgtk_qt.dropable(self.icon_label)

        # connections
        python_drop_in.connect(self.on_py_dropped_in)
        mel_drop_in.connect(self.on_mel_dropped_in)
        python_drop_in.connect(self.update_script_name)
        mel_drop_in.connect(self.update_script_name)
        icon_drop_in.connect(self.on_icon_dropped_in)
        self.create_btn.clicked.connect(self.do_create)

        self.mel_radio.toggled.connect(lambda index: self.code_stack.setCurrentIndex(index))

    @property
    def script_name(self):
        return self.script_name_line.text()

    def get_command(self):
        # get current code editor
        current_index = self.code_stack.currentIndex()

        # return script in current editor
        print current_index
        if current_index == 0:
            command_type = "python"
            command = self.code_edit_py.toPlainText()
        else:
            command_type = "mel"
            command = self.code_edit_mel.toPlainText()
        return command_type, command

    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily('Source Code Pro')
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.code_edit_py.setFont(font)
        self.code_edit_mel.setFont(font)

        self.highlighter_py = cgtk_qt.syntax.PythonHighlighter(self.code_edit_py.document())
        self.highlighter_mel = cgtk_qt.syntax.MelHighlighter(self.code_edit_mel.document())

    def on_code_dropped_in(self, script, editor):
        with open(script) as f:
            code = f.read()
        editor.setText(code)

    def on_py_dropped_in(self, files):
        self.on_code_dropped_in(files[0], self.code_edit_py)

    def on_mel_dropped_in(self, files):
        self.on_code_dropped_in(files[0], self.code_edit_mel)

    def on_icon_dropped_in(self, icon_file):
        ext = os.path.splitext(icon_file[0])[-1]
        if ext.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            icon_pix = QtGui.QPixmap(icon_file[0])
            icon_pix = icon_pix.scaled(QtCore.QSize(32, 32), QtCore.Qt.KeepAspectRatio)
            # show in ui
            self.icon_label.setPixmap(icon_pix)

    def update_script_name(self, files):
        code_file = files[0]
        script_name = os.path.splitext(os.path.basename(code_file))[0]
        self.script_name_line.setText(script_name)

    def do_create(self):
        # save image
        # todo: fix the hard coding of icon_dir with configs
        icon_dir = r"C:\Users\aaron\Documents\maya\2016\prefs\icons"
        icon_path = os.path.join(icon_dir, "%s.png" % self.script_name)
        self.icon_label.pixmap().save(icon_path, "PNG")
        # create shelf button
        command_type, command = self.get_command()
        pm.shelfButton(image="%s.png" % self.script_name,
                       style="iconOnly",
                       command=command,
                       sourceType=command_type,
                       parent=self.current_shelf_name)


if __name__ == "__main__":
    pass
