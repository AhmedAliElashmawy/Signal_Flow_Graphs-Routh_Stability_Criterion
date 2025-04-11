from PyQt6.QtWidgets import QApplication, QGraphicsPathItem , QGraphicsScene, QGraphicsView , QGraphicsPolygonItem
from PyQt6.QtGui import QBrush, QPen, QColor , QPainterPath , QPolygonF
from PyQt6.QtCore import Qt , QPointF
import math
from Node import Node
import sympy as sp


class Edge(QGraphicsPathItem):
    def __init__(self, start_node : Node, end_node : Node = None , weight : sp =1):
        super().__init__()

        self.__start_node = start_node
        self.__end_node = end_node
        self.__weight = weight

        self.__pen = QPen(QColor('black'), 2)
        self.setPen(self.__pen)

        # Register edge with nodes
        self.__start_node.add_outward_edge(self)
        if end_node != None:
            self.__end_node.add_inward_edge(self)


        self.arrow_head = QGraphicsPolygonItem(self)



    def update_path(self , start_pos=None , ending_pos=None):
        """Update edge with a curve if the x-distance is large, otherwise keep it straight."""
        path = QPainterPath()


        if ending_pos is None:
            self.__ending_pos = start_pos


        path.moveTo(self.__start_pos)
        path.lineTo(self.__ending_pos)
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




















def DFS (nodes , i , visited):
    nodes[i] = True

    if nodes[i].id == 'C':
        # ADD PATh
        pass

    for i in nodes:
        if(not visited[i]):
            DFS(i)

    nodes[i] = False