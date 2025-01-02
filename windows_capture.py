import wx
import cv2
from threading import Thread
from camera_capture import CameraCapture

class CaptureWindow(wx.Frame):
    def __init__(self, parent, project_manager):
        super().__init__(parent, title='Captura de Imágenes', size=(840, 680))
        self.project_manager = project_manager
        self.camera_capture = None
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.image_ctrl = wx.StaticBitmap(self.panel)
        self.sizer.Add(self.image_ctrl, 0, wx.ALL | wx.TOP, 5)

        self.capture_button = wx.Button(self.panel, label="Capturar Imagen")
        self.close_button = wx.Button(self.panel, label="Cerrar")
        self.sizer.Add(self.capture_button, 0, wx.ALL | wx.BOTTOM, 5)
        self.sizer.Add(self.close_button, 0, wx.ALL | wx.BOTTOM, 5)

        self.capture_button.Bind(wx.EVT_BUTTON, self.on_capture)
        self.close_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.panel.SetSizer(self.sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.camera_running = False
        self.select_camera()

    def select_camera(self):
        cameras = CameraCapture.list_cameras()
        if not cameras:
            wx.MessageBox("No se encontraron cámaras.", "Error", wx.OK | wx.ICON_ERROR)
            self.Destroy()
            return

        dialog = wx.SingleChoiceDialog(self, "Seleccione una cámara", "Cámaras disponibles", [str(c) for c in cameras])
        if dialog.ShowModal() == wx.ID_OK:
            camera_index = int(dialog.GetStringSelection())
            self.camera_capture = CameraCapture(camera_index)
            if self.camera_capture.is_opened():
                self.start_camera()
            else:
                wx.MessageBox("No se pudo abrir la cámara seleccionada.", "Error", wx.OK | wx.ICON_ERROR)
                self.Destroy()
        else:
            self.Destroy()

    def start_camera(self):
        self.camera_running = True
        Thread(target=self.update_frame, daemon=True).start()

    def update_frame(self):
        while self.camera_running:
            frame = self.camera_capture.get_frame()
            if frame is not None:
                height, width = frame.shape[:2]
                bitmap = wx.Bitmap.FromBuffer(width, height, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                wx.CallAfter(self.image_ctrl.SetBitmap, bitmap)
            wx.CallAfter(self.Refresh)

    def on_capture(self, event):
        frame = self.camera_capture.get_frame()
        if frame is not None:
            self.project_manager.add_image_to_active_project(frame)
            wx.MessageBox("Imagen capturada y añadida al proyecto.", "Información", wx.OK | wx.ICON_INFORMATION)

    def on_close(self, event):
        """Método para manejar el cierre de la ventana de captura."""
        self.camera_running = False  # Detener el bucle de la cámara
        if self.camera_capture:
            self.camera_capture.stop_capture()
        self.Destroy()
