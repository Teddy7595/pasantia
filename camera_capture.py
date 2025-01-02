import cv2

class CameraCapture:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)

    def start_capture(self):
        if not self.cap.isOpened():
            self.cap.open(self.camera_index)

    def stop_capture(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def is_opened(self):
        return self.cap.isOpened()

    def __del__(self):
        self.stop_capture()

    @staticmethod
    def list_cameras():
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr
