import wx

class ReportApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Gestión de Informes y Proyectos', size=(800, 600))
        
        # Configuración de la ventana principal
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Panel de visualización de imágenes
        self.image_panel = wx.Panel(self.panel)
        self.image_panel.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.image_sizer = wx.BoxSizer(wx.VERTICAL)
        self.image_display = wx.StaticBitmap(self.image_panel)
        self.image_sizer.Add(self.image_display, 1, wx.EXPAND | wx.ALL, 5)
        self.image_panel.SetSizer(self.image_sizer)

        # Panel de anotaciones
        self.annotation_panel = wx.Panel(self.panel)
        self.annotation_sizer = wx.BoxSizer(wx.VERTICAL)
        self.annotation_label = wx.StaticText(self.annotation_panel, label="Anotaciones:")
        self.annotation_text = wx.TextCtrl(self.annotation_panel, style=wx.TE_MULTILINE)
        self.save_button = wx.Button(self.annotation_panel, label="Guardar Anotaciones")
        self.annotation_sizer.Add(self.annotation_label, 0, wx.ALL, 5)
        self.annotation_sizer.Add(self.annotation_text, 1, wx.EXPAND | wx.ALL, 5)
        self.annotation_sizer.Add(self.save_button, 0, wx.ALL | wx.CENTER, 5)
        self.annotation_panel.SetSizer(self.annotation_sizer)

        # Panel lateral para informes/proyectos
        self.project_panel = wx.Panel(self.panel)
        self.project_sizer = wx.BoxSizer(wx.VERTICAL)
        self.project_label = wx.StaticText(self.project_panel, label="Informes/Proyectos:")
        self.project_list = wx.ListBox(self.project_panel, choices=["Proyecto 1", "Informe 2"], style=wx.LB_SINGLE)
        self.attach_button = wx.Button(self.project_panel, label="Adjuntar Documento")
        self.project_sizer.Add(self.project_label, 0, wx.ALL, 5)
        self.project_sizer.Add(self.project_list, 1, wx.EXPAND | wx.ALL, 5)
        self.project_sizer.Add(self.attach_button, 0, wx.ALL | wx.CENTER, 5)
        self.project_panel.SetSizer(self.project_sizer)

        # Añadir los paneles al sizer principal
        self.sizer.Add(self.image_panel, 2, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.annotation_panel, 3, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.project_panel, 2, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(self.sizer)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_button)
        self.Bind(wx.EVT_BUTTON, self.on_attach, self.attach_button)

        self.Centre()
        self.Show()

    def on_save(self, event):
        # Lógica para guardar anotaciones
        annotations = self.annotation_text.GetValue()
        print("Anotaciones guardadas:", annotations)

    def on_attach(self, event):
        # Lógica para adjuntar documentos
        with wx.FileDialog(self, "Adjuntar documento", wildcard="Documentos (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # El usuario canceló
            pathname = fileDialog.GetPath()
            print("Documento adjuntado:", pathname)


if __name__ == '__main__':
    app = wx.App(False)
    frame = ReportApp()
    app.MainLoop()
