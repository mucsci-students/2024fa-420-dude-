import MongoFunctions
import Utility_Functions
import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsTextItem, QVBoxLayout, QDialog, QPushButton, QLineEdit,
    QLabel, QMainWindow, QWidget, QMessageBox
)
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF
from PyQt5.QtWidgets import QGraphicsLineItem


# Makes box in the window when a class is created.
class ClassBox(QGraphicsRectItem):
    def __init__(self, name, attributes):
        super(ClassBox, self).__init__()

        self.name = name
        self.attributes = attributes
        self.setRect(0, 0, 200, 100)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable)

        # Draw the class name at the top
        self.text = QGraphicsTextItem(self.name, self)
        self.text.setPos(10, 10)

        # Draw attributes below the class name
        self.attr_text = QGraphicsTextItem(self.format_attributes(), self)
        self.attr_text.setPos(10, 40)

        # Relationships will be stored here
        self.relationships = []

    def format_attributes(self):
        return "\n".join(self.attributes)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    def remove_relationship(self, relationship):
        self.relationships.remove(relationship)

# Lines made when you create a relationship.
class RelationshipLine(QGraphicsLineItem):
    def __init__(self, class_box_a, class_box_b):
        super(RelationshipLine, self).__init__()

        self.class_box_a = class_box_a
        self.class_box_b = class_box_b

        self.class_box_a.add_relationship(self)
        self.class_box_b.add_relationship(self)

        self.update_line()
    # Functionality for arealtionship line.
    def update_line(self):
        start_point = self.class_box_a.rect().bottomLeft() + self.class_box_a.pos()
        end_point = self.class_box_b.rect().topLeft() + self.class_box_b.pos()

        self.setLine(QLineF(start_point, end_point))

    def boundingRect(self):
        return QRectF(self.class_box_a.rect().bottomLeft() + self.class_box_a.pos(),
                      self.class_box_b.rect().topLeft() + self.class_box_b.pos()).normalized()

    def paint(self, painter, option, widget=None):
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(self.line())

# Creates GUI instance when GUI is selected.
class UMLScene(QGraphicsScene):
    MIN_DISTANCE = 500  # Minimum distance between boxes

    def __init__(self):
        super(UMLScene, self).__init__()
        self.setSceneRect(0, 0, 800, 600)

    def add_class_box(self, position=None):
        dialog = ClassDialog()
        if dialog.exec_():
            name = dialog.get_class_name()
            attributes = dialog.get_attributes()

            class_box = ClassBox(name, attributes)

            if not position:
                position = self.find_non_overlapping_position(class_box)

            class_box.setPos(position)
            self.addItem(class_box)
    # Handles finding a random spaw position for a new box.
    def find_non_overlapping_position(self, class_box):
        """Find a random position that doesn't overlap with existing class boxes."""
        max_attempts = 100
        for _ in range(max_attempts):
            random_x = random.uniform(0, self.width() - class_box.rect().width())
            random_y = random.uniform(0, self.height() - class_box.rect().height())
            new_position = QPointF(random_x, random_y)

            if self.is_position_valid(new_position, class_box):
                return new_position

        # If no valid position is found after max_attempts, return a default position
        return QPointF(10, 10)
    # Checks to make sure a position is valid before creating it.
    def is_position_valid(self, new_position, class_box):
        """Check if the position is valid (i.e., no overlap with existing boxes)."""
        new_rect = class_box.rect().translated(new_position)

        for item in self.items():
            if isinstance(item, ClassBox):
                existing_rect = item.sceneBoundingRect()
                if new_rect.intersects(existing_rect):
                    # Check if the boxes are too close
                    distance = (new_position - item.pos()).manhattanLength()
                    if distance < self.MIN_DISTANCE:
                        return False

        return True
    
# Needed to make the GUI flow.
class UMLGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super(UMLGraphicsView, self).__init__(scene)
        self.setRenderHint(QPainter.Antialiasing, True)

# Dialog for creating a class.
class ClassDialog(QDialog):
    def __init__(self):
        super(ClassDialog, self).__init__()

        self.setWindowTitle("Create Class")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Class Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.attr_label = QLabel("Attributes (comma separated):")
        self.attr_input = QLineEdit()
        self.layout.addWidget(self.attr_label)
        self.layout.addWidget(self.attr_input)

        self.submit_button = QPushButton("Create")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_class_name(self):
        return self.name_input.text()

    def get_attributes(self):
        return [attr.strip() for attr in self.attr_input.text().split(",")]

# Dialog for creating a relationship.
class RelationshipDialog(QDialog):
    def __init__(self, class_boxes):
        super(RelationshipDialog, self).__init__()

        self.setWindowTitle("Create Relationship")
        self.layout = QVBoxLayout()

        self.label_a = QLabel("Class A Name:")
        self.input_a = QLineEdit()
        self.layout.addWidget(self.label_a)
        self.layout.addWidget(self.input_a)

        self.label_b = QLabel("Class B Name:")
        self.input_b = QLineEdit()
        self.layout.addWidget(self.label_b)
        self.layout.addWidget(self.input_b)

        self.submit_button = QPushButton("Create Relationship")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_selected_classes(self):
        return self.input_a.text(), self.input_b.text()

class UMLApp(QMainWindow):
    def __init__(self):
        super(UMLApp, self).__init__()

        self.scene = UMLScene()
        self.view = UMLGraphicsView(self.scene)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.layout.addWidget(self.view)

        self.create_button = QPushButton("Create Class")
        self.create_button.clicked.connect(self.on_create_class)
        self.layout.addWidget(self.create_button)

        self.create_relationship_button = QPushButton("Create Relationship")
        self.create_relationship_button.clicked.connect(self.on_create_relationship)
        self.layout.addWidget(self.create_relationship_button)

        self.setWindowTitle("UML Class Diagram Editor")
        self.setGeometry(100, 100, 900, 600)

    def on_create_class(self):
        self.scene.add_class_box()

    def on_create_relationship(self):
        class_boxes = [item for item in self.scene.items() if isinstance(item, ClassBox)]
        if len(class_boxes) < 2:
            QMessageBox.warning(self, "Warning", "Need at least two classes to create a relationship.")
            return

        relationship_dialog = RelationshipDialog(class_boxes)
        if relationship_dialog.exec_():
            class_a_name, class_b_name = relationship_dialog.get_selected_classes()
            if not class_a_name or not class_b_name:
                QMessageBox.warning(self, "Warning", "Please enter both class names.")
                return
            
            class_box_a = next((box for box in class_boxes if box.name == class_a_name), None)
            class_box_b = next((box for box in class_boxes if box.name == class_b_name), None)

            if class_box_a and class_box_b:
                relationship = RelationshipLine(class_box_a, class_box_b)
                self.scene.addItem(relationship)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UMLApp()
    main_window.show()
    sys.exit(app.exec_())


