from PyQt6.QtWidgets import QApplication, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView , QGraphicsPathItem, QInputDialog , QMessageBox
from PyQt6 import QtCore
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import Qt , QPointF
from Node import Node
from Edge import Edge
from typing import Final

class Canvas(QGraphicsView):
    def __init__(self , parent=None):
        super().__init__(parent)

        self.__node_list = []
        self.__dragged_edge : Edge = None

        self.setSceneRect(0, 0, 800, 600)  # Set fixed scene size
        self.__scene = QGraphicsScene(self)
        self.setScene(self.__scene)
        self.setBackgroundBrush(QBrush(QColor('white')))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


        self.__add_node(20 , 10 , 'R')
        self.__add_node(1000 , 20 , 'C')

    @property
    def adj_list(self):
        return self.__node_list



    def __add_node(self , x , y , id=None):
        new_node = Node(x=x , y=y , node_id=id)
        self.__node_list.append(new_node)
        self.__scene.addItem(new_node)

    def __add_edge(self , edge):
        self.__edge_list.append(edge)



    def __change_node_pos(self , node , x , y):
        node.setPos(x-15,y-15)
        node.pos = QPointF(x-15 , y-15)
        node_rect = node.boundingRect()
        for edge in node.inward_edges + node.outward_edges:
                edge.update_path()
                self.__scene.update(edge)
        self.__scene.update(node_rect)

    def __change_node_id(self , node):
        while True:
            new_id, ok = QInputDialog.getText(self, 'Edit Node ID', 'Enter new ID (1 or 2 alphanumeric characters):', text=node.id)

            # Check if the user entered a valid new ID
            is_dup = any(x.id == new_id for x in self.__node_list if x!=node)
            if ok:
                if 1 <= len(new_id) <= 2 and new_id.isalnum() and not is_dup:
                    node.set_id(new_id)
                    node.update()
                    break  # Exit the loop if valid ID is entered
                else:

                    invalid_format_message = 'ID must be 1 or 2 alphanumeric characters (no special characters).'

                    message = 'ID already exists' if  is_dup else invalid_format_message

                    QMessageBox.warning(self ,"Warning", message)
            else:
                # Break the loop if the user cancels
                break


    def __get_mouse_pos_item(self , event):

        current_point = event.position().toPoint()
        pos = self.mapToScene(current_point)
        graphical_item = self.itemAt(current_point)

        return graphical_item , pos


    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:


            graphical_item , pos = self.__get_mouse_pos_item(event)
            if isinstance(graphical_item , Node):
                # Open a dialog to edit the node ID
                self.__change_node_id(graphical_item)
            elif isinstance(graphical_item.parentItem() , Node):
                self.__change_node_id(graphical_item.parentItem())


    def mouseMoveEvent(self, event):
        graphical_item, pos = self.__get_mouse_pos_item(event)

        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.__dragged_edge is not None:
                # Update the temp edge being dragged
                self.__dragged_edge.update_path(ending_pos=event.position())
                self.__scene.update(self.__dragged_edge)
            elif isinstance(graphical_item, Node):
                self.__change_node_pos(graphical_item, pos.x(), pos.y())
            elif isinstance(graphical_item.parentItem(), Node):
                self.__change_node_pos(graphical_item.parentItem(), pos.x(), pos.y())



    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:

            graphical_item , pos = self.__get_mouse_pos_item(event)

            if graphical_item is None:
                self.__add_node(pos.x(), pos.y())
            elif isinstance(graphical_item , Node):
                self.__dragged_edge = Edge(graphical_item)
                self.__dragged_edge.update_path(pos)
                self.__scene.addItem(self.__dragged_edge)



    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            graphical_item , pos = self.__get_mouse_pos_item(event)
            if isinstance(graphical_item , Node):
                self.__dragged_edge.update_path(ending_pos=pos)
                self.__add_edge(self.__dragged_edge)
                self.__scene.update(self.__dragged_edge)
                self.__dragged_edge = None
            else:
                self.__scene.removeItem(self.__dragged_edge)
                del self.__dragged_edge

    def create_node(self, x, y, text):
        if self.__node_list:
            for node in self.__node_list:
                if node.id == text:
                    return
        self.__add_node(x, y, text)




















