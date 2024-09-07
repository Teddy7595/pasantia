import wx
import cv2
import numpy as np

class CameraApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(CameraApp, self).__init__(*args, **kw)

        self.cap = cv2.VideoCapture(0)  # Captura desde la cámara predeterminada
        self.cap.set(cv2.CAP_PROP_FPS, 60)  # Configurar la tasa de fotogramas
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.SetDoubleBuffered(True)
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la cámara")

        # Configurar la ventana y el panel
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.image_ctrl = wx.StaticBitmap(self.panel)
        self.sizer.Add(self.image_ctrl, 0, wx.ALL | wx.CENTER, 5)

        # Botón para capturar una imagen
        capture_btn = wx.Button(self.panel, label='Capturar Imagen')
        capture_btn.Bind(wx.EVT_BUTTON, self.on_capture)
        self.sizer.Add(capture_btn, 0, wx.ALL | wx.CENTER, 5)

        # Configuración final de la ventana
        self.panel.SetSizerAndFit(self.sizer)
        self.Show()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_frame, self.timer)
        self.timer.Start(30)

    def update_frame(self, event):
        ret, frame = self.cap.read()
        if ret:
            # Convertir la imagen a formato wx
            height, width = frame.shape[:2]
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bitmap = wx.Bitmap.FromBuffer(width, height, image)
            self.image_ctrl.SetBitmap(bitmap)
            self.panel.Layout()

    def on_capture(self, event):
        ret, frame = self.cap.read()
        if ret:
            date_str = wx.DateTime.Now().Format("%Y%m%d_%H%M%S")
            cv2.imwrite(f'{date_str}.jpg', frame)  # Guardar la imagen capturada
            print(f"Imagen capturada y guardada como '{date_str}.jpg'.")

    def on_close(self, event):
        self.timer.Stop()
        self.cap.release()
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = CameraApp(None, title="Aplicación de Cámara con WxPython y OpenCV")
    frame.Bind(wx.EVT_CLOSE, frame.on_close)
    app.MainLoop()
