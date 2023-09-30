import io
import picamera
from django.http import StreamingHttpResponse

class Camera:
    def stream(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, format='jpeg', quality=70, use_video_port=True):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
                stream.seek(0)
                stream.truncate()

camera = Camera()

def gen(camera):
    return camera.stream()

def camera_feed(request):
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')
