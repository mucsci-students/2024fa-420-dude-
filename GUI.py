import DBFunctions
import Utility_Functions
import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsTextItem, QVBoxLayout, QDialog, QPushButton, QLineEdit,
    QLabel, QMainWindow, QWidget, QMessageBox, QInputDialog
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
        return "".join(self.attributes)

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

    # Handles finding a random spaw position for a new box to make sure of no overlapings.
    def find_non_overlapping_position(self, class_box):
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
    
    # Handles deleting the class box.
    def delete_class_box(self):
        selected_items = self.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Warning", "No class box selected.")
            return

        for item in selected_items:
            if isinstance(item, ClassBox):
                # Remove relationships connected to the class box
                for relationship in item.relationships[:]:
                    self.removeItem(relationship)
                    relationship.class_box_a.remove_relationship(relationship)
                    relationship.class_box_b.remove_relationship(relationship)

                # Remove the class box itself
                self.removeItem(item)

    # Handles renaming a class.
    def rename_class_box(self):
        selected_items = self.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "Warning", "No class box selected.")
            return

        for item in selected_items:
            if isinstance(item, ClassBox):
                # Show dialog to input the new name
                new_name, ok = QInputDialog.getText(None, "Rename Class", "Enter new class name:")
                if ok and new_name:
                    item.name = new_name
                    item.text.setPlainText(new_name)  # Update the displayed name

    
# Needed to make the GUI flow.
class UMLGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super(UMLGraphicsView, self).__init__(scene)
        self.setRenderHint(QPainter.Antialiasing, True)

# Dialog to create a field.
class AddFieldDialog(QDialog):
    def __init__(self):
        super(AddFieldDialog, self).__init__()

        self.setWindowTitle("Add Field")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("Field Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.submit_button = QPushButton("Add Field")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_field_name(self):
        return self.name_input.text()

# Dialog to create a method.
class AddMethodDialog(QDialog):
    def __init__(self):
        super(AddMethodDialog, self).__init__()

        self.setWindowTitle("Add Method")
        self.layout = QVBoxLayout()

        # Method name
        self.name_label = QLabel("Method Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        # Parameters (comma-separated)
        self.params_label = QLabel("Parameters (comma separated):")
        self.params_input = QLineEdit()
        self.layout.addWidget(self.params_label)
        self.layout.addWidget(self.params_input)

        # Submit button
        self.submit_button = QPushButton("Add Method")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_method_name(self):
        return self.name_input.text()

    def get_parameters(self):
        return [param.strip() for param in self.params_input.text().split(",")]

# Dialog to create a class.
class ClassDialog(QDialog):
    def __init__(self):
        super(ClassDialog, self).__init__()

        self.setWindowTitle("Create Class")
        self.layout = QVBoxLayout()

        # Class name
        self.name_label = QLabel("Class Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        # Attributes list (for methods)
        self.methods_list = []  # To store methods
        self.fields_list = []      # To store fields separately

        self.attributes_display = QLabel("Attributes:\n")
        self.layout.addWidget(self.attributes_display)

        # Add attribute button
        self.add_attribute_button = QPushButton("Add Attribute")
        self.add_attribute_button.clicked.connect(self.on_add_attribute)
        self.layout.addWidget(self.add_attribute_button)

        # Submit button
        self.submit_button = QPushButton("Create Class")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def on_add_attribute(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Pick Type")
        msg_box.setText("Select Attribute Type:")
        field_button = msg_box.addButton("Field", QMessageBox.ActionRole)
        method_button = msg_box.addButton("Method", QMessageBox.ActionRole)
        msg_box.exec_()

        if msg_box.clickedButton() == field_button:
            self.add_field()
        elif msg_box.clickedButton() == method_button:
            self.add_method()

    def add_field(self):
        field_dialog = AddFieldDialog()
        if field_dialog.exec_():
            field_name = field_dialog.get_field_name()
            if field_name:
                self.fields_list.append(field_name)  # Store field in fields_list
                self.update_attributes_display()

    def add_method(self):
        method_dialog = AddMethodDialog()
        if method_dialog.exec_():
            method_name = method_dialog.get_method_name()
            parameters = method_dialog.get_parameters()
            if method_name:
                param_list = ", ".join(parameters)
                self.methods_list.append(f"{method_name}({param_list})")  # Store method in attributes_list
                self.update_attributes_display()

    def update_attributes_display(self):
        fields_text = ", ".join([f"{field}" for field in self.fields_list])
        methods_text = "\n".join([f"{method}" for method in self.methods_list])

        attributes_text = "Attributes:\n" + "Fields: " + fields_text + "\nMethods: " + methods_text
        self.attributes_display.setText(attributes_text)

    def get_attributes(self):
        fields_text = ", ".join(self.fields_list) if self.fields_list else "None"
        methods_text = ", ".join([f"{method}" for method in self.methods_list]) if self.methods_list else "None"
        return f"Fields: {fields_text}\nMethods:\n{methods_text}"


    # Returns class name.
    def get_class_name(self):
        return self.name_input.text()

     # Returns the list of fields
    def get_fields(self):
        return self.fields_list  


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

        self.label_c = QLabel("Relationship Type:")
        self.input_c = QLineEdit()
        self.layout.addWidget(self.label_c)
        self.layout.addWidget(self.input_c)

        self.submit_button = QPushButton("Create Relationship")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_selected_classes(self):
        return self.input_a.text(), self.input_b.text()
    
    def get_type(self):
        return self.input_c.text()

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

        # Code to create all buttons.

        self.create_button = QPushButton("Create Class")
        self.create_button.clicked.connect(self.on_create_class)
        self.layout.addWidget(self.create_button)

        self.delete_button = QPushButton("Delete Class")
        self.delete_button.clicked.connect(self.on_delete_class)
        self.layout.addWidget(self.delete_button)

        self.rename_button = QPushButton("Rename Class")
        self.rename_button.clicked.connect(self.on_rename_class)
        self.layout.addWidget(self.rename_button)

        self.create_relationship_button = QPushButton("Create Relationship")
        self.create_relationship_button.clicked.connect(self.on_create_relationship)
        self.layout.addWidget(self.create_relationship_button)

        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.on_save)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.on_load)
        self.layout.addWidget(self.load_button)
        


        self.setWindowTitle("UML Class Diagram Editor")
        self.setGeometry(100, 100, 900, 600)

    def on_create_class(self):
        self.scene.add_class_box()

    def on_delete_class(self):
        # Gets the selected item in the scene
        selected_items = self.scene.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a class to delete.")
            return

        # Assume we are dealing with ClassBox instances
        for item in selected_items:
            if isinstance(item, ClassBox):
                # Remove the associated relationships from the scene as well
                for relationship in item.relationships:
                    self.scene.removeItem(relationship)
                    item.remove_relationship(relationship)

                # Remove the class box itself
                self.scene.removeItem(item)


    def on_rename_class(self):
        # Get the selected items in the scene
        selected_items = self.scene.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a class to rename.")
            return

        # Assume we are dealing with ClassBox instances
        for item in selected_items:
            if isinstance(item, ClassBox):
                # Get the current name
                current_name = item.name
            
                # Prompt the user for a new name
                new_name, ok = QInputDialog.getText(self, "Rename Class", "Enter new class name:", text=current_name)
            
                if ok and new_name:  # Ensure the dialog was not cancelled and the new name is not empty
                    # Update the class box's name
                    item.name = new_name
                
                    # Update the displayed text in the graphics scene
                    item.text.setPlainText(new_name)


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
            if (relationship_dialog.get_type() != "Aggregation") and  (relationship_dialog.get_type() != "Composition") and (relationship_dialog.get_type() != "Realization") and (relationship_dialog.get_type() != "Inheritance"):
                QMessageBox.warning(self, "Warning", "Please enter a valid type.")
                return
            class_box_a = next((box for box in class_boxes if box.name == class_a_name), None)
            class_box_b = next((box for box in class_boxes if box.name == class_b_name), None)

            if class_box_a and class_box_b:
                relationship = RelationshipLine(class_box_a, class_box_b)
                self.scene.addItem(relationship)

    def on_save(self):
        '''Add code to save to json file'''

    def on_load(self):
        '''Add code to load from json file'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UMLApp()
    main_window.show()
    sys.exit(app.exec_())


