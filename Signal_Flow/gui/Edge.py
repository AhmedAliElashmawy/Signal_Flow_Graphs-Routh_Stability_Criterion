from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsPolygonItem
from PyQt6.QtGui import QPen, QColor, QPainterPath , QCursor
from PyQt6.QtCore import QPointF , Qt
import sympy as sp
from Signal_Flow.gui.Node import Node
import math

class Edge(QGraphicsPathItem):
    def __init__(self, start_node: Node, end_node: Node = None, weight: sp = 1):
        super().__init__()

        self.__start_node = start_node
        self.__end_node = end_node
        self.__weight = weight



        # Register the edge in the nodes
        self.__start_node.add_outward_edge(self)
        if end_node:
            self.__end_node.add_inward_edge(self)

        # Styling
        self.setPen(QPen(QColor('black'), 3))

        # Interaction Flags
        self.setAcceptHoverEvents(True)

        # Positioning
        self.setZValue(-1)
        self.__end_pos = None


    def update_path(self, end_pos=None, curve=0):
        path = QPainterPath()

        # Set starting position
        start_pos = self.__start_node.scenePos() + QPointF(15, 15)

        # Set ending position
        if self.__end_node:
            self.__end_pos = self.__end_node.scenePos() + QPointF(15, 15)
        elif end_pos is not None:
            self.__end_pos = end_pos

        if self.__end_pos is None:
            return

        # Straight line case
        dx = self.__end_pos.x() - start_pos.x()
        if abs(dx) < 20 and curve == 0:
            path.moveTo(start_pos)
            path.lineTo(self.__end_pos)
            self.setPath(path)
            return

        # Use quadratic Bezier curve
        mid = (start_pos + self.__end_pos) / 2
        control = QPointF(mid.x(), mid.y() + curve)  # vertical curve

        path.moveTo(start_pos)
        path.quadTo(control, self.__end_pos)

        # Draw arrow in middle
        t = 0.5  # midpoint
        def bezier_point(p0, p1, p2, t):
            return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

        def bezier_tangent(p0, p1, p2, t):
            return 2 * (1 - t) * (p1 - p0) + 2 * t * (p2 - p1)

        pt = bezier_point(start_pos, control, self.__end_pos, t)
        tangent = bezier_tangent(start_pos, control, self.__end_pos, t)
        angle = math.atan2(tangent.y(), tangent.x())

        # Create arrowhead (triangle)
        arrow_size = 10
        angle1 = angle + math.radians(150)
        angle2 = angle - math.radians(150)
        p1 = pt
        p2 = QPointF(p1.x() + arrow_size * math.cos(angle1), p1.y() + arrow_size * math.sin(angle1))
        p3 = QPointF(p1.x() + arrow_size * math.cos(angle2), p1.y() + arrow_size * math.sin(angle2))

        arrow_path = QPainterPath()
        arrow_path.moveTo(p2)
        arrow_path.lineTo(p1)
        arrow_path.lineTo(p3)

        path.addPath(arrow_path)

        self.setPath(path)














    # Getters
    @property
    def start_node(self):
        return self.__start_node

    @property
    def end_node(self):
        return self.__end_node

    @property
    def weight(self):
        return self.__weight


    # Setters
    @weight.setter
    def weight(self, weight):
        self.__weight = weight

    @start_node.setter
    def start_node(self , start_node):
        self.__start_node = start_node

    @end_node.setter
    def end_node(self , end_node):
        self.__end_node = end_node



    def hoverEnterEvent(self, event):
        self.setPen(QPen(Qt.GlobalColor.blue, 3))

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(Qt.GlobalColor.black, 3))