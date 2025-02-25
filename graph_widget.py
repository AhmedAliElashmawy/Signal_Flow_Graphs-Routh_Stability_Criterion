from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QGraphicsPolygonItem
)
from PyQt6.QtGui import QPen, QPolygonF
import math
from PyQt6.QtCore import Qt, QPointF

class Arrow(QGraphicsLineItem):
    def __init__(self, start_x, start_y, end_x, end_y, parent=None):
        super().__init__(parent)
        self.setLine(start_x, start_y, end_x, end_y)
        self.arrowhead = None
        self.source_id = None
        self.target_id = None
        self.setPen(QPen(Qt.GlobalColor.black, 2))
        self._draw_arrowhead()

    def _draw_arrowhead(self):

        line = self.line()
        angle = math.atan2(line.dy(), line.dx())

        arrow_size = 10
        arrow_p1 = line.p2() - QPointF(math.cos(angle) * arrow_size, math.sin(angle) * arrow_size)
        arrow_p2 = QPointF(
            arrow_p1.x() - math.cos(angle - math.pi / 6) * arrow_size,
            arrow_p1.y() - math.sin(angle - math.pi / 6) * arrow_size,
        )
        arrow_p3 = QPointF(
            arrow_p1.x() - math.cos(angle + math.pi / 6) * arrow_size,
            arrow_p1.y() - math.sin(angle + math.pi / 6) * arrow_size,
        )

        polygon = QPolygonF([line.p2(), arrow_p2, arrow_p3])
        self.arrowhead = QGraphicsPolygonItem(polygon)
        self.arrowhead.setBrush(Qt.GlobalColor.black)
        if self.scene():
            self.scene().addItem(self.arrowhead)

    def setLine(self, *args):
        super().setLine(*args)
        self._draw_arrowhead()


class Text(QGraphicsTextItem):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setDefaultTextColor(Qt.GlobalColor.black)

class DraggableNode(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, node_id, parent=None):
        super().__init__(x - radius, y - radius, 2 * radius, 2 * radius, parent)
        self.node_id = node_id
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setBrush(Qt.GlobalColor.blue)
        self.edges = []  # Store connected edges
        self.text_items = []  # Store associated text items
        self.node_text = None  # Store node label text item

    def add_edge(self, edge, text_item):
        self.edges.append(edge)
        if text_item:
            self.text_items.append(text_item)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        
        # Get updated node position
        pos = self.pos() + QPointF(40, 40)
        
        # Update node label position
        if self.node_text:
            self.node_text.setPos(self.pos() + QPointF(40, 40))
        
        for edge, text in zip(self.edges, self.text_items):
            # Remove old arrowhead
            if edge.arrowhead:
                edge.scene().removeItem(edge.arrowhead)
                edge.arrowhead = None
                
            line = edge.line()
            
            # Update edge position
            if self.node_id == edge.source_id:
                edge.setLine(pos.x(), pos.y(), line.x2(), line.y2())
            else:
                edge.setLine(line.x1(), line.y1(), pos.x(), pos.y())

            # Update text position
            new_line = edge.line()
            text.setPos((new_line.x1() + new_line.x2()) / 2, 
                        (new_line.y1() + new_line.y2()) / 2 - 10)


class GraphWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.node_items = {}  # Store node items
        self.edges = []  # Store edges for path tracking

    def add_node(self, node_id, x, y, radius=20):
        if node_id in self.node_items:
            return None  # Don't create duplicate nodes
        
        node = DraggableNode(x, y, radius, node_id)
        self.scene.addItem(node)
        self.node_items[node_id] = node
        
        # Correctly position the text above the node
        text_item = Text(str(node_id))
        text_item.setPos(x - 10, y - 12)  # Adjusted position
        self.scene.addItem(text_item)
        node.node_text = text_item
        
        return node

    def add_edge(self, node1_id, node2_id, gain=1):
        if node1_id not in self.node_items or node2_id not in self.node_items:
            return None

        node1 = self.node_items[node1_id]
        node2 = self.node_items[node2_id]
        
        # Get current positions of nodes
        pos1 = node1.pos() + QPointF(40, 40)
        pos2 = node2.pos() + QPointF(40, 40)
        edge = Arrow(pos1.x(), pos1.y(), pos2.x(), pos2.y())
        edge.source_id = node1_id
        edge.target_id = node2_id
        self.scene.addItem(edge)
        self.scene.addItem(edge.arrowhead)
        self.edges.append(edge)

        text_item = Text(str(gain))
        text_item.setPos((pos1.x() + pos2.x()) / 2, (pos1.y() + pos2.y()) / 2 - 10)
        self.scene.addItem(text_item)

        node1.add_edge(edge, text_item)
        node2.add_edge(edge, text_item)
        
        return edge

    def num_nodes(self):
        return len(self.node_items)

    def get_node_position(self, node_id):
        if node_id in self.node_items:
            node = self.node_items[node_id]
            pos = node.pos() + QPointF(40, 40)
            return (pos.x(), pos.y())
        return None

