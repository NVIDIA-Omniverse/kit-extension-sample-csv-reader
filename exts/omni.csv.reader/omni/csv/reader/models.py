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
        stage = omni.usd.get_context().get_stage()
        root_prim = stage.GetPrimAtPath(self.root_path)
        if (root_prim.IsValid()):
            stage.RemovePrim(self.root_path)

        # create a new stage with Y up and in meters
        if omni.usd.get_context().new_stage() is False:
            carb.log_warn(f"Failed creating a new stage.")
            return
                
        stage = omni.usd.get_context().get_stage()
        #  set the up axis
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
        #  set the unit of the world
        UsdGeom.SetStageMetersPerUnit(stage, self.stage_unit_per_meter)
        stage.SetDefaultPrim(root_prim)

        # add a light
        light_prim_path = self.root_path + '/DistantLight'
        light_prim = UsdLux.DistantLight.Define(stage, light_prim_path)
        light_prim.CreateAngleAttr(0.53)
        light_prim.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 0.745))
        light_prim.CreateIntensityAttr(5000.0)

        # check that CSV exists
        if os.path.exists(self.csv_file_path):
            # Read CSV file
            with open(self.csv_file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=',')
                i = 1
                # Iterate over each row in the CSV file
                #   Skip the header row
                #   Don't read more than the max number of elements
                #   Create the shape with the appropriate color at each coordinate
                for row in itertools.islice(csv_reader, 1, self.max_elements):
                    name = row[0]
                    x = float(row[1])
                    y = float(row[2])
                    z = float(row[3])
                    cluster = row[4]
                    
                    # root prim
                    cluster_prim_path = self.root_path

                    # add group to path if the user has selected that option
                    if self.group_by_cluster:                    
                        cluster_prim_path += self.cluster_layer_root_path + cluster
                    
                    cluster_prim = stage.GetPrimAtPath(cluster_prim_path)

                    # create the prim if it does not exist
                    if not cluster_prim.IsValid():
                        UsdGeom.Xform.Define(stage, cluster_prim_path)
                        
                    shape_prim_path = cluster_prim_path + '/box_%d' % i
                    i += 1

                    # Create prim to add the reference to.
                    ref_shape = stage.OverridePrim(shape_prim_path)

                    # Add the reference
                    ref_shape.GetReferences().AddReference(str(self.shape_file_path), '/MyRef/RefMesh')
                                    
                    # Get mesh from shape instance
                    next_shape = UsdGeom.Mesh.Get(stage, shape_prim_path)

                    # Set location
                    next_shape.AddTranslateOp().Set(
                        Gf.Vec3f(
                            self.scale_factor*x, 
                            self.scale_factor*y,
                            self.scale_factor*z))

                    # Set Color
                    next_shape.GetDisplayColorAttr().Set(
                        category_colors[int(cluster) % self.max_num_clusters])                  
            
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
