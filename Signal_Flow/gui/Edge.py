from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsPolygonItem , QGraphicsTextItem
from PyQt6.QtGui import QPen, QColor, QPainterPath , QCursor 
from PyQt6.QtCore import QPointF , Qt , QRectF
import sympy as sp
from Signal_Flow.gui.Node import Node
import math

class Edge(QGraphicsPathItem):
    def __init__(self, start_node: Node, end_node: Node = None, weight: sp = 1):
        super().__init__()

        self.__start_node = start_node
        self.__end_node = end_node
        self.__weight = weight
        self.__curve = None

        # Set Edge Gain/Weight
        self.__weight_label = QGraphicsTextItem(str(self.__weight), self)
        self.__weight_label.setDefaultTextColor(Qt.GlobalColor.black)

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


    def update_path(self, end_pos=None):
        path = QPainterPath()
        radius = self.__start_node.RADIUS
        start_pos = self.__start_node.scenePos() + QPointF(radius, radius)

        if self.__end_node:
            self.__end_pos = self.__end_node.scenePos() + QPointF(radius, radius)
        elif end_pos is not None:
            self.__end_pos = end_pos

        if self.__end_pos is None:
            return

        # === SELF-LOOP LOGIC ===
        if self.__end_node == self.__start_node:
            loop_radius = 40
            loop_offset = QPointF(0, -radius - loop_radius)

            loop_center = start_pos + loop_offset
            rect = QRectF(loop_center.x() - loop_radius, loop_center.y() - loop_radius,
                        loop_radius * 2, loop_radius * 2)

            path.moveTo(start_pos)
            path.arcTo(rect, 0, 270)  # draw a loop (arc)

            # Arrow in the middle of the arc (approximate at 135 degrees)
            angle = math.radians(135)
            pt = QPointF(loop_center.x() + loop_radius * math.cos(angle),
                        loop_center.y() + loop_radius * math.sin(angle))
            tangent_angle = angle + math.radians(90)

            # Arrowhead
            arrow_size = 10
            angle1 = tangent_angle + math.radians(30)
            angle2 = tangent_angle - math.radians(30)
            p2 = QPointF(pt.x() + arrow_size * math.cos(angle1), pt.y() + arrow_size * math.sin(angle1))
            p3 = QPointF(pt.x() + arrow_size * math.cos(angle2), pt.y() + arrow_size * math.sin(angle2))

            arrow_path = QPainterPath()
            arrow_path.moveTo(p2)
            arrow_path.lineTo(pt)
            arrow_path.lineTo(p3)

            path.addPath(arrow_path)

            # Label position
            label_offset = QPointF(0, -radius - 2 * loop_radius)
            label_pos = start_pos + label_offset - QPointF(
                self.__weight_label.boundingRect().width() / 2,
                self.__weight_label.boundingRect().height() / 2
            )
            self.__weight_label.setPos(label_pos)

            self.setPath(path)
            return  # Done drawing self-loop

        # === ORIGINAL CURVE LOGIC ===
        if self.__curve is None:
            curve_outward = len(self.__start_node.outward_edges) - 1
            curve_backward = len(self.__start_node.inward_edges)
            self.__curve = 75 * (curve_backward if self.__end_pos.x() < start_pos.x() else curve_outward)

        effective_curve = self.__curve
        if self.__end_pos.x() < start_pos.x():
            effective_curve = abs(self.__curve)
        else:
            effective_curve = -abs(self.__curve)

        mid = (start_pos + self.__end_pos) / 2
        control = QPointF(mid.x(), mid.y() + (effective_curve))

        path.moveTo(start_pos)
        path.quadTo(control, self.__end_pos)

        # === Arrowhead and Label ===
        def bezier_point(p0, p1, p2, t):
            return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2

        def bezier_tangent(p0, p1, p2, t):
            return 2 * (1 - t) * (p1 - p0) + 2 * t * (p2 - p1)

        t = 0.5
        pt = bezier_point(start_pos, control, self.__end_pos, t)
        tangent = bezier_tangent(start_pos, control, self.__end_pos, t)
        angle = math.atan2(tangent.y(), tangent.x())

        arrow_size = 10
        angle1 = angle + math.radians(150)
        angle2 = angle - math.radians(150)
        p2 = QPointF(pt.x() + arrow_size * math.cos(angle1), pt.y() + arrow_size * math.sin(angle1))
        p3 = QPointF(pt.x() + arrow_size * math.cos(angle2), pt.y() + arrow_size * math.sin(angle2))

        arrow_path = QPainterPath()
        arrow_path.moveTo(p2)
        arrow_path.lineTo(pt)
        arrow_path.lineTo(p3)

        length = math.hypot(tangent.x(), tangent.y())
        if length == 0:
            offset = QPointF(0, -20)
        else:
            normal = QPointF(tangent.y() / length, -tangent.x() / length)
            offset = normal * 20

        label_pos = pt + offset - QPointF(
            self.__weight_label.boundingRect().width() / 2,
            self.__weight_label.boundingRect().height() / 2
        )
        self.__weight_label.setPos(label_pos)

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
        self.__weight_label.setPlainText(str(weight))

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