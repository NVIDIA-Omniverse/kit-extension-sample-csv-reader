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
from omni.kit.window import file_importer

CURRENT_PATH = Path(__file__).parent
DATA_PATH = CURRENT_PATH.parent.parent.parent.joinpath("data")

categoryColors = {
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

shapeUSDAName = {
    "cube": "BasicCubeAsRef.usda",
    "sphere": "BasicSphereAsRef.usda",
}


class MainModel():
    def __init__(self):
        
        #root prim paths
        self.rootUrl = '/World'
        self.clusterLayerRoot = '/Class_'
        
        # stage_unit defines the number of unit per meter
        self.stage_unit_per_meter = 1

        # Default CSV Path (sample file deployed with extension)
        self.CSVFilePath = DATA_PATH.joinpath('CSVSample.csv')
        
        # path to basic shape
        self.shapeFileName = "BasicCubeAsRef.usda"
        self.ShapeFilePath = DATA_PATH.joinpath(self.shapeFileName)
        
        # Scale factor so that the shapes are well spaced
        self.scaleDataConverter = 100.0

        # limit the number of elts read
        self.maxElements = 5000
        
        # whether or not the shapes should be grouped by cluster
        self.groupByCluster = False

        #  max number of different color clusters
        self.maxNumberOfCluster = 10

    def Generate(self):
        
        # Clear the stage
        stage = omni.usd.get_context().get_stage()
        primRoot = stage.GetPrimAtPath(self.rootUrl)
        if (primRoot.IsValid()):
            stage.RemovePrim(self.rootUrl)

        # create a new stage with Y up and in meters
        if omni.usd.get_context().new_stage() is False:
            carb.log_warn(f"failing creating a new stage")
            return None
                
        stage = omni.usd.get_context().get_stage()
        #  set the up axis
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
        #  set the unit of the world
        UsdGeom.SetStageMetersPerUnit(stage, self.stage_unit_per_meter)
        # define the root prim
        stage.DefinePrim(self.rootUrl)
        # Define the root prim as the default
        rootPrim = stage.GetPrimAtPath(self.rootUrl)
        stage.SetDefaultPrim(rootPrim)

        # add a light
        stage = omni.usd.get_context().get_stage()
        LightUrl = self.rootUrl + '/DistantLight'
        newLight = UsdLux.DistantLight.Define(stage, LightUrl)
        newLight.CreateAngleAttr(0.53)
        newLight.CreateColorAttr(Gf.Vec3f(1.0, 1.0, 0.745))
        newLight.CreateIntensityAttr(5000.0)

        # check that CSV exists
        if os.path.exists(self.CSVFilePath):
            # Read CSV file
            with open(self.CSVFilePath, newline='') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                i = 1
                #Iterate over each row in the CSV file
                #   Skip the header row
                #   Don't read more than the max number of elements
                #   Create the shape with the appropriate color at each coordinate
                for row in itertools.islice(csvReader, 1, self.maxElements):
                    name = row[0]
                    x = float(row[1])
                    y = float(row[2])
                    z = float(row[3])
                    cluster = row[4]
                    
                    # root prim
                    primClusterUrl = self.rootUrl

                    # add group to path if the user has selected that option
                    if self.groupByCluster:                    
                        primClusterUrl += self.clusterLayerRoot + cluster
                    
                    primCluster = stage.GetPrimAtPath(primClusterUrl)

                    #create the prim if it does not exist
                    if not primCluster.IsValid():
                        UsdGeom.Xform.Define(stage, primClusterUrl)
                        
                    shapeUrl = primClusterUrl + '/box_%d' % i
                    i += 1

                    #Create reference prim
                    refShape = stage.OverridePrim(shapeUrl)

                    #Create instance to reference prim
                    refShape.GetReferences().AddReference(str(self.ShapeFilePath), '/MyRef/RefMesh')
                                    
                    #Get mesh from shape instance
                    nextShape = UsdGeom.Mesh.Get(stage, shapeUrl)

                    #Set location
                    nextShape.AddTranslateOp().Set(
                        Gf.Vec3f(
                            self.scaleDataConverter*x, 
                            self.scaleDataConverter*y,
                            self.scaleDataConverter*z))

                    #Set Color
                    nextShape.GetDisplayColorAttr().Set(
                        categoryColors[int(cluster) % self.maxNumberOfCluster])                  
            
    # Handles the change between a cube and sphere shape in the UI
    def ShapeChanged(self, _comboVal_ShapeDefaultAsRef):
        key_list_shape = list(shapeUSDAName)
        self.shapeFileName = shapeUSDAName[key_list_shape[_comboVal_ShapeDefaultAsRef]]
        self.ShapeFilePath = DATA_PATH.joinpath(self.shapeFileName)

    # Handles the change of the 'group by cluster' checkbox
    def GroupByClusterChanged(self, _bool_checkboxVal_ClassGroup_):
        self.groupByCluster = _bool_checkboxVal_ClassGroup_
    
    # Handles the click of the Load button
    def SelectFile(self):
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

        self.CSVFilePath = fullpath
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
