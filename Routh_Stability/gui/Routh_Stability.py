from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QScrollArea, QPushButton, QFrame,
                           QTableWidget, QTableWidgetItem, QMainWindow, QLineEdit, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys

class RouthStability(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Routh Stability')
        self.setGeometry(0, 0, 400, 150)
        self.setMinimumWidth(400)
        self.setMinimumHeight(150)
        self.center_window()
        self.show()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create and configure widgets
        self.equation_label = QLabel("Enter the characteristic equation q(s):")
        self.equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equation_label.setFont(QFont("Arial", 12))
        self.equation_label.setStyleSheet("color: white; margin: 5px;")
        
        self.equation_input = QLineEdit()
        self.equation_input.setPlaceholderText("Example: s^3 + 2s^2 + 3s + 4")
        self.equation_input.setStyleSheet("padding: 5px; margin: 5px;")
        
        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet("padding: 5px; margin: 10px;")
        self.solve_button.clicked.connect(self.solve_equation)
        
        # Add widgets to layout
        layout.addWidget(self.equation_label)
        layout.addWidget(self.equation_input)
        layout.addWidget(self.solve_button)
        
    def solve_equation(self):
        equation = self.equation_input.text().strip()
        if not equation:
            return
        # TODO: Implement the Routh stability calculation logic
        test = [
            "s^3 1 4\ns^2 2 3\ns^1 0 0\ns^0 1 4",
            "s^3 1 4\ns^2 2 3\ns^1 0 0\ns^0 1 4",
            "s^3 1 4\ns^2 2 3\ns^1 0 0\ns^0 1 4"
        ]
        self.display_result(test)
        print(f"Solving for equation: {equation}")

    def display_result(self, result):
        self.setGeometry(0, 0, 800, 600)
        self.center_window()
        self.setWindowTitle("Routh Stability Result")
        self.solve_button.hide()
        self.equation_input.setEnabled(False)
        if hasattr(self, 'scroll_area'):
            self.scroll_area.deleteLater()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.centralWidget().layout().addWidget(self.scroll_area)

        for step_index, step in enumerate(result):
            step_label = QLabel(f"Step {step_index+1}")
            step_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            step_label.setStyleSheet("margin-top: 10px;")
            self.scroll_layout.addWidget(step_label)

            table = QTableWidget()
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setVisible(False)
            
            table.setMinimumHeight(150)
            table.setMinimumWidth(400)
            # Process step data
            steps = [line.strip() for line in step.split('\n') if line.strip()]
            max_columns = max(len(line.split()) for line in steps)
            
            table.setRowCount(len(steps))
            table.setColumnCount(max_columns)
            
            for i in range(table.rowCount()):
                table.setRowHeight(i, 40)
            for j in range(table.columnCount()):
                table.setColumnWidth(j, 100)
            # Fill table with data
            for i, line in enumerate(steps):
                columns = line.split()
                for j, column in enumerate(columns):
                    item = QTableWidgetItem(column)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    # Make font bigger
                    font = QFont()
                    font.setPointSize(12)
                    item.setFont(font)
                    table.setItem(i, j, item)
            
            # Add some spacing between tables
            table.setStyleSheet("QTableWidget { margin: 10px; }")
            
            # Add table to layout
            self.scroll_layout.addWidget(table)

        # Add stretch at the end to keep everything aligned to the top
        self.scroll_layout.addStretch()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        event.accept()
        sys.exit(0)