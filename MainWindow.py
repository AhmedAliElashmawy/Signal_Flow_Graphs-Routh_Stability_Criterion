import sys
from PyQt6.QtWidgets import QApplication, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QWidget , QMainWindow , QToolBar
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import Qt
from Canvas import Canvas



class MainWindow(QMainWindow):
    TOOLBAR_WIDTH = 300
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    def __init__(self):
        super().__init__()


        self.setWindowTitle('Signal flow graph')

        # Sets application dimensions
        self.setGeometry(0, 0, MainWindow.MIN_WIDTH , MainWindow.MIN_HEIGHT)
        self.setMinimumWidth(MainWindow.MIN_WIDTH)
        self.setMinimumHeight(MainWindow.MIN_HEIGHT)

        # Sets canvas
        self.__canvas = Canvas(self)
        self.setCentralWidget(self.__canvas)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Sets canvas dimensions
        canvas_width = self.width() - MainWindow.TOOLBAR_WIDTH
        canvas_height = self.height()

        # Updates canvas size
        self.__canvas.setGeometry(MainWindow.TOOLBAR_WIDTH, 0, canvas_width, canvas_height)
        self.__canvas.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

