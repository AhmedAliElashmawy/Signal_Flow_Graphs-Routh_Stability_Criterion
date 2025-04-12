from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QInputDialog, QMessageBox
from PyQt6.QtGui import QBrush, QPen, QColor , QCursor
from PyQt6.QtCore import Qt, QPointF , QTimer
from Signal_Flow.gui.Node import Node
from Signal_Flow.gui.Edge import Edge

class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__adj_list = []
        self.__dragged_edge: Edge = None

        self.setSceneRect(0, 0, 800, 600)
        self.__scene = QGraphicsScene(self)
        self.setScene(self.__scene)
        self.setBackgroundBrush(QBrush(QColor('white')))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__add_node(20, 10, 'R')
        self.__add_node(1000, 20, 'C')

    @property
    def adj_list(self):
        return self.__adj_list

    ##########################################################################

    """ Node Management"""

    def __add_node(self, x, y, id=None):
        new_node = Node(x=x, y=y, node_id=id)
        self.__adj_list.append(new_node)
        self.__scene.addItem(new_node)
        return new_node

    def create_node(self, x, y, text):
        if self.__adj_list:
            for node in self.__adj_list:
                if node.id == text:
                    return node
        node = self.__add_node(x, y, text)
        return node

    def create_edge(self, start_node, end_node, gian=1):
        print(f"Creating edge from {start_node} to {end_node}")
        edge = Edge(start_node=start_node, end_node=end_node)
        self.__scene.addItem(edge)
        start_node.add_outward_edge(edge)
        end_node.add_inward_edge(edge)
        edge.update_path()


    def clear(self):
        for node in self.__adj_list:
            self.__scene.removeItem(node)
        self.__adj_list.clear()
        self.__scene.clear()
        self.__add_node(20 , 10 , 'R')
        self.__add_node(1000 , 20 , 'C')
        self.__dragged_edge = None

    def __change_node_pos(self, node, x, y):
        node.setPos(x - 15, y - 15)
        for edge in node.inward_edges + node.outward_edges:
            edge.update_path()
        self.__scene.update(node.boundingRect())

    def __change_node_id(self , node):
        while True:
            new_id, ok = QInputDialog.getText(self, 'Edit Node ID', 'Enter new ID (1 or 2 alphanumeric characters):', text=node.id)

            # Check if the user entered a valid new ID
            is_dup = any(x.id == new_id for x in self.__adj_list if x!=node)
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

    #########################################################################

    """ Mouse Events """


    def __get_mouse_pos_item(self):
        current_point = self.mapFromGlobal(QCursor.pos())
        pos = self.mapToScene(current_point)
        graphical_item = self.itemAt(current_point)
        return graphical_item, pos

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            graphical_item, _ = self.__get_mouse_pos_item()
            if isinstance(graphical_item, Node):
                self.__change_node_id(graphical_item)
            elif isinstance(graphical_item.parentItem(), Node):
                self.__change_node_id(graphical_item.parentItem())

    def mousePressEvent(self, event):
        graphical_item, pos = self.__get_mouse_pos_item()



        if event.button() == Qt.MouseButton.LeftButton:
            if graphical_item is None:
                self.__add_node(pos.x(), pos.y())

        elif event.button() == Qt.MouseButton.RightButton:
            graphical_item = graphical_item.parentItem() if isinstance(graphical_item.parentItem(), Node) else graphical_item
            if isinstance(graphical_item, Node):
                self.__dragged_edge = Edge(start_node=graphical_item)
                self.__scene.addItem(self.__dragged_edge)
                self.__scene.update(self.__dragged_edge.boundingRect())
                self.__dragged_edge.update_path(None)

        super().mousePressEvent(event)



    def mouseMoveEvent(self, event):
        _ , pos = self.__get_mouse_pos_item()
        items = self.__scene.items(pos)
        node = next((item for item in items if isinstance(item, Node)), None)

        if event.buttons() & Qt.MouseButton.RightButton and self.__dragged_edge:
            self.__dragged_edge.update_path(pos , len(self.__dragged_edge.start_node.outward_edges) -1)
            self.__scene.update(self.__dragged_edge.boundingRect())


        elif event.buttons() & Qt.MouseButton.LeftButton and node is None:
            if isinstance(node, Node):
                self.__change_node_pos(node, pos.x(), pos.y())

        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.__dragged_edge:
            graphical_item, pos = self.__get_mouse_pos_item()

            items = self.__scene.items(pos)
            if all(isinstance(item, Edge) for item in items):
                self.__scene.removeItem(self.__dragged_edge)
                del self.__dragged_edge
                return

            node = next((item for item in items if isinstance(item, Node)), None)
            if isinstance(node, Node) and node != self.__dragged_edge.start_node:
                self.__dragged_edge.end_node = node
                node.add_inward_edge(self.__dragged_edge)
                self.__dragged_edge.update_path(None)
                self.__scene.update(self.__dragged_edge.boundingRect())
            else:
                self.__scene.removeItem(self.__dragged_edge)

            self.__dragged_edge = None

        super().mouseReleaseEvent(event)























































