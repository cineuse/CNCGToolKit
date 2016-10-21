# -*- coding: utf-8 -*-

import Qt.QtGui as QtGui
import Qt.QtCore as QtCore


class DragMoveWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(DragMoveWidget, self).__init__(*args, **kwargs)
        self.__last_clicked_pos = None

    @property
    def last_clicked_pos(self):
        return self.__last_clicked_pos

    def mousePressEvent(self, event):
        super(DragMoveWidget, self).mousePressEvent(event)
        self.__last_clicked_pos = (event.globalPos(), QtCore.QPoint(self.pos()))

    def mouseMoveEvent(self, event):
        if self.__last_clicked_pos:
            move, begin = self.__last_clicked_pos
            self.move((event.globalPos()-move)+begin)
        else:
            super(DragMoveWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(DragMoveWidget, self).mouseReleaseEvent(event)
        self.__last_clicked_pos = None


if __name__ == "__main__":
    pass
