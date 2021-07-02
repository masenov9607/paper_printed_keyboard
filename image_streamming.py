import cv2
import urllib.request

import numpy as np
import preprocessing
import keras
import socket
import json

URL = "http://192.168.1.2:8080/shot.jpg"
model = keras.models.load_model("resources/bcnn")
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)
def predict_on_img(event,x,y,flags,param):
    global laptop, android

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.imwrite("android.jpg", android)
        prep_img = preprocessing.preprocess("android.jpg")
        flatten_img = prep_img.flatten()
        normalized_img = flatten_img.astype("float32")/255
        array_img = normalized_img.tolist()
        normalized_img_reshaped = normalized_img.reshape(1, 64, 64, 3)
        prediction = np.argmax(model.predict(normalized_img_reshaped))
        print(f"{prediction} has been pressed")
        send_data = json.dumps({"key": int(prediction)})
        s.sendto(send_data.encode('utf-8'),("192.168.1.3", 4210))

        """
        if predictions.is_pressed(array_img):
            normalized_img_reshaped = normalized_img.reshape(1, 28, 56, 3)
            prediction = np.argmax(model.predict(normalized_img_reshaped))
            print(f"{prediction} has been pressed")
        else:
            print("Button not pressed")
       """
cv2.namedWindow('IPWebcam')
cv2.setMouseCallback('IPWebcam', predict_on_img)

while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    android = cv2.imdecode(img_arr, -1)

    cv2.imshow('IPWebcam', android)
    keyboard = cv2.waitKey(1)

    if keyboard == ord('q'):
        break
cv2.destroyAllWindows()
