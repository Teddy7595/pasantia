import json
import wx
import os
from windows_viewer import WindowsViewer

from wx.lib import scrolledpanel

class WindowsProjects(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Listado de Proyectos", size=(350, 400))

        self.panel = scrolledpanel.ScrolledPanel(self, style=wx.VSCROLL)
        self.panel.SetupScrolling()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Project directory path
        self.projects_dir = f"{os.path.dirname(__file__)}\projects"
        self.load_projects()

        # Asignar el sizer al panel scrollable
        self.panel.SetSizer(self.sizer)

        # Añadir el panel scrollable al frame
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

        # Center and show the window
        self.Centre()
        self.Show()
        
    def load_projects(self):
        
        if not os.path.exists(self.projects_dir):
            wx.MessageBox(f"La carpeta '{self.projects_dir}' no existe.", "Error", wx.OK | wx.ICON_ERROR)
            return

        for project in os.listdir(self.projects_dir):
            button = wx.Button(self.panel, label=project, size=(200, 30))
            button.Bind(wx.EVT_BUTTON, lambda event, path=f"{self.projects_dir}/{project}": self.open_project(path))
            self.sizer.Add(button, 0, wx.ALL | wx.CENTER, 5)

        # Actualizar el tamaño virtual del panel scrollable
        self.panel.SetupScrolling(scroll_x=False, scroll_y=True)
        self.panel.SetVirtualSize((300, len(os.listdir(self.projects_dir)) * 50))

    def open_project(self, project_path):
        with open(project_path, 'r') as file:
            project_data = json.loads(file.read())

        frame = WindowsViewer(None, "Visor de Imágenes y Reporte", project_data["images"], project_data["reports"][0])
        frame.Show() 
