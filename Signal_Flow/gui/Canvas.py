from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QInputDialog, QMessageBox
from PyQt6.QtGui import QBrush, QColor , QCursor
from PyQt6.QtCore import Qt
from Signal_Flow.gui.Node import Node
from Signal_Flow.gui.Edge import Edge
from sympy import sympify , SympifyError


class Canvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__adj_list = []
        self.__dragged_edge: Edge = None
        self.__delete_mode = False

        self.setSceneRect(0, 0, 800, 600)
        self.__scene = QGraphicsScene(self)
        self.setScene(self.__scene)
        self.setBackgroundBrush(QBrush(QColor('white')))

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__add_node(20, 10, 'R')
        self.__add_node(1000, 20, 'C')
        Node.reset_id()

    @property
    def adj_list(self):
        return self.__adj_list

    @property
    def delete_mode(self):
        return self.__delete_mode
    @delete_mode.setter
    def delete_mode(self , mode):
        self.__delete_mode = mode

    ##########################################################################



    """ Node Management"""

    def __add_node(self, x, y, id=None):
        existing_ids = {node.id for node in self.__adj_list}

        if id is None:
            while True:
                proposed_id = f"X{Node.ID}"
                if proposed_id not in existing_ids:
                    id = proposed_id
                    break
                Node.ID += 1

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

    def create_edge(self, start_node, end_node, gain=1):
        print(f"Creating edge from {start_node} to {end_node}")
        edge = Edge(start_node=start_node, end_node=end_node, weight=gain)
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
        Node.reset_id()
        self.__dragged_edge = None

    def __change_node_pos(self, node : Node, x, y):
        node.setPos(x - 15, y - 15)
        for edge in node.inward_edges + node.outward_edges:
            edge.update_path(None)
            self.__scene.update(edge.boundingRect())
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

    """ Edge Management"""

    def __change_edge_weight(self, edge: Edge):
        while True:

            new_weight, ok = QInputDialog.getText(
                self,
                'Edit Edge Weight',
                'Enter new weight (Algebraic Expression / Numeric Value):',
                text=str(edge.weight)
            )

            if not ok:
                break  # User cancelled

            try:
                expr = sympify(new_weight)
                edge.weight = expr
                edge.update()
                break  # Success
            except (SympifyError, SyntaxError):
                QMessageBox.warning(
                    self,
                    "Invalid Input",
                    "Please enter a valid number or algebraic expression."
                )



    #########################################################################

    def __delete_item(self, graphical_item):

        while graphical_item and not isinstance(graphical_item, (Node, Edge)):
            graphical_item = graphical_item.parentItem()

        if isinstance(graphical_item, Node):
            node = graphical_item

            for edge in node.inward_edges[:]:
                if edge.start_node:
                    edge.start_node.outward_edges.remove(edge)
                self.__scene.removeItem(edge)

            for edge in node.outward_edges[:]:
                if edge.end_node:
                    edge.end_node.inward_edges.remove(edge)
                self.__scene.removeItem(edge)

            self.__scene.removeItem(node)
            self.__adj_list.remove(node)

        elif isinstance(graphical_item, Edge):
            edge = graphical_item

            if edge.start_node and edge in edge.start_node.outward_edges:
                edge.start_node.outward_edges.remove(edge)
            if edge.end_node and edge in edge.end_node.inward_edges:
                edge.end_node.inward_edges.remove(edge)

            self.__scene.removeItem(edge)


        self.update()





    #########################################################################
    """ Mouse Events """


    def __get_mouse_pos_item(self):
        current_point = self.mapFromGlobal(QCursor.pos())
        pos = self.mapToScene(current_point)
        graphical_item = self.itemAt(current_point)
        return graphical_item, pos

    def mouseDoubleClickEvent(self, event):
        if event.buttons() != Qt.MouseButton.LeftButton:
            return

        graphical_item, _ = self.__get_mouse_pos_item()

        # Find Parent of Items until it's either node or edge
        while graphical_item and not isinstance(graphical_item, (Node, Edge)):
            graphical_item = graphical_item.parentItem()

        if isinstance(graphical_item, Node):
            if graphical_item.id != 'C' or graphical_item.id!='R':
                self.__change_node_id(graphical_item)
        elif isinstance(graphical_item, Edge):
            self.__change_edge_weight(graphical_item)


    def mousePressEvent(self, event):
        graphical_item, pos = self.__get_mouse_pos_item()

        # Adds Node in Empty Space on left click
        if event.button() == Qt.MouseButton.LeftButton:

            if graphical_item is None and not self.__delete_mode:
                self.__add_node(pos.x(), pos.y())
            elif graphical_item is not None and self.__delete_mode:
                self.__delete_item(graphical_item)


        elif event.button() == Qt.MouseButton.RightButton and graphical_item is not None:

            while not isinstance(graphical_item , Node):
                graphical_item = graphical_item.parentItem()

            # Creates Edge
            if isinstance(graphical_item, Node) and graphical_item.id != 'C':
                self.__dragged_edge = Edge(start_node=graphical_item)
                self.__scene.addItem(self.__dragged_edge)
                self.__scene.update(self.__dragged_edge.boundingRect())
                self.__dragged_edge.update_path(None)

        super().mousePressEvent(event)



    def mouseMoveEvent(self, event):
        _ , pos = self.__get_mouse_pos_item()


        # Check if the mouse is over a node
        items = self.__scene.items(pos)
        node = next((
                item if isinstance(item, Node)
                else item.parentItem()
                for item in items
                if isinstance(item, Node) or (item.parentItem() and isinstance(item.parentItem(), Node))
            ), None)

        # Drag Edge in the canvas
        if event.buttons() & Qt.MouseButton.RightButton and self.__dragged_edge:
            self.__dragged_edge.update_path(pos)
            self.__scene.update(self.__dragged_edge.boundingRect())

        # Moves Node in the canvas
        elif event.buttons() & Qt.MouseButton.LeftButton and isinstance(node, Node):
            self.__change_node_pos(node, pos.x(), pos.y())

        super().mouseMoveEvent(event)




    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.__dragged_edge:
            _, pos = self.__get_mouse_pos_item()

            print (len(self.__dragged_edge.start_node.outward_edges))

            items = self.__scene.items(pos)

            # Extracts the node at the cursor on release
            node = next((
                item if isinstance(item, Node)
                else item.parentItem()
                for item in items
                if isinstance(item, Node) or (item.parentItem() and isinstance(item.parentItem(), Node))
            ), None)


            if isinstance(node, Node) and node.id != 'R':
                self.__dragged_edge.end_node = node
                node.add_inward_edge(self.__dragged_edge)
                self.__dragged_edge.update_path(None)
                self.__scene.update(self.__dragged_edge.boundingRect())
            else:
                # Remove the edge if no node is found
                self.__scene.removeItem(self.__dragged_edge)
                self.__dragged_edge.start_node.outward_edges.remove(self.__dragged_edge)


            self.__dragged_edge = None

        super().mouseReleaseEvent(event)























































