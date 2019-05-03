import base64
import json
import os
import subprocess

from flask import Flask, request, send_file
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


def decode_and_save_image(image_file_name, base64_data):
    decoded_data = base64.b64decode(base64_data)
    if not os.path.exists("samples"):
        os.makedirs("samples")
    with open(os.path.join("samples", image_file_name), "wb") as f:
        f.write(decoded_data)


@app.route("/doodle", methods=["post"])
def create_doodle():
    request_data = json.loads(request.data)
    decode_and_save_image("face.png", request_data["face_image"])
    decode_and_save_image("face_sem.png", request_data["face_sem_map"])
    decode_and_save_image("style.png", request_data["style_image"])
    decode_and_save_image("style_sem.png", request_data["style_sem_map"])
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(" ".join(["doodle", "--style", "samples/style.png", "--content", "samples/face.png", "--output", "samples/result.png", "--device=cuda*", "--phases=4", "--iterations=80"]))
    subprocess.call(
        ["./create-doodle.sh"],
        shell=True
    )
    return send_file(os.path.join("samples", "result.png"), mimetype="image/png")


if __name__ == "__main__":
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()
