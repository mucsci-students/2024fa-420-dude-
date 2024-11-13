import sys
from pathlib import Path
import copy

# Add the project root to sys.path dynamically
project_root = Path(__file__).resolve().parent.parent
print(project_root)
sys.path.append(str(project_root))

# Now import Utility_Functions from the Control package
from Control import Utility_Functions as uf
from Model import DBFunctions as dbf
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
    def __init__(self, name, attributes, app_instance):
        super(ClassBox, self).__init__()

        self.name = name
        self.attributes = attributes
        self.uml_app = app_instance
        self.setRect(0, 0, 200, 100)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        # Draw the class name at the top
        self.text = QGraphicsTextItem(self.name, self)
        self.text.setPos(10, 10)

        # Draw attributes below the class name
        self.attr_text = QGraphicsTextItem(self.format_attributes(), self)
        self.attr_text.setPos(10, 40)

        # Relationships will be stored here
        self.relationships = []

        # Adjust size based on text content
        self.adjust_size()

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.ItemPositionHasChanged:
            pos = {
                "x": value.x(),
                "y": value.y(),
            }
            self.uml_app.project_data = dbf.json_update_pos(self.uml_app.project_data, self.name, pos)
            for relationship in self.relationships:
                relationship.update_line()
        return super().itemChange(change, value)


    def format_attributes(self):
        return "".join(self.attributes)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    def remove_relationship(self, relationship):
        self.relationships.remove(relationship)

    def update_attributes_display(self):
        self.attr_text.setPlainText(self.format_attributes())

    def adjust_size(self):
        # Get the bounding rectangles for the text and attribute text items
        name_rect = self.text.boundingRect()
        attr_rect = self.attr_text.boundingRect()

        # Calculate width and height based on the text content
        width = max(name_rect.width(), attr_rect.width()) + 20
        height = name_rect.height() + attr_rect.height() + 30

        # Update the rectangle of the ClassBox
        self.setRect(0, 0, width, height)

# Lines made when you create a relationship.
class RelationshipLine(QGraphicsLineItem):
    def __init__(self, class_box_a, class_box_b, scene):
        super(RelationshipLine, self).__init__()

        self.class_box_a = class_box_a
        self.class_box_b = class_box_b
        self.scene = scene  # Store the scene reference to access items

        self.class_box_a.add_relationship(self)
        self.class_box_b.add_relationship(self)

        self.update_line()

    # Functionality for arealtionship line.
    def update_line(self):
        # Ensure class_box_a is on the left and class_box_b is on the right
        if self.class_box_a.pos().x() > self.class_box_b.pos().x():
            self.class_box_a, self.class_box_b = self.class_box_b, self.class_box_a

        # Calculate start and end points
        start_x = self.class_box_a.rect().right() + self.class_box_a.pos().x()
        start_y = self.class_box_a.rect().center().y() + self.class_box_a.pos().y()
        start_point = QPointF(start_x, start_y)

        end_x = self.class_box_b.rect().left() + self.class_box_b.pos().x()
        end_y = self.class_box_b.rect().center().y() + self.class_box_b.pos().y()
        end_point = QPointF(end_x, end_y)

        # Set initial line
        proposed_line = QLineF(start_point, end_point)

        # Check for intersections with other lines
        if self.intersects_existing_lines(proposed_line):
            # Adjust the line slightly (for demonstration, we’ll offset vertically by 10 pixels)
            start_point.setY(start_point.y() - 10)
            end_point.setY(end_point.y() - 10)
            proposed_line = QLineF(start_point, end_point)

        # Set the adjusted or original line
        self.setLine(proposed_line)

    def intersects_existing_lines(self, new_line):
        """Checks if the new line intersects with any other line in the scene."""
        for item in self.scene.items():
            # Only check against other RelationshipLines
            if isinstance(item, RelationshipLine) and item is not self:
                # Check if lines intersect
                intersect_point = QPointF()
                if new_line.intersect(item.line(), intersect_point) == QLineF.BoundedIntersection:
                    return True
        return False


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

    def __init__(self, app_instance):
        super(UMLScene, self).__init__()
        self.uml_app = app_instance
        self.setSceneRect(0, 0, 800, 600)

    def add_class_box(self, project_data, undo_stack, undo_clicked, redo_stack, position=None):
        dialog = ClassDialog()
        if dialog.exec_():
            name = dialog.get_class_name()
            attributes = dialog.get_attributes()
            any_fields = True
            any_methods = True
            try:
                fields = attributes.split("\n")[0].split(":")[1].split(", ")
            except IndexError:
                any_fields = False
            try:
                methods = attributes.split("\n")[2].split(":")[1].split("\n")
            except IndexError:
                any_methods = False
            if undo_clicked:
                redo_stack.clear()
                undo_clicked = False
            undo_stack.append(copy.deepcopy(project_data))
            project_data = uf.add_class(project_data, name)
            if any_fields:
                if fields[0] != ' None':
                    for field in fields:
                        parts = field.split(" ", 1)
                        type = parts[1].split(" ", 1)[0]
                        field = parts[1].split(" ", 1)[1]
                        project_data = uf.add_field(project_data, name, field, type)
            if any_methods:
                if methods[0] != ' None':
                    for method in methods:
                        # Ensure the method string contains both a return type and method signature
                        parts = method.split(" ", 1)[1].split(" ", 1)
                        # The return type is the first part
                        return_type = parts[0]
                        # Extract method name (before the parentheses)
                        method_name = parts[1].split("(", 1)[0].strip()
                        # Extract parameters (inside the parentheses)
                        parameters_str = parts[1].split("(", 1)[1].split(")", 1)[0].strip()
                        # Split parameters by comma and strip whitespace from each
                        parameters = [param.strip() for param in parameters_str.split(",") if param]
                        # Add the parsed method to the project data
                        project_data = uf.add_method(project_data, name, method_name, parameters, return_type)
          

            class_box = ClassBox(name, attributes, self.uml_app)

            if not position:
                position = self.find_non_overlapping_position(class_box)
            pos = {
                "x": position.x(),
                "y": position.y(),
            }
            project_data = dbf.json_update_pos(project_data, name, pos)
            class_box.setPos(position)
            self.addItem(class_box)
            return (project_data, undo_stack, undo_clicked, redo_stack)

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

        self.type_label = QLabel("Field Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

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
    
    def get_field_type(self):
        return self.type_input.text()

# Dialog to create a method.
class AddMethodDialog(QDialog):
    def __init__(self, existing_parameters=None):
        super(AddMethodDialog, self).__init__()

        self.setWindowTitle("Add Method")
        self.layout = QVBoxLayout()

        # Method name
        self.name_label = QLabel("Method Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.type_label = QLabel("Method Return Type:")
        self.type_input = QLineEdit()
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.type_input)

        # Parameters (comma-separated)
        self.params_label = QLabel("Parameters (comma separated):")
        self.params_input = QLineEdit()
        self.layout.addWidget(self.params_label)
        self.layout.addWidget(self.params_input)

        # If there are existing parameters, populate the input field
        if existing_parameters:
            self.params_input.setText(", ".join(existing_parameters))

        # Submit button
        self.submit_button = QPushButton("Add Method")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_method_name(self):
        return self.name_input.text()

    def get_method_type(self):
        return self.type_input.text()

    def get_str_parameters(self):
        params = []
        for param in self.params_input.text().split(","):
            params.append(param)
        return params

    def get_tuple_parameters(self):
        params = []
        for param in self.params_input.text().split(","):
            param_parts = param.strip().split()  # Split by space and remove extra whitespace
            if len(param_parts) == 2:  # Ensure there are exactly two parts (type and name)
                param_type, param_name = param_parts
                params.append(param_type, param_name)  # Store as a tuple (type, name)
        return params


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

        # Store fields and methods separately
        self.methods_list = []  # To store methods with their parameters
        self.fields_list = []

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
            field_type = field_dialog.get_field_type()
            full_field = field_type + " " +field_name
            if full_field:
                self.fields_list.append(full_field)
                self.update_attributes_display()
        

    def add_method(self, method_name=None, return_type=None, existing_parameters=None):
        method_dialog = AddMethodDialog(existing_parameters=existing_parameters)
        if method_dialog.exec_():
            method_name = method_dialog.get_method_name()
            print(method_name)
            return_type = method_dialog.get_method_type()
            print(return_type)
            parameters = method_dialog.get_str_parameters()
            if method_name:
                method = {"name": method_name, "type": return_type, "parameters": parameters}
                self.methods_list.append(method)
                self.update_attributes_display()

    def update_attributes_display(self):
        fields_text = ", ".join(self.fields_list)
        methods_text = "".join(
            [f"Method: {method['type']} {method['name']}({', '.join(method['parameters'])})" for method in self.methods_list]
        )

        attributes_text = "Attributes:\n" + "Field: " + fields_text + "\n" + methods_text
        self.attributes_display.setText(attributes_text)

    def on_edit_method_parameters(self, project_data, scene):
        original_project_data = project_data
        # Get class name
        class_name, ok1 = QInputDialog.getText(self if isinstance(self, QWidget) else None, "Class Name", "Enter the class name:")
        if not ok1 or not class_name:
            return original_project_data # User canceled or provided no class name

        # Get method name
        method_name, ok2 = QInputDialog.getText(self if isinstance(self, QWidget) else None, "Method Name", "Enter the method name:")
        if not ok2 or not method_name:
            return original_project_data # User canceled or provided no method name

        
        # Search for the class box by class name in backend.
        class_box = dbf.json_get_class(project_data, class_name)

        if class_box is None:
            QMessageBox.warning(self, "Warning", f"Class '{class_name}' not found.")
            return original_project_data

        # Find the method in the class box's attributes (methods)
        method_found = dbf.json_get_method(project_data, class_name, method_name, 1)
        mult_method = dbf.json_get_method_with_same_name(project_data, class_name, method_name)
        method_count = 1
        if len(mult_method) > 1:
            method_count, ok4 = QInputDialog.getText(self if isinstance(self, QWidget) else None, "Which Method", "Enter the method number:")
            if not ok4 or not method_name:
                return original_project_data # User canceled or provided no method count
            method_found = dbf.json_get_method(project_data, class_name, method_name, method_count)


        if method_found is None:
            QMessageBox.warning(self, "Warning", f"Method '{method_name}' not found in class '{class_name}'.")
            return original_project_data\
            
        temp = copy.deepcopy(project_data)

        # Existing parameters
        existing_parameters = dbf.json_get_parameters(project_data, class_name, method_name, method_count)
        formatted_existing_parameters = ""
        if existing_parameters is not None:
            for param in existing_parameters:
                formatted_existing_parameters += param["type"] + " " + param["name"] + ", "
            dbf.json_delete_all_parameters(project_data, class_name, method_name, method_count)
        if len(formatted_existing_parameters) > 0:
            existing_parameters = formatted_existing_parameters[:-2]
        else:
            existing_parameters = "None"
        print("Existing parameters: " + str(existing_parameters))
        print(dbf.json_get_parameters(project_data, class_name, method_name, method_count))
        QMessageBox.information(self, "Info", f"Existing parameters: {existing_parameters}")
        # Let user edit the parameters
        new_parameters, ok3 = QInputDialog.getText(self if isinstance(self, QWidget) else None, "Edit Parameters", "Edit parameters (comma separated):", text=existing_parameters)
        if not ok3:
            return original_project_data # User canceled

        if self.undo_clicked:
            self.redo_stack.clear()
            self.undo_clicked = False
        self.undo_stack.append(copy.deepcopy(temp))

        # Update the method with the new parameters
        if len(new_parameters) > 0:
            print("New parameters: " + str(new_parameters))
            for param in new_parameters.split(","):
                param = param.strip()
                type = param.split(" ")[0]
                name = param.split(" ")[1]
                project_data = uf.add_param(project_data, class_name, method_name, method_count, name, type)

        # Update the class box's attributes display
        scene_box = None
        for item in scene.items():
            if isinstance(item, ClassBox) and item.name == class_name:
                scene_box = item
                break
        fields = dbf.json_get_fields(project_data, class_name)
        methods = dbf.json_get_methods(project_data, class_name)
        attributes = "Fields: "
        if fields is not None:
            for field in fields:
                attributes += field["type"] + " " + field["name"] + ", "
            attributes = attributes[:-2] + "\nMethods:\n"
        else:
            attributes += "None\nMethods:\n"
        if methods is not None:
            for method in methods:
                params = dbf.json_get_parameters(project_data, class_name, method["name"], method_count)
                parameters = ""
                for param in params:
                    parameters += param["type"] + " " + param["name"] + ", "
                if len(parameters) > 0:
                    parameters = parameters[:-2]
                attributes += "Method: " + method["return_type"] + " " + method["name"] + "(" + parameters + ")\n"
        else:
            attributes += "None"
        print(attributes)
        scene_box.attributes = attributes
        scene_box.update_attributes_display()
        scene_box.adjust_size()

        return project_data



    def edit_method(self, method_index):
        method_to_edit = self.methods_list[method_index]
        method_name = method_to_edit['name']
        existing_parameters = method_to_edit['parameters']

        # Re-open dialog to edit method name and parameters
        self.add_method(method_name=method_name, existing_parameters=existing_parameters)

        # Update the method in the list after editing
        self.methods_list[method_index] = {"name": method_name, "parameters": existing_parameters}
        self.update_attributes_display()

    def get_attributes(self):
        fields_text = ", ".join(self.fields_list) if self.fields_list else "None"
        methods_text = "\n".join(
            [f"Method: {method['type']} {method['name']}({', '.join(method['parameters'])})" for method in self.methods_list]
        ) if self.methods_list else "None"
        return f"Fields: {fields_text}\nMethods:\n{methods_text}"


    # Returns class name.
    def get_class_name(self):
        return self.name_input.text()

     # Returns the list of fields
    def get_fields(self):
        return self.fields_list  
    
    def on_save(self, project_data, scene):
        file_path, ok1 = QInputDialog.getText(self if isinstance(self, QWidget) else None, "File Path", "Enter the file path:")
        if not ok1 or not file_path:
            return project_data # User canceled or provided no class name
        # Set the positions for each class box in the project data
        class_boxes = [item for item in scene.items() if isinstance(item, ClassBox)]
        for class_box in class_boxes:
            class_data = dbf.json_get_class(self.project_data, class_box.name)
            if class_data:
                project_data = dbf.json_update_pos(project_data, class_box.name, {"x": class_box.pos().x(), "y": class_box.pos().y()})
        return dbf.json_write_file(file_path, project_data)

    def on_load(self, project_data, scene):
        save = QMessageBox.question(self if isinstance(self, QWidget) else None, "Save", "Would you like to save before loading?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if save == QMessageBox.Cancel:
            return None
        if save == QMessageBox.Yes:
            ClassDialog.on_save(self, project_data, scene)
        file_path, ok1 = QInputDialog.getText(self if isinstance(self, QWidget) else None, "File Path", "Enter the file path:")
        if not ok1 or not file_path:
            return None # User canceled or provided no class name
        project_data = dbf.json_read_file(file_path)
        return project_data


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

# Dialog for deleting a relationship.
class DeleteRelationshipDialog(QDialog):
    def __init__(self, class_boxes):
        super(DeleteRelationshipDialog, self).__init__()

        self.setWindowTitle("Delete Relationship")
        self.layout = QVBoxLayout()

        self.label_a = QLabel("Class A Name:")
        self.input_a = QLineEdit()
        self.layout.addWidget(self.label_a)
        self.layout.addWidget(self.input_a)

        self.label_b = QLabel("Class B Name:")
        self.input_b = QLineEdit()
        self.layout.addWidget(self.label_b)
        self.layout.addWidget(self.input_b)

        self.submit_button = QPushButton("Delete Relationship")
        self.submit_button.clicked.connect(self.accept)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def get_selected_classes(self):
        return self.input_a.text(), self.input_b.text()
    

class UMLApp(QMainWindow):
    def __init__(self):
        super(UMLApp, self).__init__()

        self.project_data = {
            "classes": [],
            "relationships": []
        }
        self.undo_stack = []
        self.undo_clicked = False
        self.redo_stack = []

        self.scene = UMLScene(self)
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

        self.edit_attr_button = QPushButton("Edit Attributes")
        self.edit_attr_button.clicked.connect(lambda: self.on_edit_attr(self.project_data, self.scene))

        self.layout.addWidget(self.edit_attr_button)


        self.edit_method_button = QPushButton("Edit Method Parameters")
        self.edit_method_button.clicked.connect(self.on_edit_method_parameters)
        self.layout.addWidget(self.edit_method_button)

        self.create_relationship_button = QPushButton("Create Relationship")
        self.create_relationship_button.clicked.connect(self.on_create_relationship)
        self.layout.addWidget(self.create_relationship_button)

        self.delete_relationship_button = QPushButton("Delete Relationship")
        self.delete_relationship_button.clicked.connect(self.on_delete_relationship)
        self.layout.addWidget(self.delete_relationship_button)

        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.on_save)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.on_load)
        self.layout.addWidget(self.load_button)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.on_undo)
        self.layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.on_redo)
        self.layout.addWidget(self.redo_button)
        


        self.setWindowTitle("UML Class Diagram Editor")
        self.setGeometry(100, 100, 900, 600)

    def on_create_class(self):
        class_box_return = self.scene.add_class_box(self.project_data, self.undo_stack, self.undo_clicked, self.redo_stack)
        if class_box_return:
            self.project_data = class_box_return[0]
            self.undo_stack = class_box_return[1]
            self.undo_clicked = class_box_return[2]
            self.redo_stack = class_box_return[3]
            print(self.project_data)

    def on_delete_class(self):
        # Gets the selected item in the scene
        selected_items = self.scene.selectedItems()
        print(self.project_data)

        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a class to delete.")
            return
        class_name = selected_items[0].name
        if self.undo_clicked:
            self.redo_stack.clear()
            self.undo_clicked = False
        self.undo_stack.append(copy.deepcopy(self.project_data))
        self.project_data = uf.delete_class(self.project_data, class_name)

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
                    if self.undo_clicked:
                        self.redo_stack.clear()
                        self.undo_clicked = False
                    self.undo_stack.append(copy.deepcopy(self.project_data))
                    self.project_data = uf.update_class_name(self.project_data, current_name, new_name)
                    print(self.project_data)

                    # Update the class box's name
                    item.name = new_name
                
                    # Update the displayed text in the graphics scene
                    item.text.setPlainText(new_name)

    def on_edit_attr(self, project_data, scene):
        # Prompt user to select an action: Add, Delete, Rename
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Edit Attribute")
        msg_box.setText("Pick an Action:")
        add_attr_button = msg_box.addButton("Add", QMessageBox.ActionRole)
        delete_attr_button = msg_box.addButton("Delete", QMessageBox.ActionRole)
        rename_attr_button = msg_box.addButton("Rename", QMessageBox.ActionRole)
        msg_box.exec_()

        # Prompt for the class name
        class_name, ok1 = QInputDialog.getText(self, "Class Name", "Enter the class name:")
        if not ok1 or not class_name:
            return  # User canceled or didn't provide a class name

        # Prompt for attribute type (Field or Method)
        attr_type_msg = QMessageBox()
        attr_type_msg.setWindowTitle("Select Attribute Type")
        attr_type_msg.setText("Is this a Field or a Method?")
        field_button = attr_type_msg.addButton("Field", QMessageBox.ActionRole)
        method_button = attr_type_msg.addButton("Method", QMessageBox.ActionRole)
        attr_type_msg.exec_()

        attr_type = None
        if attr_type_msg.clickedButton() == field_button:
            attr_type = "Field"
        elif attr_type_msg.clickedButton() == method_button:
            attr_type = "Method"

        if not attr_type:
            return  # User canceled or didn't select an attribute type

        if msg_box.clickedButton() == add_attr_button:
            if attr_type == "Field":
                # Create and display the AddFieldDialog
                add_field_dialog = AddFieldDialog()
                if add_field_dialog.exec_() == QDialog.Accepted:  # If the user clicks "Add Field" in the dialog
                    # Retrieve the field details from the dialog
                    field_name = add_field_dialog.get_field_name()
                    field_type = add_field_dialog.get_field_type()

                    # Ensure the field name and type are provided
                    if not field_name or not field_type:
                        QMessageBox.warning(self, "Warning", "Field name and type cannot be empty.")
                        return
                    
                    # Check if the field already exists
                    if dbf.json_get_field(project_data, class_name, field_name) is not None:
                        QMessageBox.warning(self, "Warning", f"Field '{field_name}' already exists in class '{class_name}'.")
                        return

                    # Add the field to the project data
                    project_data = self.add_field(project_data, class_name, field_name, scene, field_type)

            elif attr_type == "Method":
                # Create and display the AddMethodDialog
                add_method_dialog = AddMethodDialog()
                if add_method_dialog.exec_() == QDialog.Accepted:  # If the user clicks "Add Method" in the dialog
                    # Retrieve the method details from the dialog
                    method_name = add_method_dialog.get_method_name()
                    method_type = add_method_dialog.get_method_type()
                    params = add_method_dialog.get_str_parameters()
                    json_formatted_params = []
                    if params[0] == '':
                        params = []
                    else:
                        for param in params:
                            param = param.strip()
                            type = param.split(" ")[0]
                            name = param.split(" ")[1]
                            json_formatted_params.append({ "type": type, "name": name })


                    # Ensure the method name is provided
                    if not method_name:
                        QMessageBox.warning(self, "Warning", "Method name cannot be empty.")
                        return

                    # Add the method to the project data
                    self.project_data = self.add_method(project_data, class_name, method_name, self.scene, method_type, json_formatted_params)

        elif msg_box.clickedButton() == delete_attr_button:
            # Prompt for the attribute name to delete
            attribute_name, ok2 = QInputDialog.getText(self, "Attribute Name", f"Enter the {attr_type.lower()} name to delete:")
            if not ok2 or not attribute_name:
                return  # User canceled or didn't provide an attribute name

            # Delete the attribute based on type
            self.project_data = self.delete_attribute(project_data, class_name, attribute_name, scene, attr_type)

        elif msg_box.clickedButton() == rename_attr_button:
            # Prompt for the attribute name to rename
            attribute_name, ok2 = QInputDialog.getText(self, "Attribute Name", f"Enter the {attr_type.lower()} name to rename:")
            if not ok2 or not attribute_name:
                return  # User canceled or didn't provide an attribute name

            # Prompt for the new name
            new_name, ok3 = QInputDialog.getText(self, "New Attribute Name", f"Enter the new name for the {attr_type.lower()}:")
            if not ok3 or not new_name:
                return  # User canceled or didn't provide a new name

            # Rename the attribute based on type
            self.rename_attribute(project_data, class_name, attribute_name, new_name, scene, attr_type)

    # Functions to handle attribute manipulation directly:
    def add_field(self, project_data, class_name, field_name, scene, attr_type):
        # Check if the class exists
        class_data = dbf.json_get_class(project_data, class_name)
        if class_data is None:
            QMessageBox.warning(self, "Warning", f"Class '{class_name}' not found.")
            return project_data
    
        # Check if the field already exists
        if dbf.json_get_field(project_data, class_name, field_name) is not None:
            QMessageBox.warning(self, "Warning", f"Field '{field_name}' already exists in class '{class_name}'.")
            return project_data


        # Update the project data with the modified class
        if self.undo_clicked:
            self.redo_stack.clear()
            self.undo_clicked = False
        self.undo_stack.append(copy.deepcopy(project_data))
        project_data = uf.add_field(project_data, class_name, field_name, attr_type)

        # Update the UI
        self.update_scene_attributes(scene, project_data, class_name)

            
        return project_data


    def add_method(self, project_data, class_name, method_name, scene, attr_type, params):
        # Check if the method already exists to prevent adding it twice
        existing_methods = dbf.json_get_method_with_same_name(project_data, class_name, method_name)
        if any(method['name'] == method_name and method["params"] == params for method in existing_methods):
            QMessageBox.warning(self, "Warning", f"Method '{method_name}' already exists in class '{class_name}'.")
            return project_data
        
        # Add the method to the project data
        if self.undo_clicked:
            self.redo_stack.clear()
            self.undo_clicked = False
        self.undo_stack.append(copy.deepcopy(project_data))
        project_data = uf.add_method(project_data, class_name, method_name, params, attr_type)
        print(f"Method {method_name} added with params: {params}")

        # Update the UI
        self.update_scene_attributes(scene, project_data, class_name)

        # Confirm the method was added
        QMessageBox.information(self, "Success", f"Method '{method_name}' added to class '{class_name}'.")

        return project_data

    def delete_attribute(self, project_data, class_name, attribute_name, scene, attr_type):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Delete Attribute")
        msg_box.setText("Is the attribute a field or a method?")
        field_button = msg_box.addButton("Field", QMessageBox.ActionRole)
        method_button = msg_box.addButton("Method", QMessageBox.ActionRole)
        msg_box.exec_()
        temp = copy.deepcopy(project_data)
        # Determine if the user selected field or method
        if msg_box.clickedButton() == field_button:
            if self.undo_clicked:
                self.redo_stack.clear()
                self.undo_clicked = False
            self.undo_stack.append(copy.deepcopy(temp))
            project_data = uf.delete_field(project_data, class_name, attribute_name)
            if dbf.json_get_field(project_data, class_name, attribute_name) is None:
                 QMessageBox.information(self, "Success", f"Field '{attribute_name}' deleted.")
        elif msg_box.clickedButton() == method_button:
            mult_method = dbf.json_get_method_with_same_name(project_data, class_name, attribute_name)
            method_count = None
            if len(mult_method) > 0:
                method_count_str, ok = QInputDialog.getText(None, "Which Method", "Enter Method Count:")
                if not ok:
                    QMessageBox.warning(self, "Warning", " count not found.")
                    return project_data
                method_count = int(method_count_str)
            # Call the delete method function
            if self.undo_clicked:
                self.redo_stack.clear()
                self.undo_clicked = False
            self.undo_stack.append(copy.deepcopy(temp))
            project_data = uf.delete_method(project_data, class_name, attribute_name, method_count)
            if dbf.json_get_method(project_data, class_name, attribute_name):
                QMessageBox.information(self, "Success", f"Method '{attribute_name}' deleted.")
        # Update the scene attributes display after deletion
        self.update_scene_attributes(scene, project_data, class_name)
        return project_data


    def rename_attribute(self, project_data, class_name, old_attribute_name, new_name, scene, attr_type):
        # Prompt the user to specify if the attribute is a field or a method
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Rename Attribute")
        msg_box.setText("Is the attribute a field or a method?")
        field_button = msg_box.addButton("Field", QMessageBox.ActionRole)
        method_button = msg_box.addButton("Method", QMessageBox.ActionRole)
        msg_box.exec_()
        temp = copy.deepcopy(project_data)
        # Get the new attribute name from the user
        new_attribute_name, ok = QInputDialog.getText(self, "Rename Attribute", "Enter the new attribute name:")
        if not ok or not new_attribute_name:
            return  # User canceled or didn't provide a new name

        # Determine if the user selected field or method
        if msg_box.clickedButton() == field_button:
            # Call the rename field function
            if uf.update_field_name(project_data, class_name, old_attribute_name, new_attribute_name) is not None:
                if self.undo_clicked:
                    self.redo_stack.clear()
                    self.undo_clicked = False
                self.undo_stack.append(copy.deepcopy(temp))
                QMessageBox.information(self, "Success", f"Field '{old_attribute_name}' renamed to '{new_attribute_name}'.")
            else:
                QMessageBox.warning(self, "Warning", f"Field '{old_attribute_name}' not found in class '{class_name}'.")

        elif msg_box.clickedButton() == method_button:
            mult_method = dbf.json_get_method_with_same_name(project_data, class_name, old_attribute_name)
            method_count = None
            if mult_method > 0:
                method_count_str, ok = QInputDialog.getText(None, "Which Method", "Enter Method Count:")
                if not ok:
                    QMessageBox.warning(self, "Warning", "count not found.")
                    return project_data
                method_count = int(method_count_str)
            # Call the rename method function
            if uf.update_method_name(project_data, class_name, old_attribute_name, new_attribute_name, method_count) is not None:
                if self.undo_clicked:
                    self.redo_stack.clear()
                    self.undo_clicked = False
                self.undo_stack.append(copy.deepcopy(temp))
                QMessageBox.information(self, "Success", f"Method '{old_attribute_name}' renamed to '{new_attribute_name}'.")
            else:
                QMessageBox.warning(self, "Warning", f"Method '{old_attribute_name}' not found in class '{class_name}'.")

        # Update the scene attributes display after renaming
        self.update_scene_attributes(scene, project_data, class_name)


    def update_scene_attributes(self, scene, project_data, class_name):
        fields = dbf.json_get_fields(project_data, class_name)
        methods = dbf.json_get_methods(project_data, class_name)

        attributes = "Fields: "
        
       # Format fields as "type name"
        field_lines = []
        if isinstance(fields, list):
            for field in fields:
                if isinstance(field, dict) and 'name' in field and 'type' in field:
                    field_type = field['type']  # Ensure you get the type correctly
                    field_name = field['name']
                    # Add formatted string to the list
                    field_lines.append(f"{field_type} {field_name}")
        attributes += ", ".join(field_lines) if field_lines else ""
        
        attributes += "\nMethods:\n"

        # Format methods as "return_type name"
        if isinstance(methods, list):
            method_lines = []
            for method in methods:
                if isinstance(method, dict) and 'name' in method and 'return_type' in method:
                    return_type = method['return_type']  # Get the return type
                    method_name = method['name']
                    # Create a string for parameters
                    params = method["params"]
                    formatted_params = "("
                    for param in params:
                        type = param["type"]
                        name = param["name"]
                        formatted_params += f"{type} {name}, "
                    if len(formatted_params) > 1:
                        formatted_params = formatted_params[:-2]
                    formatted_params += ")"
                    # Add formatted string to the list
                    method_line = f"Method: {return_type} {method_name}{formatted_params}"
                    method_lines.append(method_line)
            attributes += "\n".join(method_lines) or "None"

        print("Attributes to be displayed:\n", attributes)  # Debug print

        # Update the ClassBox in the scene
        scene_box = next((item for item in scene.items() if isinstance(item, ClassBox) and item.name == class_name), None)
        if scene_box:
            scene_box.attributes = attributes
            scene_box.update_attributes_display()  # Update the display method
            scene_box.adjust_size()  # Adjust size if needed
        else:
            print(f"No ClassBox found for class '{class_name}' in the scene.")



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
                relationship = RelationshipLine(class_box_a, class_box_b, self.scene)
                self.scene.addItem(relationship)
                if self.undo_clicked:
                    self.redo_stack.clear()
                    self.undo_clicked = False
                self.undo_stack.append(copy.deepcopy(self.project_data))
                self.project_data = uf.add_relationship(self.project_data, class_a_name, class_b_name, relationship_dialog.get_type())
                print(self.project_data)

    def on_edit_method_parameters(self):
        self.project_data = ClassDialog.on_edit_method_parameters(self, self.project_data, self.scene)
        print(self.project_data)

    def on_delete_relationship(self):
        class_boxes = [item for item in self.scene.items() if isinstance(item, ClassBox)]
    
        if len(class_boxes) < 2:
            QMessageBox.warning(self, "Warning", "Need at least two classes to delete a relationship.")
            return

        # Open the relationship dialog to select classes
        relationship_dialog = DeleteRelationshipDialog(class_boxes)
        if relationship_dialog.exec_():
            class_a_name, class_b_name = relationship_dialog.get_selected_classes()
        
            # Ensure both class names are provided
            if not class_a_name or not class_b_name:
                QMessageBox.warning(self, "Warning", "Please enter both class names.")
                return

            # Find the class boxes associated with the selected names
            class_box_a = next((box for box in class_boxes if box.name == class_a_name), None)
            class_box_b = next((box for box in class_boxes if box.name == class_b_name), None)

            if not class_box_a or not class_box_b:
                QMessageBox.warning(self, "Warning", "Could not find the specified classes.")
                return
        
              # Get relationship data from project_data (JSON)
        relationship_data = None
        if dbf.json_get_relationship(self.project_data, class_a_name, class_b_name):
            relationship_data = dbf.json_get_relationship(self.project_data, class_a_name, class_b_name)
        elif dbf.json_get_relationship(self.project_data, class_b_name, class_a_name):
            relationship_data = dbf.json_get_relationship(self.project_data, class_b_name, class_a_name)

        if relationship_data:
            # Find the actual QGraphicsItem (RelationshipLine) in the scene corresponding to the relationship data
            relationship_item = next(
                (item for item in self.scene.items() if isinstance(item, RelationshipLine) and
                 item.class_box_a.name == class_a_name and item.class_box_b.name == class_b_name), 
                None
            )

            if relationship_item:
                # Remove the relationship from the scene
                self.scene.removeItem(relationship_item)
                if self.undo_clicked:
                    self.redo_stack.clear()
                    self.undo_clicked = False
                self.undo_stack.append(copy.deepcopy(self.project_data))
                self.project_data = uf.delete_relationship(self.project_data, class_a_name, class_b_name)
                # Remove the relationship references from both class boxes
                class_box_a.remove_relationship(relationship_item)
                class_box_b.remove_relationship(relationship_item)
                print(f"Relationship between {class_a_name} and {class_b_name} deleted.")
            else:
                QMessageBox.warning(self, "Warning", "Could not find the relationship in the scene.")
        else:
            QMessageBox.warning(self, "Warning", "No relationship found between the selected classes.")


    def on_save(self):
        return ClassDialog.on_save(self, self.project_data, self.scene)

    def on_load(self):
        data = ClassDialog.on_load(self, self.project_data, self.scene)
        if data is None:
            return
        self.scene.clear()
        self.project_data = data
        classes = dbf.json_get_classes(self.project_data)
        for class_ in classes:
            name = class_["name"]
            fields = dbf.json_get_fields(self.project_data, name)
            methods = dbf.json_get_methods(self.project_data, name)
            attributes = "Fields: "
            if fields is not None:
                for field in fields:
                    attributes += field["type"] + " " + field["name"] + ", "
                attributes = attributes[:-2] + "\nMethods:\n"
            else:
                attributes += "None\nMethods:\n"
            methods_used = []
            if methods is not None:
                for method in methods:
                    if method["name"] not in methods_used:
                        mult_method = dbf.json_get_method_with_same_name(self.project_data, name, method["name"])
                        if len(mult_method) > 1:
                            count = 1
                            for method_ in mult_method:
                                params = dbf.json_get_parameters(self.project_data, name, method["name"], count)
                                parameters = ""
                                for param in params:
                                    parameters += param["type"] + " " + param["name"] + ", "
                                if len(parameters) > 0:
                                    parameters = parameters[:-2]
                                attributes += "Method: " + method["return_type"] + " " + method["name"] + "(" + parameters + ")\n"
                                count += 1
                        else:
                            params = dbf.json_get_parameters(self.project_data, name, method["name"], 1)
                            parameters = ""
                            for param in params:
                                parameters += param["type"] + " " + param["name"] + ", "
                            if len(parameters) > 0:
                                parameters = parameters[:-2]
                            attributes += "Method: " + method["return_type"] + " " + method["name"] + "(" + parameters + ")\n"
                        methods_used.append(method["name"])
            else:
                attributes += "None"
            class_box = ClassBox(name, attributes, self)
            position_json = class_["position"]
            position = QPointF(position_json["x"], position_json["y"])
            class_box.setPos(position)
            self.scene.addItem(class_box)

            # Add relationships
            relationships = dbf.json_get_relationships(self.project_data)
            class_boxes = []
            for item in self.scene.items():
                if isinstance(item, ClassBox):
                    class_boxes.append(item)
            for relationship in relationships:
                class_box_a = None
                class_box_b = None
                for class_box in class_boxes:
                    if class_box.name == relationship["source"]:
                        class_box_a = class_box
                    if class_box.name == relationship["destination"]:
                        class_box_b = class_box
                if class_box_a and class_box_b:
                    relationship_line = RelationshipLine(class_box_a, class_box_b)
                    self.scene.addItem(relationship_line)

    def on_undo(self):
        if len(self.undo_stack) > 0:
            self.undo_clicked = True
            self.redo_stack.append(copy.deepcopy(self.project_data))
            self.project_data = self.undo_stack.pop()
            # Clear the scene and draw new data
            self.draw_data()
            print("Redo stack:\n" + str(self.redo_stack))


    def on_redo(self):
        if len(self.redo_stack) > 0:
            self.undo_stack.append(copy.deepcopy(self.project_data))
            self.project_data = self.redo_stack.pop()
            # Clear the scene and draw new data
            self.draw_data()

    def draw_data(self):
        self.scene.clear()
        classes = dbf.json_get_classes(self.project_data)
        for class_ in classes:
            name = class_["name"]
            fields = dbf.json_get_fields(self.project_data, name)
            methods = dbf.json_get_methods(self.project_data, name)
            attributes = "Fields: "
            if fields is not None:
                for field in fields:
                    attributes += field["type"] + " " + field["name"] + ", "
                attributes = attributes[:-2] + "\nMethods:\n"
            else:
                attributes += "None\nMethods:\n"
            methods_used = []
            if methods is not None:
                for method in methods:
                    if method["name"] not in methods_used:
                        mult_method = dbf.json_get_method_with_same_name(self.project_data, name, method["name"])
                        if len(mult_method) > 1:
                            count = 1
                            for method_ in mult_method:
                                params = dbf.json_get_parameters(self.project_data, name, method["name"], count)
                                parameters = ""
                                for param in params:
                                    parameters += param["type"] + " " + param["name"] + ", "
                                if len(parameters) > 0:
                                    parameters = parameters[:-2]
                                attributes += "Method: " + method["return_type"] + " " + method["name"] + "(" + parameters + ")\n"
                                count += 1
                        else:
                            params = dbf.json_get_parameters(self.project_data, name, method["name"], 1)
                            parameters = ""
                            for param in params:
                                parameters += param["type"] + " " + param["name"] + ", "
                            if len(parameters) > 0:
                                parameters = parameters[:-2]
                            attributes += "Method: " + method["return_type"] + " " + method["name"] + "(" + parameters + ")\n"
                        methods_used.append(method["name"])
            else:
                attributes += "None"
            class_box = ClassBox(name, attributes, self)
            position_json = class_["position"]
            position = QPointF(position_json["x"], position_json["y"])
            class_box.setPos(position)
            self.scene.addItem(class_box)

            # Add relationships
            relationships = dbf.json_get_relationships(self.project_data)
            class_boxes = []
            for item in self.scene.items():
                if isinstance(item, ClassBox):
                    class_boxes.append(item)
            for relationship in relationships:
                class_box_a = None
                class_box_b = None
                for class_box in class_boxes:
                    if class_box.name == relationship["source"]:
                        class_box_a = class_box
                    if class_box.name == relationship["destination"]:
                        class_box_b = class_box
                if class_box_a and class_box_b:
                    relationship_line = RelationshipLine(class_box_a, class_box_b)
                    self.scene.addItem(relationship_line)
        
               

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UMLApp()
    main_window.show()
    sys.exit(app.exec_())


