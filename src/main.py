#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, numpy
from PySide2 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        view = GraphicView()
        scroller = QtWidgets.QScrollArea()
        scroller.setWidget(view)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(scroller, 0, 0)

        self.setLayout(layout)
        self.resize(view.width(), view.height())
        self.setWindowTitle("QGraphics View Scene Item + QScrollArea")
        self.show()
     
class GraphicView(QtWidgets.QGraphicsView):
    def __init__(self):
        QtWidgets.QGraphicsView.__init__(self)
        self.setWindowTitle("QGraphicsScene draw Grid")
        self.setScene(EditorScene(self))

    def mousePressEvent(self, event):
        super(self.__class__, self).mousePressEvent(event)
        if self.scene(): self.scene().update()

    def mouseMoveEvent(self, event):
        super(self.__class__, self).mouseMoveEvent(event)
        if self.scene(): self.scene().update()

class EditorScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
        self.setSceneRect(0, 0, self.size*self.scale, self.size*self.scale)

        grid = GridItem()
        self.addItem(grid)

        bg = BackgroundItem()
        self.addItem(bg)

        drawable = DrawableItem()
        self.addItem(drawable)

        bg.setZValue(0)
        drawable.setZValue(1)
        grid.setZValue(9999)

    def mousePressEvent(self, event):
        for item in self.items():
            item.mousePressEvent(event)
        super(self.__class__, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        for item in self.items():
            item.setAcceptHoverEvents(True)
            item.mouseMoveEvent(event)
        super(self.__class__, self).mouseMoveEvent(event)

class DrawableItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.size = 16
        self.scale = 32
        self.pixels = numpy.zeros(self.size*self.size).reshape(self.size, self.size)

    def paint(self, painter, option, widget):
        painter.fillRect(widget.rect(), QtGui.QBrush( QtGui.QColor(0,0,0,0), QtCore.Qt.SolidPattern))
        for y in range(self.size):
            for x in range(self.size):
                if 1 == self.pixels[y][x]:
                    painter.fillRect(x*self.scale, y*self.scale, self.scale, self.scale, QtGui.QBrush( QtGui.QColor(255,0,0,128), QtCore.Qt.SolidPattern))

    def mouseMoveEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
        print('Move', str(pos.x()//self.scale), str(pos.y()//self.scale))
        if event.buttons() & QtCore.Qt.LeftButton:
            self.pixels[y][x] = 1
            print('L DRAG!!', x, y)
        if event.buttons() & QtCore.Qt.RightButton:
            self.pixels[y][x] = 0
            print('R DRAG!!', x, y)

    def mousePressEvent(self, event):
        pos = event.scenePos()
        x = int(pos.x()//self.scale)
        y = int(pos.y()//self.scale)
        print(type(pos.x()))
        print('Press', str(pos.x()//self.scale), str(pos.y()//self.scale))
        if event.buttons() & QtCore.Qt.LeftButton:
            self.pixels[y][x] = 1
            print('L PRESS!!', x, y)
        if event.buttons() & QtCore.Qt.RightButton:
            self.pixels[y][x] = 0
            print('R PRESS!!', x, y)

    def mouseReleaseEvent(self, event):
        pass
    def mouseDoubleClickEvent(self, event):
        pass

class BackgroundItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
        self.colors = [QtGui.QColor(196,196,196,255), QtGui.QColor(232,232,232,255)]
    def paint(self, painter, option, widget):
        for i in range(self.size*self.size):
            x = (i % self.size)
            y = (i // self.size)
            color = QtGui.QColor(128,128,128,255) if 0 == (i % 2) and 0 == (x % 2) else QtGui.QColor(196,196,196,255)
            painter.fillRect(x * (self.scale),               y * (self.scale),               self.scale//2, self.scale//2, self.colors[0])
            painter.fillRect(x * (self.scale)+self.scale//2, y * (self.scale)+self.scale//2, self.scale//2, self.scale//2, self.colors[0])
            painter.fillRect(x * (self.scale)+self.scale//2, y * (self.scale),               self.scale//2, self.scale//2, self.colors[1])
            painter.fillRect(x * (self.scale),               y * (self.scale)+self.scale//2, self.scale//2, self.scale//2, self.colors[1])

class GridItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.size = 16
        self.scale = 32
    def paint(self, painter, option, widget):
        painter.fillRect(widget.rect(), QtGui.QBrush(QtGui.QColor(0,0,0,0), QtCore.Qt.SolidPattern))
        lines = []
        for y in range(self.size+1):
            lines.append(QtCore.QLine(0, y*self.scale, self.size*self.scale, y*self.scale))
        for x in range(self.size+1):
            lines.append(QtCore.QLine(x*self.scale, 0, x*self.scale, self.size*self.scale))
        painter.drawLines(lines)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

