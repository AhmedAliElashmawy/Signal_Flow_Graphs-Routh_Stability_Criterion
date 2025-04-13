from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QToolBar, QLineEdit, QLabel, QVBoxLayout, QApplication, QDialog, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt
from Signal_Flow.gui.Canvas import Canvas
import sys

class SignalFlowGraph(QMainWindow):
    TOOLBAR_HEIGHT = 50
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__canvas = Canvas(self)
        self.setCentralWidget(self.__canvas)
        self.setWindowTitle('Signal Flow Graph')
        self.showMaximized()

        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(self.TOOLBAR_HEIGHT)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: white;
                border: 1px solid white;  /* Changed border to white */
                border-radius: 0px;
            }
            QPushButton {
                background-color: #8a8a8a;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #BDBDBD;
            }
        """)
        self.toolbar.setMovable(False)
        # Create buttons widget
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.addStretch()

        # Create buttons
        self.add_function_btn = QPushButton('Add Function')
        self.add_function_btn.clicked.connect(self.addFunction)
        self.calculate_btn = QPushButton('Calculate Transfer Function')
        self.clear_btn = QPushButton('Clear Graph')
        self.clear_btn.clicked.connect(self.clear_graph)

        # Add buttons to layout
        buttons_layout.addWidget(self.add_function_btn)
        buttons_layout.addWidget(self.calculate_btn)
        buttons_layout.addWidget(self.clear_btn)

        # Add right stretch to center the buttons
        buttons_layout.addStretch()
        buttons_widget.setLayout(buttons_layout)
        # Add buttons widget to toolbar
        self.toolbar.addWidget(buttons_widget)

    def clear_graph(self):
        self.__canvas.clear()


    def addFunction(self):
        dialog = QDialog(self)
        dialog.setWindowFlags(Qt.WindowType.Window)
        dialog.setWindowTitle("Add Function")
        dialog.setMinimumSize(700, 400)

        self.equation_rows = []

        # Set black theme stylesheet
        dialog.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QLineEdit {
                background-color: #3b3b3b;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
                color: white;
            }
            QLabel {
                color: white;
                padding: 0 10px;
            }
            QPushButton {
                background-color: #404040;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px 15px;
                color: white;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QScrollArea {
                border: none;
            }
        """)

        dialog_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        def add_equation_row():
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10)

            left_textbox = QLineEdit()
            equals_label = QLabel("=")
            right_textbox = QLineEdit()

            row_layout.addWidget(left_textbox)
            row_layout.addWidget(equals_label)
            row_layout.addWidget(right_textbox)

            main_layout.insertLayout(len(self.equation_rows), row_layout)
            self.equation_rows.append(row_layout)

        # Add initial equation row
        add_equation_row()

        # Create add more button
        add_more_btn = QPushButton("+")
        add_more_btn.clicked.connect(add_equation_row)
        add_more_btn.setFixedWidth(40)
        main_layout.addWidget(add_more_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # Set layout for scroll content
        scroll_content.setLayout(main_layout)
        scroll_area.setWidget(scroll_content)

        # Create buttons layout
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.addToCanvas())
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.close)
        buttons_layout.addStretch()
        buttons_layout.addWidget(ok_button)
        buttons_layout.addSpacing(500)
        buttons_layout.addWidget(cancel_button)

        # Add scroll area and buttons to dialog layout
        dialog_layout.addWidget(scroll_area)
        dialog_layout.addLayout(buttons_layout)

        # Set layout for dialog
        dialog.setLayout(dialog_layout)

        # Show dialog
        dialog.show()

    def addToCanvas(self):
        x_offset = 0
        y_offset = 0
        for row in self.equation_rows:
            left_textbox = row.itemAt(0).widget()
            right_textbox = row.itemAt(2).widget()
            if not left_textbox.text().strip() or not right_textbox.text().strip():
                QMessageBox.warning(self, "Warning", "Please fill all fields")
                return
            left_text = left_textbox.text()
            right_text = right_textbox.text()
            gain = ''

            for char in right_text:
                if char.isdigit() or char == '.':
                    gain += char
                    right_text = right_text.replace(char, '', 1)
                else:
                    break

            gain = float(gain) if gain else 1.0
            print(f"Left: {left_text}, Right: {right_text}, Gain: {gain}")

            # Use the new public method with proper spacing
            
            left_node = self.__canvas.create_node(x_offset, y_offset, left_text)
            right_node=self.__canvas.create_node(x_offset + 100, y_offset, right_text)
            if left_node and right_node:
                self.__canvas.create_edge(left_node, right_node, gain)
            y_offset += 50  # Move next pair of nodes down

        # Close the dialog after adding nodes
        self.findChild(QDialog).close()

    def closeEvent(self, event):
        event.accept()
        self.__canvas.close()
        self.__canvas.deleteLater()
        self.__canvas = None
        sys.exit(0)
