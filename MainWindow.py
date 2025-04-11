import sys
from PyQt6.QtWidgets import QApplication, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView, QWidget , QMainWindow , QToolBar, QPushButton
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import Qt
from Signal_Flow import SignalFlowGraph



class MainWindow(QMainWindow):
    MIN_WIDTH = 250
    MIN_HEIGHT = 100
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Signal flow graph OR Routh stability')

        # Sets application dimensions
        self.setGeometry(0, 0, MainWindow.MIN_WIDTH , MainWindow.MIN_HEIGHT)
        self.setMinimumWidth(MainWindow.MIN_WIDTH)
        self.setMinimumHeight(MainWindow.MIN_HEIGHT)
        self.center_window()

        # Create buttons
        self.SignalFlow = QPushButton('Signal Flow', self)
        self.SignalFlow.setGeometry(75, 10, 100, 30)
        self.SignalFlow.clicked.connect(self.create_SignalFlow)

        self.Routh = QPushButton('Routh Stability', self)
        self.Routh.setGeometry(75, 50, 100, 30)
        self.Routh.clicked.connect(self.create_Routh)

    def create_SignalFlow(self):
        window.close()
        self.signal_flow_window = SignalFlowGraph(self)

    def create_Routh(self):
        # TODO: Implement Routh stability method
        pass

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

