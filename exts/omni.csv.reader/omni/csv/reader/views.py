# UI related
from ctypes import alignment
#  import from omniverse
import omni.ui as ui
from omni.ui.workspace_utils import LEFT, RIGHT, TOP
#  import from other extension py
from .models import MainModel


class MainView():
    def __init__(self, csvmodel: MainModel):
        self._window = ui.Window(
                                "CSV Reader", width=800, height=600,
                                dockPreference=ui.DockPreference.RIGHT_TOP
                                 )

        self._window.visible = True
        csvmodel.csv_field_model = None

        with self._window.frame:
            with ui.VStack(alignment=TOP, style={"margin":5}):
                # 2 - parameters to be set, in case not default values
                with ui.VStack():

                    with ui.HStack(height=20):           
                        ui.Label("CSV file path:", height=10, width=120)             
                        self.CsvField = ui.StringField(height=10)
                        self.CsvField.enabled = False
                        self.CsvField.model.set_value(str(csvmodel.CSVFilePath))
                        csvmodel.csv_field_model = self.CsvField.model
                        ui.Button("Load", 
                                width=40,
                                clicked_fn=lambda: csvmodel.SelectFile())

                    with ui.HStack(height=20):
                        ui.Label("Shape:", height=0)
                        ShapeDefaultAsRef = ui.ComboBox(0, "cube", "sphere")
                        ShapeDefaultAsRef.model.add_item_changed_fn(
                            lambda m, 
                            f=ShapeDefaultAsRef: csvmodel.ShapeChanged(
                                m.get_item_value_model().get_value_as_int()))
                
                    with ui.HStack(height=20):
                        ui.Label("Group By Cluster:", height=0)
                        ChoiceCheckBoxWithClass = ui.CheckBox(width=20)
                        ChoiceCheckBoxWithClass.model.add_value_changed_fn(
                            lambda a: csvmodel.GroupByClusterChanged(
                                a.get_value_as_bool()))

                ui.Line(style={"color": 0xff00b976}, height=20)
                # 3 - buttons to generate the 3D scene populated
                ui.Button( "Generate",
                            height=50,
                            clicked_fn=lambda: csvmodel.Generate())

    def destroy(self):
        self._window.destroy()
        self._window = None
