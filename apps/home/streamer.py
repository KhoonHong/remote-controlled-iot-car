import io
import os

class Camera:
    def __init__(self):
        self.is_recording = False
        self.recording_path = None
        self.camera = None

    def init_camera(self):
        if self.camera is None:
            import picamera
            self.camera = picamera.PiCamera(resolution=(640, 480), framerate=24)

    def stream(self):
        self.init_camera()

        try:
            import picamera
            return self.pi_camera_stream()
        except ImportError:
            import cv2
            return self.opencv_stream()

    def pi_camera_stream(self):
        stream = io.BytesIO()
        for _ in self.camera.capture_continuous(stream, format='jpeg', quality=70, use_video_port=True):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
            stream.seek(0)
            stream.truncate()

    def opencv_stream(self):
        import cv2
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                _, jpeg = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        finally:
            cap.release()

    def start_recording(self, save_path="video.h264"):
        self.recording_path = save_path
        if os.path.exists(self.recording_path):
            os.remove(self.recording_path)
        self.init_camera()

        try:
            self.pi_camera_start_recording()
        except AttributeError:
            import cv2
            self.opencv_start_recording()

    def stop_recording(self):
        if self.is_recording:
            try:
                self.pi_camera_stop_recording()
            except AttributeError:
                import cv2
                self.opencv_stop_recording()
            self.is_recording = False

    def pi_camera_start_recording(self):
        if not self.is_recording:
            self.camera.start_recording(self.recording_path, splitter_port=1, resize=(640,480))
            self.is_recording = True

    def pi_camera_stop_recording(self):
        if self.is_recording:
            self.camera.stop_recording(splitter_port=1)

    def close_camera(self):
        if self.camera:
            self.camera.close()
            self.camera = None

    def opencv_start_recording(self):
        import cv2
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.recording_path, fourcc, 20.0, (640,480))
        self.is_recording = True

    def opencv_stop_recording(self):
        self.out.release()
        self.cap.release()