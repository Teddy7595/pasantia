import wx

class ReportWindow(wx.Frame):
    def __init__(self, parent, project_manager):
        super().__init__(parent, title='Crear Informe', size=(400, 300))
        self.project_manager = project_manager
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Campos de texto para el informe
        self.report_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.sizer.Add(self.report_text, 1, wx.ALL | wx.EXPAND, 5)

        # Botón para guardar el informe
        self.save_button = wx.Button(self.panel, label="Guardar Informe")
        self.sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)

        # Evento de guardado
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save_report)

        self.panel.SetSizer(self.sizer)
        self.Centre()

    def on_save_report(self, event):
        report_content = self.report_text.GetValue()

        # Asegúrate de que active_project es el nombre del proyecto
        active_project_name = self.project_manager.active_project

        if active_project_name is None:
            wx.MessageBox("No hay ningún proyecto activo.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Obtener el proyecto activo del diccionario de proyectos
        active_project = self.project_manager.projects.get(active_project_name)

        if active_project is None:
            wx.MessageBox("Proyecto activo no encontrado.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Asegúrate de que existe una lista para almacenar los informes
        if 'reports' not in active_project:
            active_project['reports'] = []

        # Añadir el contenido del informe al proyecto activo
        active_project['reports'].append(report_content)
        wx.MessageBox("Informe guardado en el proyecto.", "Guardado", wx.OK | wx.ICON_INFORMATION)

