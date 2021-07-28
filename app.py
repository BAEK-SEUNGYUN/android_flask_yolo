from flask import Flask, render_template, Response
import yolo_webcam

app = Flask(__name__)

@ app.route('/')
def index():
    return render_template("main.html")

@ app.route('/webcam')
def webcam():
    return Response(yolo_webcam.webcam('http://192.168.219.122:8080/video'))


if __name__ == "__main__":
    app.run(host="192.168.56.1", port="8080", debug=True)