import wx
from project_manager    import ProjectManager
from windows_capture    import CaptureWindow
from windows_report     import ReportWindow
from windows_projects   import WindowsProjects
from windows_imports    import FileImporter

class MainApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(400, 300))
        self.project_manager = ProjectManager()
        
        # Configuración de la interfaz principal
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Botones de la interfaz
        self.create_project_button      = wx.Button(self.panel, label="Crear Proyecto", size=(200, 30))
        self.open_capture_button        = wx.Button(self.panel, label="Capturar de Imágenes", size=(200, 30))
        self.open_import_button         = wx.Button(self.panel, label="Importar imagenes", size=(200, 30))
        self.create_report_button       = wx.Button(self.panel, label="Crear Informe", size=(200, 30))
        self.save_project_button        = wx.Button(self.panel, label="Guardar Proyecto", size=(200, 30))
        self.open_project_reader_button = wx.Button(self.panel, label="Abrir Lista de Proyectos", size=(200, 30))

        # Añadir botones al sizer
        self.sizer.Add(self.create_project_button, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.open_capture_button, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.open_import_button, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.create_report_button, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.save_project_button, 0, wx.ALL | wx.CENTER, 5)
        self.sizer.Add(self.open_project_reader_button, 0, wx.ALL | wx.CENTER, 5)

        # Eventos
        self.create_project_button.Bind(wx.EVT_BUTTON, self.on_create_project)
        self.open_capture_button.Bind(wx.EVT_BUTTON, self.open_capture_window)
        self.open_import_button.Bind(wx.EVT_BUTTON, self.on_open_import)
        self.create_report_button.Bind(wx.EVT_BUTTON, self.on_create_report)
        self.save_project_button.Bind(wx.EVT_BUTTON, self.on_save_project)
        self.open_project_reader_button.Bind(wx.EVT_BUTTON, self.on_open_project_reader)

        self.panel.SetSizer(self.sizer)
        self.Centre()

    def on_close(self, event):
        """Cerrar la aplicación."""
        self.Destroy()

    def on_create_project(self, event):
        """Crear un nuevo proyecto y abrir la ventana de captura."""
        dialog = wx.TextEntryDialog(self, 'Nombre del nuevo proyecto:', 'Crear Proyecto')
        if dialog.ShowModal() == wx.ID_OK:
            project_name = dialog.GetValue()
            institution = wx.GetTextFromUser('Nombre de la institución:', 'Crear Proyecto')
            if project_name and institution:
                self.project_manager.create_project(project_name, institution)
                #self.open_capture_window()

    def open_capture_window(self, event=None):
        """Abrir la ventana de captura de imágenes."""
        if self.project_manager.active_project is None:
            wx.MessageBox("No hay ningún proyecto activo. Crea un proyecto primero.", "Error", wx.OK | wx.ICON_ERROR)
            return
        self.capture_window = CaptureWindow(self, self.project_manager)
        self.capture_window.Show()

    def on_create_report(self, event):
        """Abrir la ventana para crear un informe."""
        if self.project_manager.active_project is None:
            wx.MessageBox("No hay ningún proyecto activo. Crea un proyecto primero.", "Error", wx.OK | wx.ICON_ERROR)
            return
        self.report_window = ReportWindow(self, self.project_manager)
        self.report_window.Show()

    def on_save_project(self, event):
        """Guardar el proyecto activo."""
        active_project_name = self.project_manager.active_project

        if active_project_name is None:
            wx.MessageBox("No hay ningún proyecto activo.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Guardar el proyecto
        self.project_manager.save_project(active_project_name)
        wx.MessageBox(f"Proyecto '{active_project_name}' guardado con éxito.", "Guardado", wx.OK | wx.ICON_INFORMATION)

    def on_open_project_reader(self, event):
        # Aquí llamamos a la clase WindowsProjects que ya has definido
        projects_window = WindowsProjects(self)  # Asegúrate que el 
        projects_window.Show()

    def on_open_import(self, event):
        self.project_manager.import_images()

    def on_close(self, event):
        """Método para manejar el cierre de la ventana principal."""
        if self.capture_window and self.capture_window.camera_running:
            self.capture_window.camera_running = False
            self.capture_window.camera_capture.stop_capture()
        self.Destroy()
        wx.GetApp().ExitMainLoop()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainApp(None, title="Gestor de Proyectos de Imagen")
    frame.Show()
    app.MainLoop()
