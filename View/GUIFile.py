from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QFrame, QScrollArea, QGridLayout, QPushButton, QInputDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen
import DBFunctions  # Assuming this handles JSON read operations
import Utility_Functions  # Assuming this handles JSON write operations


class UMLCanvas(QWidget):
    def __init__(self, parent=None, project_data=None):
        super().__init__(parent)
        self.project_data = project_data
        self.class_positions = {}

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        # Draw relationships as lines
        for relationship in self.project_data['relationships']:
            source_class = relationship['source']
            destination_class = relationship['destination']
            if source_class in self.class_positions and destination_class in self.class_positions:
                source_pos = self.class_positions[source_class]
                destination_pos = self.class_positions[destination_class]
                # Draw line between source and destination
                # Connect the center of the boxes
                painter.drawLine(source_pos.x() + 100, source_pos.y() + 30,  # Center of source box
                                 destination_pos.x() + 100, destination_pos.y() + 30)  # Center of destination box

    def set_class_position(self, class_name, position):
        """Set the position of a class box."""
        self.class_positions[class_name] = position


class UMLWindow(QMainWindow):
    def __init__(self, project_data):
        super().__init__()
        self.setWindowTitle("UML Editor")
        self.setGeometry(100, 100, 800, 600)

        # Scroll area for UML diagram
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.setCentralWidget(scroll_area)

        # Main widget for layout
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)

        # Grid layout for UML diagram
        grid_layout = QGridLayout(main_widget)
        grid_layout.setHorizontalSpacing(150)  # Increased spacing between class boxes
        grid_layout.setVerticalSpacing(100)

        # Create UML canvas
        self.canvas = UMLCanvas(self, project_data)
        main_widget.setLayout(grid_layout)

        row, col = 0, 0
        for uml_class in project_data['classes']:
            class_box = self.create_class_box(uml_class)
            grid_layout.addWidget(class_box, row, col)

            # Use the class box's position after layout is finalized
            class_box.setStyleSheet("background-color: lightgray;")  # Optional: Add a background color for visibility
            class_box.adjustSize()  # Ensure the box size is adjusted before calculating position
            class_box.updateGeometry()  # Update the geometry to ensure accurate positions

            # Get the top-left corner position of the class box
            class_pos = class_box.mapToGlobal(class_box.rect().topLeft())
            self.canvas.set_class_position(uml_class['name'], QPoint(class_pos.x(), class_pos.y()))

            if col == 2:  # Adjust column width as necessary
                col = 0
                row += 1
            else:
                col += 1

        # Set the canvas as the layout's widget to ensure painting occurs
        grid_layout.addWidget(self.canvas, row + 1, 0, 1, 3)  # Add canvas below the class boxes
        self.show()

    def create_class_box(self, uml_class):
        """Creates a visual representation of a class."""
        class_frame = QFrame(self)
        class_frame.setFrameShape(QFrame.Box)
        class_layout = QVBoxLayout(class_frame)

        class_name_label = QLabel(uml_class['name'], self)
        class_layout.addWidget(class_name_label)

        for field in uml_class['fields']:
            field_label = QLabel(f"+ {field['name']}", self)
            class_layout.addWidget(field_label)

        for method in uml_class['methods']:
            method_label = QLabel(f"- {method['name']}()", self)
            class_layout.addWidget(method_label)

        class_frame.setLayout(class_layout)  # Set layout for class_frame
        return class_frame


class FilePromptWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Prompt")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.open_button = QPushButton("Open Existing File")
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

        self.new_button = QPushButton("Create New File")
        self.new_button.clicked.connect(self.create_file)
        layout.addWidget(self.new_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    def open_file(self):
        filepath, _ = QInputDialog.getText(self, 'Open File', 'Enter the file path:')
        if filepath:
            try:
                project_data = DBFunctions.json_read_file(filepath)
                print("Loaded project data:", project_data)
                self.uml_window = UMLWindow(project_data)
                self.uml_window.show()
                self.close()  # Close the file prompt window
            except Exception as e:
                print(f"Error loading file: {e}")

    def create_file(self):
        filepath, _ = QInputDialog.getText(self, 'Create File', 'Enter the file path:')
        if filepath:
            try:
                Utility_Functions.create_project_data_file(filepath)
                project_data = DBFunctions.json_read_file(filepath)  # Load the newly created file
                print("Created and loaded project data:", project_data)
                self.uml_window = UMLWindow(project_data)
                self.uml_window.show()
                self.close()  # Close the file prompt window
            except Exception as e:
                print(f"Error creating file: {e}")


if __name__ == "__main__":
    app = QApplication([])

    window = FilePromptWindow()
    app.exec_()