from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                           QScrollArea, QPushButton, QFrame,
                           QTableWidget, QSpinBox , QHBoxLayout,QSizePolicy, QMainWindow, QLineEdit, QApplication,QTableWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("Agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from Routh_Stability.Routh_Stability_Criterion_Solver import RouthStabilitySolver
import io
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
        central_widget.setStyleSheet("""
           QWidget {
                background-color: #2b2b2b;
                color: white;
            }
        """)
        # Create and configure widgets
        self.equation_label = QLabel("Enter the System Order:")
        self.equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.equation_label.setFont(QFont("Arial", 12))
        self.equation_label.setStyleSheet("color: white;")

        self.spin = QSpinBox()
        self.spin.setValue(3)
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
            try:
                coeffs[i] = int(item.text())
            except ValueError:
                coeffs[i] = 0



        # Optimize coeffs and remove first consecutive zeros
        for i in range(len(coeffs)):
            if coeffs[i]!=0:
                coeffs = coeffs[i:]
                break

        self.solver = RouthStabilitySolver(coeffs)
        sign_changes, rhp_roots , characteristic_eqn, steps = self.solver.solve()
        self.display_result(steps, characteristic_eqn, sign_changes, rhp_roots)
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

    def render_latex_to_pixmap(self, latex_str):
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

    def display_result(self, result, characteristic_eqn , sign_changes , rhp_roots):
        self.setGeometry(0, 0, 1000, 800)  # Make window larger
        self.center_window()
        self.setWindowTitle("Routh Stability Result")
        self.solve_button.hide()
        self.back_button.hide()
        self.equation_label.hide()
        self.spin.hide()
        self.characteristic.hide()


        central_layout = self.centralWidget().layout()


        if hasattr(self, 'scroll_area'):
            central_layout.removeWidget(self.scroll_area)
            self.scroll_area.deleteLater()


        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.centralWidget().layout().addWidget(self.scroll_area)

        #Create break lines
        lines = []

        for _ in range(4):
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            lines.append(line)


        # Shows System Characteristic Equation
        characteristic_eqn_label = QLabel()
        characteristic_eqn_label.setPixmap(self.render_latex_to_pixmap(characteristic_eqn))
        self.scroll_layout.addWidget(characteristic_eqn_label)

        self.scroll_layout.addWidget(lines[0])

        # Shows System Stability
        stability_label = QLabel("The System is " + ("Stable" if sign_changes==0 else "Unstable"))
        stability_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        stability_label.setStyleSheet("color: white; margin: 10px;")
        self.scroll_layout.addWidget(stability_label)




        self.scroll_layout.addWidget(lines[1])



        # Shows No of sign changes
        sign_label = QLabel(f"Number of Sign Changes: {sign_changes}")
        sign_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        sign_label.setStyleSheet("color: white; margin: 10px;")
        self.scroll_layout.addWidget(sign_label)


        self.scroll_layout.addWidget(lines[2])



        # Shows roots in Right hand side of s-plane
        if rhp_roots != []:
            roots_label = QLabel("Roots in positive s-plane side:\n")
            roots_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            roots_label.setStyleSheet("color: white; margin: 10px;")
            self.scroll_layout.addWidget(roots_label)

            for i, root in enumerate(rhp_roots):

                root_latex = f"\\mathrm{{r}}_{{{i}}} = {root}"
                root_label = QLabel()
                root_label.setPixmap(self.render_latex_to_pixmap(f"\\bullet {root_latex}"))

                self.scroll_layout.addWidget(root_label)


            self.scroll_layout.addWidget(lines[3])




        for step_index, step in enumerate(result):

            step_label = QLabel(f"Step {step_index + 1}")
            step_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            step_label.setStyleSheet("margin-top: 10px; color: white;")
            self.scroll_layout.addWidget(step_label)

            table = QTableWidget()
            table.horizontalHeader().setVisible(False)  # Hide horizontal header
            table.verticalHeader().setVisible(False)  # Hide vertical header



            # Determine table size from the number of rows and columns in the result
            num_rows = len(step)
            num_columns = max(len(row) for row in step)

            table.setRowCount(num_rows)
            table.setColumnCount(num_columns)

            # Set the table size (this will help prevent tables from being too small)
            table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # Set minimum height and width for the table and labels to ensure visibility
            max_height = 80*len(result[0]) + 20
            threshold_height = 80*10 + 20

            if(max_height<threshold_height):
                table.setMinimumHeight(max_height)
                table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            else:
                table.setMinimumHeight(threshold_height)

            table.setMinimumWidth(600)


            # Set row and column sizes dynamically based on content size
            for i in range(table.rowCount()):
                table.setRowHeight(i, 80)  # Adjust row height to allow for bigger expressions
            for j in range(table.columnCount()):
                table.setColumnWidth(j, 150)  # Adjust column width



            # Set Highlighted Row
            highlight_row_index = step_index + 1 if 1 <= step_index < len(result) - 1  else -1



            # Populate the table with data
            for i, row in enumerate(step):
                highlighted = i == highlight_row_index
                for j, column in enumerate(row):
                    label = QLabel()
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                    if highlighted:
                        pixmap = self.render_latex_to_pixmap(column)
                        label.setPixmap(pixmap)

                        pix_width = pixmap.width()
                        pix_height = pixmap.height()
                        label.setMinimumSize(pix_width, pix_height)

                        label.setStyleSheet("font-weight: bold; background-color: rgba(255,255,255,0.05);")
                        table.setColumnWidth(j, max(table.columnWidth(j), pix_width))
                        table.setRowHeight(i, max(table.rowHeight(i), pix_height))
                    else:
                        label.setText(str(column))
                        label.setFont(QFont("Arial", 13))
                        label.setStyleSheet("color: white;")  # Optional: white plain text
                        label.setMinimumSize(50, 30)

                    label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    table.setCellWidget(i, j, label)




            table.setStyleSheet("QTableWidget { margin: 10px; }")
            self.scroll_layout.addWidget(table)

        self.scroll_layout.addStretch()

        # Back button fixed at the bottom
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("padding: 10px; margin: 10px;")
        self.back_button.clicked.connect(self.go_back)

        central_layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignBottom)





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






