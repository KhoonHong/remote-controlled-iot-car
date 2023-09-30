import io

class Camera:
    def stream(self):
        try:
            import picamera
            return self.pi_camera_stream()
        except ImportError:
            import cv2
            return self.opencv_stream()

    def pi_camera_stream(self):
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
