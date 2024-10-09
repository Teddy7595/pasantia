import wx
import os
import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

class FileImporter(wx.Frame):
    def __init__(self, parent, title):
        super(FileImporter, self).__init__(parent, title=title, size=(400, 200))
        self.images = []  # Referencia al manejador de proyectos

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Botón para abrir el diálogo de selección de archivos
        self.import_button = wx.Button(panel, label="Importar Imágenes")
        self.import_button.Bind(wx.EVT_BUTTON, self.on_import_images)
        sizer.Add(self.import_button, 0, wx.ALL | wx.CENTER, 15)

        # Caja de texto para mostrar las rutas de los archivos seleccionados
        self.file_paths_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(350, 100))
        sizer.Add(self.file_paths_text, 0, wx.ALL | wx.EXPAND, 10)

        panel.SetSizer(sizer)
        self.Centre()
        self.Show()

    def on_import_images(self, event):
        with wx.FileDialog(self, "Selecciona imágenes", wildcard="Archivos de imagen (*.jpg;*.png)|*.jpg;*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as file_dialog:

            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return

            file_paths = file_dialog.GetPaths()
            self.file_paths_text.SetValue("\n".join(file_paths))

            for file_path in file_paths:
                # Leer la imagen desde el archivo
                image = self.load_image(file_path)

                if image is not None:
                    # Codificar la imagen en base64
                    image_base64 = self.encode_image_to_base64(image)
                    if image_base64:
                        self.add_image_to_list(image)

    def load_image(self, file_path):
        try:
            # Abrir la imagen con PIL y convertir a array de numpy
            pil_image = Image.open(file_path)
            pil_image = pil_image.convert('RGB')  # Asegurarse de que la imagen esté en formato RGB
            image_np = np.array(pil_image, dtype=np.uint8)  # Convertir a numpy array con tipo uint8
            print(f"Imagen cargada correctamente: {image_np.shape}")
            return image_np
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            return None

    def encode_image_to_base64(self, image):
        try:
            # Asegúrate de que la imagen sea un array de numpy antes de usar imencode
            if isinstance(image, np.ndarray):
                _, buffer = cv2.imencode('.jpg', image)
                image_base64 = base64.b64encode(buffer).decode('utf-8')
                return image_base64
            else:
                wx.MessageBox(f"La imagen no es correcta", "Error", wx.OK | wx.ICON_ERROR)
                return None
        except Exception as e:
            wx.MessageBox(f"Error al codificar la imagen: {e}", "Error", wx.OK | wx.ICON_ERROR)
            return None
    
    def add_image_to_list(self, image):
        print(f"Tipo de la imagen: {type(image)}, dtype: {image.dtype}, shape: {image.shape}")
        
        if not isinstance(image, np.ndarray):
            print("Error: La imagen no es un array de numpy")
            return

        if image.dtype != np.uint8:
            print("Convirtiendo la imagen a tipo uint8")
            image = image.astype(np.uint8)

        # Redimensionar la imagen si es demasiado grande
        image = cv2.resize(image, (640, 480))

        # Convertir a RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        try:
            _, buffer = cv2.imencode('.jpg', image)
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            print("Imagen codificada correctamente")
            self.images.append(image_base64)
        except Exception as e:
            wx.MessageBox(f"Error al codificar la imagen: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def get_images(self):
        return self.images