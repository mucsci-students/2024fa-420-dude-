import Utility_Functions as uf
import DBFunctions as dbf

project_data = dbf.json_read_file("json_files/TinyDBTestFile.json")

project_data = uf.display_class(project_data, "Tire")

project_data = uf.display_relationship(project_data, "Car", "Tire")