# Model related
# Python built-in
import os.path
import carb
from pathlib import Path
# external python lib
import csv
import itertools
# USD imports
from pxr import Gf, UsdGeom, UsdLux
# omniverse
import omni.client
import omni.kit.app
from omni.kit.window.file_importer import get_file_importer

CURRENT_PATH = Path(__file__).parent
DATA_PATH = CURRENT_PATH.parent.parent.parent.joinpath("data")

category_colors = {
    0: [(1, 0, 0)],
    1: [(0, 1, 0)],
    2: [(0, 0.4, 0)],
    3: [(0, 0, 1)],
    4: [(0.3, 0.5, 1)],
    5: [(.5, .5, .5)],
    6: [(0, 0, 0)],
    7: [(0, 1, 1)],
    8: [(.8, .5, .25)],
    9: [(1, .5, 0)],
    10: [(1, 1, 1)],
}

shape_usda_name = {
    "cube": "BasicCubeAsRef.usda",
    "sphere": "BasicSphereAsRef.usda",
}


class MainModel():
    def __init__(self):
        
        #root prim paths
        self.root_path = '/World'
        self.cluster_layer_root_path = '/Class_'
        
        # stage_unit defines the number of unit per meter
        self.stage_unit_per_meter = 1

        # Default CSV Path (sample file deployed with extension)
        self.csv_file_path = DATA_PATH.joinpath('CSVSample.csv')
        
        # path to basic shape
        self.shape_file_name = "BasicCubeAsRef.usda"
        self.shape_file_path = DATA_PATH.joinpath(self.shape_file_name)
        
        # Scale factor so that the shapes are well spaced
        self.scale_factor = 100.0

        # limit the number of rows read
        self.max_elements = 5000
        
        # whether or not the shapes should be grouped by cluster
        self.group_by_cluster = False

        #  max number of different color clusters
        self.max_num_clusters = 10

    def generate(self):
        # Clear the stage

        # create a new stage with Y up and in meters

        #  set the up axis

        #  set the unit of the world

        # add a light

        # check that CSV exists

            # Read CSV file

                # Iterate over each row in the CSV file
                #   Skip the header row
                #   Don't read more than the max number of elements
                #   Create the shape with the appropriate color at each coordinate
                    
                    # root prim

                    # add group to path if the user has selected that option

                    # create the prim if it does not exist

                    # Create prim to add the reference to.

                    # Add the reference
                                    
                    # Get mesh from shape instance

                    # Set location

                    # Set Color
        pass          
            
    # Handles the change between a cube and sphere shape in the UI
    def shape_changed(self, choice):
        chosen_key = list(shape_usda_name.keys())[choice]
        self.shape_file_name = shape_usda_name[chosen_key]
        self.shape_file_path = DATA_PATH.joinpath(self.shape_file_name)

    # Handles the change of the 'group by cluster' checkbox
    def group_by_cluster_changed(self, do_clustering):
        self.group_by_cluster = do_clustering
    
    # Handles the click of the Load button
    def select_file(self):
        self.file_importer = get_file_importer()
        self.file_importer.show_window(
            title="Select a CSV File",
            import_button_label="Select",
            import_handler=self._on_click_open,
            file_extension_types=[(".csv", "CSV Files (*.csv)")],
            file_filter_handler=self._on_filter_item
            )

    # Handles the click of the open button within the file importer dialog
    def _on_click_open(self, filename: str, dirname: str, selections):
        
        # File name should not be empty.
        filename = filename.strip()
        if not filename:
            carb.log_warn(f"Filename must be provided.")
            return

        # create the full path to csv file
        if dirname:
            fullpath = f"{dirname}{filename}"
        else:
            fullpath = filename

        self.csv_file_path = fullpath
        self.csv_field_model.set_value(str(fullpath))

    # Handles the filtering of files within the file importer dialog
    def _on_filter_item(self, filename: str, filter_postfix: str, filter_ext: str) -> bool:
        if not filename:
            return True
        # Show only .csv files
        _, ext = os.path.splitext(filename)
        if ext == filter_ext:
            return True
        else:
            return False
