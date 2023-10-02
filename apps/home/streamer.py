import io
import os

class Camera:
    def __init__(self):
        self.is_recording = False
        self.recording_path = None

    def stream(self):
        try:
            import picamera
            return self.pi_camera_stream()
        except ImportError:
            import cv2
            return self.opencv_stream()

    def pi_camera_stream(self):
        import picamera
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, format='jpeg', quality=70, use_video_port=True):
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

        try:
            import picamera
            self.pi_camera_start_recording()
        except ImportError:
            import cv2
            self.opencv_start_recording()

    def stop_recording(self):
        try:
            import picamera
            self.pi_camera_stop_recording()
        except ImportError:
            import cv2
            self.opencv_stop_recording()
        self.is_recording = False

    def pi_camera_start_recording(self):
        import picamera

        # Check if camera is already initialized
        if hasattr(self, 'camera'):
            self.pi_camera_stop_recording()

        try:
            self.camera = picamera.PiCamera(resolution=(640, 480), framerate=24)
            self.camera.start_recording(self.recording_path)
            self.is_recording = True
        except picamera.PiCameraError as e:
            print(f"Error starting recording: {e}")


    def pi_camera_stop_recording(self):
        self.camera.stop_recording()
        self.camera.close()

    def opencv_start_recording(self):
        import cv2
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.recording_path, fourcc, 20.0, (640,480))
        self.is_recording = True

    def opencv_stop_recording(self):
        self.out.release()
        self.cap.release()