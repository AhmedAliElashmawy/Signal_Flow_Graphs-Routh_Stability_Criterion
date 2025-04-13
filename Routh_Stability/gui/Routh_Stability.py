from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QScrollArea, QPushButton, QFrame,
                           QTableWidget, QTableWidgetItem, QMainWindow,
                           QLineEdit, QApplication, QSpinBox , QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from Routh_Stability.stability_solver import RouthStabilitySolver
import sys

class RouthStability(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Routh Stability')
        self.setGeometry(0, 0, 380, 300)
        self.setMinimumWidth(380)
        self.setMinimumHeight(300)
        self.center_window()
        self.show()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create and configure widgets
        self.equation_label = QLabel("Enter the System Order:")
        self.equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equation_label.setFont(QFont("Arial", 12))
        self.equation_label.setStyleSheet("color: white;")
        
        self.spin = QSpinBox()
        self.spin.setMinimum(1)
        
        self.characteristic = self.characteristic_table(self.spin.value())
        
        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet("padding: 5px; margin: 10px;")
        self.solve_button.clicked.connect(self.solve_equation)
        
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("padding: 5px; margin: 10px;")
        self.back_button.clicked.connect(self.go_back)
        
        self.spin.valueChanged.connect(self.update_characteristic_table)
        
        layout.addWidget(self.equation_label)
        layout.addWidget(self.spin)
        layout.addWidget(self.characteristic)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.solve_button)
        button_layout.addWidget(self.back_button)
        
        layout.addLayout(button_layout)

    def go_back(self):
        self.close()
        self.parent().show()

    def update_characteristic_table(self):
        layout = self.centralWidget().layout()
        layout.removeWidget(self.characteristic)
        self.characteristic.deleteLater()
        self.characteristic = self.characteristic_table(self.spin.value())
        layout.insertWidget(2, self.characteristic)

    def solve_equation(self):
        coeffs = [0] * (self.spin.value() + 1)
        for i in range(self.spin.value() + 1):
            item = self.characteristic.item(0, i)
            coeffs[i] = int(item.text()) if item and item.text().isdigit() else 0
        print(coeffs)
        self.solver = RouthStabilitySolver(coeffs)
        self.solver.create_table()
        self.solver.solve()
        self.solver.print_steps()
        # self.display_result(test)

    def characteristic_table(self, colums):
        table = QTableWidget()
        table.setColumnCount(colums + 1)
        table.setRowCount(1)
        table.setHorizontalHeaderLabels([f"s^{colums-i}" for i in range(colums + 1)])
        table.horizontalHeader().setVisible(True)
        table.verticalHeader().setVisible(False)
        table.setFixedHeight(88)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #1C1C1C;
                gridline-color: #3A3A3A;
                border: 1px solid #3A3A3A;
                border-radius: 6px;
                margin: 10px;
            }
            QHeaderView::section {
                background-color: #2A2A2A;
                color: white;
                padding: 5px;
                border: 1px solid #3A3A3A;
            }
            QTableWidget::item {
                color: white;
                padding: 5px;
            }
        """)
        
        for i in range(colums):
            table.setColumnWidth(i, 80)
        
        return table

    def display_result(self, result):
        self.setGeometry(0, 0, 800, 600)
        self.center_window()
        self.setWindowTitle("Routh Stability Result")
        self.solve_button.hide()
        self.equation_label.hide()
        self.spin.hide()
        self.characteristic.hide()
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
                    font = QFont()
                    font.setPointSize(12)
                    item.setFont(font)
                    table.setItem(i, j, item)
            
            table.setStyleSheet("QTableWidget { margin: 10px; }")
            
            self.scroll_layout.addWidget(table)

        self.scroll_layout.addStretch()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        if self.parent() is None:
            event.accept()
            sys.exit(0)
        else:
            event.accept()
            self.close()
