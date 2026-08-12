from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPolygon, QPainter, QColor

class Rectangle(QWidget):
    def __init__(self,win,x,y,w,h):
        super().__init__(win)
        self.x_ = x
        self.y_ = y
        self.w_ = w
        self.h_ = h
        
    def paintEvent(self, event):

        self.pen = QPainter(self)
        self.pen.setPen(QColor(0,0,0))
        self.pen.setBrush(QColor(0,50,156))

        self.rectangle = QPolygon([
            QPoint(self.x_, self.y_), 
            QPoint(self.x_+self.w_, self.y_), 
            QPoint(self.x_+self.w_,self.y_+self.h_),
            QPoint(self.x_, self.y_+ self.h_)
        ])
        
        self.pen.drawPolygon(self.rectangle)

        self.pen.end()
