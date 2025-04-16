from PyQt6.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QToolBar, QLineEdit, QLabel, QVBoxLayout, QApplication, QDialog, QScrollArea, QMessageBox , QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from Signal_Flow.gui.Canvas import Canvas
from LogicalComputation.Loops_and_Path_Extractor import solver
from LogicalComputation.Signal_Flow_Graph_Solver import SignalFlowAnalyzer
from Signal_Flow.gui.Node import Node
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("Agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sympy import Symbol, latex , simplify
import io
import re
import sys
from sympy import sympify

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
        self.calculate_btn.clicked.connect(self.show_solution)
        self.delete_mode_btn = QPushButton('Enter Delete_Mode')
        self.delete_mode_btn.clicked.connect(self.toggle_delete)
        self.clear_btn = QPushButton('Clear Graph')
        self.clear_btn.clicked.connect(self.clear_graph)
        self.back_btn = QPushButton('Back')
        self.back_btn.clicked.connect(self.back)

        # Add buttons to layout
        buttons_layout.addWidget(self.add_function_btn)
        buttons_layout.addWidget(self.calculate_btn)
        buttons_layout.addWidget(self.delete_mode_btn)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.back_btn)






        # Add right stretch to center the buttons
        buttons_layout.addStretch()
        buttons_widget.setLayout(buttons_layout)
        # Add buttons widget to toolbar
        self.toolbar.addWidget(buttons_widget)

    def clear_graph(self):
        self.__canvas.clear()

    def back(self):
        self.close()
        self.parent().show()

    def toggle_delete(self):
        if(self.__canvas.delete_mode):
            self.delete_mode_btn.setText("Enter Delete Mode")
            self.delete_mode_btn.setStyleSheet("background-color: grey;")
            self.__canvas.delete_mode = False
        else:
            self.delete_mode_btn.setText("Exit Delete Mode")
            self.delete_mode_btn.setStyleSheet("background-color: red;")
            self.__canvas.delete_mode = True


    def addFunction(self):
        self.dialog = QDialog(self)
        dialog = self.dialog
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
            left_textbox.setPlaceholderText("e.g., X1 (no R)")
            left_textbox.setMinimumWidth(100)

            equals_label = QLabel("=")

            right_textbox = QLineEdit()
            right_textbox.setPlaceholderText("e.g., (s+1)*X2")
            right_textbox.setMinimumWidth(200)

            row_layout.addWidget(left_textbox)
            row_layout.addWidget(equals_label)
            row_layout.addWidget(right_textbox)

            # Optional: Add a row-specific error label
            # error_label = QLabel("")
            # error_label.setStyleSheet("color: red")
            # row_layout.addWidget(error_label)

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
            left_textbox.setPlaceholderText("e.g., X1")
            right_textbox.setPlaceholderText("e.g., (s+1)X2 + (2*s)X3")
            if left_textbox.text().strip() == 'R':
                QMessageBox.warning(self, "Warning", "No 'R' are allowed on the left box")
                return
            left_text = left_textbox.text()
            right_text = right_textbox.text().replace(' ', '')
            arr = []
            gain = []
            i = 0

            # X1 = (A)X2+(-3.5)R

            while i < len(right_text):
                if right_text[i] == '(':
                    i += 1
                    temp = ''
                    while i < len(right_text) and right_text[i] != ')':
                        temp += right_text[i]
                        i += 1
                    gain.append(temp)
                    i += 1
                elif right_text[i] == '+':
                    i += 1
                elif right_text[i] == '*' or right_text[i] == '/':
                    QMessageBox.warning(self, "Warning", "No '*' or '/' are allowed")
                    return
                else:
                    temp = ''
                    while i < len(right_text) and right_text[i] != '(' and right_text[i] != '+':
                        if right_text[i] == 'C':
                            QMessageBox.warning(self, "Warning", "No 'C' are allowed on the right box")
                            return
                        temp += right_text[i]
                        i += 1
                    if temp:
                        arr.append(temp)
            
            # gain = ['A', '-3.5']
            # arr = ['X2', 'R']
            
            left_node = self.__canvas.create_node(x_offset, y_offset, left_text)
            for i in range(len(arr)):
                weight = sympify(gain[i]) if i < len(gain) else 1.0
                right_node=self.__canvas.create_node(x_offset + 100, y_offset, arr[i])
                if left_node and right_node:
                    self.__canvas.create_edge(right_node, left_node, weight)
            y_offset += 50  # Move next pair of nodes down
            
        # Close the dialog after adding nodes
        if hasattr(self, 'dialog') and self.dialog is not None:
            self.dialog.close()
            self.dialog = None




    def closeEvent(self, event):
        if self.parent() is None:  # Only exit if no parent (main application close)
            event.accept()
            self.__canvas.close()
            self.__canvas.deleteLater()
            self.__canvas = None
            sys.exit(0)
        else:  # Otherwise just clean up resources
            event.accept()
            self.__canvas.close()
            self.__canvas.deleteLater()
            self.__canvas = None


#############################################################################
    def render_to_latex(self , latex_str):
        fig = plt.figure(figsize=(0.01, 0.01))
        text = fig.text(
                0, 0, f"${latex_str}$",
                fontsize=16,
                fontfamily="monospace",  # or "sans-serif", "monospace", etc.
                fontweight="bold",     # optional: "normal", "bold", "light"
                color="white"
            )
        fig.patch.set_alpha(0.0)

        canvas = FigureCanvas(fig)
        canvas.draw()
        bbox = text.get_window_extent()
        width, height = bbox.size
        width, height = int(width), int(height)
        fig.set_size_inches(width / fig.dpi, height / fig.dpi)
        canvas.draw()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=fig.dpi, bbox_inches='tight', transparent=True, pad_inches=0.05)
        plt.close(fig)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        return pixmap


    def __create_title(self,text):
        title = QLabel(text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        return title

    def __create_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: white; background-color: white;")
        return line


    def show_solution(self):
        solution_dialog = QDialog(self)
        solution_dialog.setModal(True)
        solution_dialog.setWindowTitle("Solution")
        solution_dialog.setMinimumSize(500, 400)

        # Styling
        solution_dialog.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QPushButton {
                padding: 8px 20px;
                border-radius: 4px;
                background-color: #404040;
                border: 1px solid #555;
                color: white;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)

        scroll.setWidget(scroll_content)

        # Extracts paths and loops
        path_loops_extractor = solver(self.__canvas)
        path_loops_extractor.extract_paths_and_loops()
        paths, loops = path_loops_extractor.paths, path_loops_extractor.loops

        # Computes the deltas and the total transfer func
        _solver = SignalFlowAnalyzer()
        main_delta , deltas , non_touching_loops ,total_transfer_func = _solver.solve(loops , paths)

        # Title: Paths
        layout.addWidget(self.__create_title("Paths"))

        for i, path in enumerate(paths, 1):
            node_str = " \\rightarrow ".join(str(n) for n in path["path"])
            weight_str = latex(path["weight"])  # convert sympy expression or keep as str
            latex_str = f"\\bullet P_{{{i}}} : {node_str}, \\quad W = {weight_str}"
            pixmap = self.render_to_latex(latex_str)
            label = QLabel()
            label.setPixmap(pixmap)
            layout.addWidget(label)

        layout.addWidget(self.__create_separator())

        # Title: Loops
        layout.addWidget(self.__create_title("Loops"))

        for i, loop in enumerate(loops, 1):
            node_str = " \\rightarrow ".join(str(n) for n in loop["loop"])
            weight_str = latex(loop["weight"])
            latex_str = f"\\bullet L_{{{i}}} : {node_str}, \\quad W = {weight_str}"
            pixmap = self.render_to_latex(latex_str)
            label = QLabel()
            label.setPixmap(pixmap)
            layout.addWidget(label)

        layout.addWidget(self.__create_separator())

        # Title: Non-Touching Loops
        layout.addWidget(self.__create_title("Non-Touching Loops"))

        # Map loop content to their label names
        loop_labels = {}
        for idx, loop in enumerate(_solver.loops_gain.keys(), 1):
            loop_labels[tuple(loop)] = f"L_{{{idx}}}"

        for level in sorted(non_touching_loops.keys()):
            if not non_touching_loops[level]:
                continue

            level_title = QLabel(f"{level + 1} Non-Touching Loops")
            level_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(level_title)

            for group in non_touching_loops[level]:
                label_names = [loop_labels[tuple(loop)] for loop in group]
                joined = " \\quad \\|\\quad ".join(label_names)
                latex_str = f"\\bullet {joined}"
                label = QLabel()
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setPixmap(self.render_to_latex(latex_str))
                layout.addWidget(label)

        layout.addWidget(self.__create_separator())



        #Title : Deltas
        layout.addWidget(self.__create_title("Deltas"))


        for i, delta in enumerate(deltas, 1):
            delta_str = f"\\bullet \\Delta_{i} = {latex(delta)}"
            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setPixmap(self.render_to_latex(delta_str))
            layout.addWidget(label)

        layout.addWidget(self.__create_separator())

        #Title : Deltas
        layout.addWidget(self.__create_title("Delta"))

        delta_str = f"\\Delta = {latex(main_delta)}"
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setPixmap(self.render_to_latex(delta_str))
        layout.addWidget(label)

        layout.addWidget(self.__create_separator())



        #Transfer func R/C
        layout.addWidget(self.__create_title("Total Transfer Function"))

        total_transfer_func = "\\infty" if main_delta ==0 else total_transfer_func
        total_transfer_func_str = f"\\frac{{C}}{{R}} = {total_transfer_func}"
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setPixmap(self.render_to_latex(total_transfer_func_str))
        layout.addWidget(label)






        layout.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(solution_dialog.close)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(scroll)
        dialog_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        solution_dialog.setLayout(dialog_layout)

        solution_dialog.exec()





