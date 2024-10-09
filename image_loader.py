import wx
import cv2

class ImageLoader:
    def __init__(self):
        self.current_image = None

    def load_image(self, path):
        self.current_image = cv2.imread(path)
        return self.current_image

    def show_image_dialog(self):
        with wx.FileDialog(None, "Abrir imagen", wildcard="Imagenes (*.png;*.jpg)|*.png;*.jpg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            path = fileDialog.GetPath()
            return self.load_image(path)
