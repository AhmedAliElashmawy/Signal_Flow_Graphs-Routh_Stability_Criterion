from PyQt6 import QtWidgets, QtCore , QtGui
from PyQt6.QtCore import Qt , QPointF
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent,QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsPathItem
from PyQt6.QtGui import QPen, QColor , QBrush , QPainterPath


class Node(QGraphicsEllipseItem):

    ID = 0
    RADIUS = 15

    def __init__(self , x , y , node_id = None):

        super().__init__()

        self.__inward_edges = []
        self.__outward_edges = []


        # Set the Node ID
        node_id = "X"+ str(Node.ID) if node_id == None else node_id
        Node.ID += 1
        self.__node_id = QGraphicsTextItem(node_id, self)
        self.__node_id.setDefaultTextColor(Qt.GlobalColor.black)

        # Center the text inside the ellipse
        text_rect = self.__node_id.boundingRect()
        text_x = (Node.RADIUS*2 - text_rect.width()) / 2
        text_y = (Node.RADIUS*2 - text_rect.height()) / 2
        self.__node_id.setPos(text_x, text_y)




        # Set Position and Radius
        self.setRect(0, 0, Node.RADIUS*2, Node.RADIUS*2)
        self.setPos(x- Node.RADIUS, y- Node.RADIUS)
        self.setZValue(1)

        # Boarder Styling
        self.setBrush(QBrush(QColor('white')))
        self.setPen(QPen(Qt.GlobalColor.black, 2))

        # Object Interaction Flags
        self.setFlags(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable |
                      QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)



    def set_id(self,node_id):
        self.__node_id.setPlainText(node_id)

    def add_outward_edge(self,edge):
        self.__outward_edges.append(edge)

    def add_inward_edge(self,edge):
        self.__inward_edges.append(edge)

    @property
    def inward_edges(self):
        return self.__inward_edges

    @property
    def outward_edges(self):
        return self.__outward_edges

    @property
    def id(self):
        return self.__node_id.toPlainText()



    def hoverEnterEvent(self, event):
        self.setPen(QPen(Qt.GlobalColor.darkCyan, 2))

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(Qt.GlobalColor.black, 2))






















