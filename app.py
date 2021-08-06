from cv2 import data
from flask import Flask, render_template, Response, jsonify, request
import cv2
import time, datetime, sys
import numpy as np
import yolo_webcam
from camera import Camera
import pandas as pd

app = Flask(__name__)


# object와 해당하는 price
datas = pd.read_excel(r'C:\Users\User\github\android_flask_yolo\dataset\object_price.xlsx', engine='openpyxl')


cap = cv2.VideoCapture('http://172.20.10.2:8080/video')
# cap = cv2.VideoCapture('http://192.168.219.105:8080/video')
# cap = cv2.VideoCapture('http://172.30.1.57:8080/video')
# cap = cv2.VideoCapture(0)

detect_label = []

def price(labels):
    total_price = 0
    list = labels

    for label in list:
        for i in range(datas.shape[0]):
            try:
                name = datas.loc[i, 'object']
                unit_price = datas.loc[i, 'price']

                if name == label["name"] :
                    price = int(unit_price)
                    label["price"] = price
                    total_price += price
                    break

            except KeyError as k:
                print(k)
                break
            i += 1

    return list, total_price

@app.route('/_stuff', methods=['GET',"POST"])
def stuff():
    global detect_label

    if request.method == "POST":
        detect_label = []
        return jsonify(result=detect_label)
    detect_label,total_price = price(detect_label)
    return jsonify(result=detect_label, total_price= total_price)



# 실행
def gen_frames():

    # model = r'C:\Users\User\github\android_flask_yolo\yolo_v3\yolov3_detect\yolov3_last.weights'
    # config = r'C:\Users\User\github\android_flask_yolo\yolo_v3\yolov3_detect\yolov3.cfg'
    # class_labels = r'C:\Users\User\github\android_flask_yolo\yolo_v3\yolov3_detect\coco.names'

    model = r'C:\Users\User\github\android_flask_yolo\yolo_v3\yolo_best\yolov4_tiny_custom_best.weights'
    config = r'C:\Users\User\github\android_flask_yolo\yolo_v3\yolo_best\yolov4_tiny_custom.cfg'
    class_labels = r'C:\Users\User\github\android_flask_yolo\yolo_v3\yolo_best\obj.names'
    confThreshold = 0.5
    nmsThreshold = 0.4

    net = cv2.dnn.readNet(model, config)

    if net.empty():
        print('Net open failed!')
        sys.exit()

    # 클래스 이름 불러오기

    classes = []
    with open(class_labels, 'rt', encoding="UTF8") as f:
        classes = f.read().rstrip('\n').split('\n')

    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # 출력 레이어 이름 받아오기

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # output_layers = ['yolo_82', 'yolo_94', 'yolo_106']

    global detect_label

    while True:

        success, frame = cap.read()

        if not success:
            break
        # 블롭 생성 & 추론
        blob = cv2.dnn.blobFromImage(frame, 1/255., (320, 320), swapRB=True)
        net.setInput(blob)
        outs = net.forward(output_layers) #

        h, w = frame.shape[:2]

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                # detection: 4(bounding box) + 1(objectness_score) + 80(class confidence)
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > confThreshold:
                    # 바운딩 박스 중심 좌표 & 박스 크기
                    cx = int(detection[0] * w)
                    cy = int(detection[1] * h)
                    bw = int(detection[2] * w)
                    bh = int(detection[3] * h)

                    # 바운딩 박스 좌상단 좌표
                    sx = int(cx - bw / 2)
                    sy = int(cy - bh / 2)

                    boxes.append([sx, sy, bw, bh])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        # 비최대 억제, Non Max Suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

        for i in indices:
            global detect_label
            i = i[0]
            sx, sy, bw, bh = boxes[i]
            label = f'{classes[class_ids[i]]}: {confidences[i]:.2}'
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (sx, sy, bw, bh), color, 2)
            cv2.putText(frame, label, (sx, sy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
           
            
            print(label)
            detect_label.append({"name" : classes[class_ids[i]]})
            # detect_label.append('{classes[class_ids[i]]}')
            # print(detect_label)
            detect_label = list(map(dict, set(tuple(sorted(d.items())) for d in detect_label)))
        
        print(f"print :{detect_label} ")


        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 1, cv2.LINE_AA)

        # for c in det[:, -1].unique():
        #             n = (det[:, -1] == c).sum()  # detections per class
        #             s += '%g %ss, ' % (n, names[int(c)])  # add to string

        
        dst = cv2.resize(frame, dsize=(640, 480), interpolation=cv2.INTER_AREA)

        # cv2.imshow('frame', dst)
        # out.write(dst)
        # key = cv2.waitKey(1) & 0xFF
    #  if the `q` key was pressed, break from the loop
        # if key == ord("q"):
            # break
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@ app.route('/')
def index():
    """Video streaming home page."""
    # print(detect_label)
    return render_template("main.html", data = detect_label)

if __name__ == "__main__":
    # app.run(host="192.168.56.1", port="8080", debug=True)
    app.run(debug=True)