import shadows_preprocessing
import keypoint2
import os
import numpy as np
import cv2

def preprocess(android_cam):
    #sh_img = shadows_preprocessing.get_shadows(laptop_cam)
    pose_model = keypoint2.general_pose_model()
    res_points = pose_model.predict(android_cam)
    hand_keypoint_img = pose_model.get_hand_keypoint_image(android_cam, res_points)
    dim = (64,64)
   # sh_img_resized = cv2.resize(sh_img, dim, interpolation = cv2.INTER_AREA)
    result = cv2.resize(hand_keypoint_img, dim, interpolation=cv2.INTER_AREA)
    #result= np.concatenate((sh_img_resized,hand_keypoint_img_resized), axis=1)
    return result



def class_images_preprocess(num_class):
    path = f"resources/{num_class}"
    prep_dir = f"resources/{num_class}_preprocessed"
    if not os.path.exists(prep_dir):
        os.mkdir(prep_dir)

    for i  in range(1,1500):
        image_from_android_cam = path + f'/{i}_android.jpg'
        image_from_laptop_cam = path + f'/{i}_laptop.jpg'
        if  os.path.isfile(image_from_android_cam) and os.path.isfile(image_from_laptop_cam):
            print(f"Preprocessing {image_from_android_cam} and {image_from_laptop_cam}")
            prep_img = preprocess(image_from_android_cam, image_from_laptop_cam)
            cv2.imwrite(f"{prep_dir}/{i}.jpg",prep_img)

if __name__ == '__main__':
    for num_class in range(10):
        class_images_preprocess(num_class)
