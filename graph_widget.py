from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt, QPointF

class DraggableNode(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, node_id, parent=None):
        super().__init__(x - radius, y - radius, 2 * radius, 2 * radius, parent)
        self.node_id = node_id
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setBrush(Qt.GlobalColor.blue)
        self.edges = []  # Store connected edges
        self.text_items = []  # Store associated text items

    def add_edge(self, edge, text_item):
        self.edges.append(edge)
        if text_item:
            self.text_items.append(text_item)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Update edge positions
        pos = self.pos() + QPointF(self.rect().width()/2, self.rect().height()/2)
        
        for edge, text in zip(self.edges, self.text_items):
            line = edge.line()
            # Update line position based on whether this node is source or target
            if self.node_id == edge.source_id:
                edge.setLine(pos.x(), pos.y(), line.x2(), line.y2())
            else:
                edge.setLine(line.x1(), line.y1(), pos.x(), pos.y())
            # Update text position
            text.setPos((line.x1() + line.x2())/2, (line.y1() + line.y2())/2)

class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.nodes = {}  # Dictionary to store node positions
        self.node_items = {}  # Store node items

    def add_node(self, node_id, x, y, radius=20):
        node = DraggableNode(x, y, radius, node_id)
        self.scene.addItem(node)
        self.nodes[node_id] = (x, y)
        self.node_items[node_id] = node
        return node

    def add_edge(self, node1_id, node2_id, gain=1):
        if node1_id not in self.nodes or node2_id not in self.nodes:
            return None
            
        x1, y1 = self.nodes[node1_id]
        x2, y2 = self.nodes[node2_id]
        
        edge = QGraphicsLineItem(x1, y1, x2, y2)
        edge.setPen(QPen(Qt.GlobalColor.black, 2))
        edge.source_id = node1_id  # Store source node id
        edge.target_id = node2_id  # Store target node id
        self.scene.addItem(edge)

        # Display gain text
        text_item = self.scene.addText(f"{gain}")
        text_item.setPos((x1 + x2) / 2, (y1 + y2) / 2)

        # Add edge to both nodes
        self.node_items[node1_id].add_edge(edge, text_item)
        self.node_items[node2_id].add_edge(edge, text_item)
        
        return edge

    def get_node_position(self, node_id):
        return self.nodes.get(node_id)
