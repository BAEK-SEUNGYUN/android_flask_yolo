from flask import Flask, render_template, Response
import yolo_webcam

app = Flask(__name__)

@ app.route('/')
def index():
    return render_template("main.html")

@ app.route('/webcam')
def webcam():
    return Response(yolo_webcam.webcam('http://172.20.10.2:8080/vedio'))


if __name__ == "__main__":
    app.run(debug=True)