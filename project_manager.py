import json
import base64
import os
import cv2
import numpy as np
import wx

class ProjectManager:
    
    def __init__(self):
        self.projects = {}
        self.active_project = None

    def create_project(self, name, institution):
        if name in self.projects:
            print(f"El proyecto '{name}' ya existe.")
            return
        
        self.projects[name] = {
            'name': name,
            'institution': institution,
            'images': []
        }
        self.active_project = name
        print(f"Proyecto '{name}' creado.")

    def add_image_to_active_project(self, image):
        if self.active_project is None:
            print("No hay ningún proyecto activo.")
            return

        # Convertir la imagen a base64
        _, buffer = cv2.imencode('.jpg', image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        self.projects[self.active_project]['images'].append(image_base64)
        print(f"Imagen añadida al proyecto '{self.active_project}'.")

    def save_project(self, name):
        if name not in self.projects:
            print(f"Proyecto '{name}' no existe.")
            return

        project_data = self.projects[name]
        with open(f"{os.path.dirname(__file__)}\projects\{name}.json", 'w') as file:
            json.dump(project_data, file, indent=4)  # Añadido indentación para legibilidad
        print(f"Proyecto '{name}' guardado.")

    def load_project(self, name):
        try:
            with open(f"{name}.json", 'r') as file:
                project_data = json.load(file)
            
            # Decodificar imágenes
            if 'images' in project_data:
                for i in range(len(project_data['images'])):
                    image_base64 = project_data['images'][i]
                    image_bytes = base64.b64decode(image_base64)
                    nparr = np.frombuffer(image_bytes, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    project_data['images'][i] = image

            self.projects[name] = project_data
            self.active_project = name
            print(f"Proyecto '{name}' cargado.")
        except FileNotFoundError:
            print(f"Proyecto '{name}' no encontrado.")
        except json.JSONDecodeError:
            print(f"Error al decodificar el archivo de proyecto '{name}.json'.")
        except Exception as e:
            print(f"Error al cargar el proyecto '{name}': {e}")

    def import_images(self):
        app = wx.App(False)
        frame = wx.Frame(None, title="Importar Imágenes", size=(600, 400))
        panel = wx.Panel(frame)
        
        open_button = wx.Button(panel, label="Seleccionar Imágenes")
        open_button.Bind(wx.EVT_BUTTON, self.on_import_images)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(open_button, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

        frame.Show()
        app.MainLoop()

    def on_import_images(self, event):
        dialog = wx.FileDialog(None, "Selecciona las imágenes", wildcard="*.jpg;*.png;*.bmp", style=wx.FD_OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
            for path in paths:
                image = cv2.imread(path)
                if image is not None:
                    print(f"Imagen cargada correctamente: {image.shape}")
                    self.add_image_to_active_project(image)
                else:
                    print(f"Error al cargar la imagen desde '{path}'")
        dialog.Destroy()