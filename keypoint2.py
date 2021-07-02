
from __future__ import division
import os
import cv2
import time
import numpy as np



class general_pose_model(object):
    def __init__(self):
        self.model_path = "resources/"
        self.num_points = 22
        self.point_pairs = [[0,1],[1,2],[2,3],[3,4],
                            [0,5],[5,6],[6,7],[7,8],
                            [0,9],[9,10],[10,11],[11,12],
                            [0,13],[13,14],[14,15],[15,16],
                            [0,17],[17,18],[18,19],[19,20]]
        # self.inWidth = 368
        self.inHeight = 368
        self.threshold = 0.1
        self.hand_net = self.get_hand_model(self.model_path)


    def get_hand_model(self, modelpath):

        prototxt   = os.path.join(self.model_path, "hand/pose_deploy.prototxt")
        caffemodel = os.path.join(self.model_path, "hand/pose_iter_102000.caffemodel")
        hand_model = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)

        return hand_model


    def predict(self, imgfile):
        img_cv2 = cv2.imread(imgfile)
        img_height, img_width, _ = img_cv2.shape
        aspect_ratio = img_width/img_height

        inWidth = int(((aspect_ratio * self.inHeight) * 8)//8)
        inpBlob = cv2.dnn.blobFromImage(img_cv2, 1.0/255, (inWidth, self.inHeight), (0, 0, 0), swapRB=False, crop=False)

        self.hand_net.setInput(inpBlob)

        output = self.hand_net.forward()

        points = []
        for idx in range(self.num_points):
            probMap = output[0, idx, :, :] # confidence map.
            probMap = cv2.resize(probMap, (img_width, img_height))

            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            if prob > self.threshold:
                points.append((int(point[0]), int(point[1])))
            else:
                points.append(None)

        return points


    def get_hand_keypoint_image(self, imgfile, points):
        img_cv2 = cv2.imread(imgfile)
        img_cv2_copy = np.zeros(img_cv2.shape)
        for idx in range(len(points)):
            if points[idx]:
                cv2.circle(img_cv2_copy, points[idx], 8, (255, 255, 255), thickness=-1,
                           lineType=cv2.FILLED)
        return img_cv2_copy.astype("uint8")



if __name__ == '__main__':
    print("[INFO]Pose estimation.")

    imgs_path = "resources/0/1_android.jpg"
    img_files = [imgs_path]

    #
    start = time.time()
    modelpath = "resources/"
    pose_model = general_pose_model()
    print("[INFO]Model loads time: ", time.time() - start)

    for img_file in img_files:
        start = time.time()
        res_points = pose_model.predict(img_file)
        print("[INFO]Model predicts time: ", time.time() - start)
        pose_model.get_hand_keypoint_image(img_file, res_points)

    print("[INFO]Done.")