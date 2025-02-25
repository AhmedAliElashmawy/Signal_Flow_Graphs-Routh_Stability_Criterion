import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QToolBar, QLineEdit, QHBoxLayout, QLabel)
from graph_widget import GraphWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signal Flow Graph & Routh Stability Analyzer")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Buttons
        self.sfg_button = QPushButton("Draw Signal Flow Graph")
        self.routh_button = QPushButton("Compute Routh Stability")

        # Connect button to method
        self.sfg_button.clicked.connect(self.show_sfg)

        layout.addWidget(self.sfg_button)
        layout.addWidget(self.routh_button)

        # Create toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Node creation widgets
        self.node_id_input = QLineEdit()
        self.node_id_input.setPlaceholderText("Node ID")
        
        # Edge creation widgets
        self.from_node_input = QLineEdit()
        self.to_node_input = QLineEdit()
        self.gain_input = QLineEdit()
        self.from_node_input.setPlaceholderText("From Node")
        self.to_node_input.setPlaceholderText("To Node")
        self.gain_input.setPlaceholderText("Gain")

        # Add widgets to toolbar
        add_node_btn = QPushButton("Add Node")
        add_node_btn.clicked.connect(self.add_node)
        toolbar.addWidget(add_node_btn)
        
        toolbar.addSeparator()
        
        toolbar.addWidget(QLabel("Add Edge:"))
        toolbar.addWidget(self.from_node_input)
        toolbar.addWidget(self.to_node_input)
        toolbar.addWidget(self.gain_input)
        add_edge_btn = QPushButton("Add Edge")
        add_edge_btn.clicked.connect(self.add_edge)
        toolbar.addWidget(add_edge_btn)

    def show_sfg(self):
        self.graph_widget = GraphWidget()
        self.setCentralWidget(self.graph_widget)

    def add_node(self):
        try:
            num_nodes = self.graph_widget.num_nodes()
            node_id = num_nodes + 1
            x = 50
            y = 50
            self.graph_widget.add_node(node_id, x, y)
        except (ValueError, AttributeError):
            pass  # Handle invalid input

    def add_edge(self):
        try:
            from_node = int(self.from_node_input.text())
            to_node = int(self.to_node_input.text())
            gain = float(self.gain_input.text())
            self.graph_widget.add_edge(from_node, to_node, gain)
            # Clear inputs after successful addition
            self.from_node_input.clear()
            self.to_node_input.clear()
            self.gain_input.clear()
        except (ValueError, AttributeError):
            pass  # Handle invalid input

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
