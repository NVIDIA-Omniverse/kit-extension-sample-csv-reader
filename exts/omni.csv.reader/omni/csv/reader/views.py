#  import from omniverse
import omni.ui as ui
from omni.ui.workspace_utils import TOP
#  import from other extension py
from .models import MainModel


class MainView():
    def __init__(self, csvmodel: MainModel):
        self._window = ui.Window("CSV Reader", width=800, height=600, dockPreference=ui.DockPreference.RIGHT_TOP)
        self._window.visible = True
        csvmodel.csv_field_model = None

        with self._window.frame:
            with ui.VStack(alignment=TOP, style={"margin":5}):
                # 2 - parameters to be set, in case not default values
                with ui.VStack():
                    with ui.HStack(height=20):           
                        ui.Label("CSV file path:", height=10, width=120)             
                        self.csv_field = ui.StringField(height=10)
                        self.csv_field.enabled = False
                        self.csv_field.model.set_value(str(csvmodel.csv_file_path))
                        csvmodel.csv_field_model = self.csv_field.model
                        ui.Button("Load", 
                                width=40,
                                clicked_fn=lambda: csvmodel.select_file())
                    with ui.HStack(height=20):
                        ui.Label("Shape:", height=0)
                        shape_combo = ui.ComboBox(0, "cube", "sphere")
                        shape_combo.model.add_item_changed_fn(
                            lambda m, 
                            f=shape_combo: csvmodel.shape_changed(m.get_item_value_model().get_value_as_int()))
                    with ui.HStack(height=20):
                        ui.Label("Group By Cluster:", height=0)
                        cluster_cb = ui.CheckBox(width=20)
                        cluster_cb.model.add_value_changed_fn(
                            lambda a: csvmodel.group_by_cluster_changed(a.get_value_as_bool()))

                ui.Line(style={"color": 0xff00b976}, height=20)
                # 3 - button to populate the 3D scene
                ui.Button( "Generate", height=50, clicked_fn=lambda: csvmodel.generate())
    
    def destroy(self):
        self._window.destroy()
        self._window = None
