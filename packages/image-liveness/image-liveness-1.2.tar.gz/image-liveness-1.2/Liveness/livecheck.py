# -*- coding: utf-8 -*-
# @Time : 20-6-9 下午3:06
# @Author : zhuying
# @Company : Minivision
# @File : test.py
# @Software : PyCharm

import os
import cv2
import numpy as np
import argparse
import warnings
import time

from anti_spoof_predict import AntiSpoofPredict
from generate_patches import CropImage
from utility import parse_model_name
warnings.filterwarnings('ignore')


SAMPLE_IMAGE_PATH = "./images/"


# 因为安卓端APK获取的视频流宽高比为3:4,为了与之一致，所以将宽高比限制为3:4
class Liveness():
    def check_image(self,image):
        # import pdb;pdb.set_trace()
        # height, width, channel = image.shape
        # if width/height:
        #     print("Image is not appropriate!!!\nHeight/Width should be 4/3.")
        #     return False
        # else:
        return True


    def test(self,image, model_dir='./anti_spoof_models',device_id=0):
        model_test = AntiSpoofPredict(device_id)
        image_cropper = CropImage()
        width = int((image.shape[0]*3)/4)
        dim=(width,image.shape[0])
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        result = self.check_image(resized)
        if result is False:
            return
        image_bbox = model_test.get_bbox(image)
        prediction = np.zeros((1, 3))
        test_speed = 0
        # sum the prediction from single model's result
        for model_name in os.listdir(model_dir):
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": image,
                "bbox": image_bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }
            if scale is None:
                param["crop"] = False
            img = image_cropper.crop(**param)
            start = time.time()
            prediction += model_test.predict(img, os.path.join(model_dir, model_name))
            test_speed += time.time()-start

        # draw result of prediction
        label = np.argmax(prediction)
        value = prediction[0][label]/2
        if label == 1:
            res={"score":value,
                "result":"real",
                "rectangle":{
                "left":image_bbox[0],
                "top":image_bbox[1],
                "right":image_bbox[0] + image_bbox[2],
                "bottom":image_bbox[1] + image_bbox[3]
                }}
            # print("Image '{}' is Real Face. Score: {:.2f}.".format(image_name, value))
            result_text = "RealFace Score: {:.2f}".format(value)
            color = (255, 0, 0)
        else:
            res={"score":value,
                "result":"fake",
                "rectangle":{
                "left":image_bbox[0],
                "top":image_bbox[1],
                "right":image_bbox[0] + image_bbox[2],
                "bottom":image_bbox[1] + image_bbox[3]
                }}
            # print("Image '{}' is Fake Face. Score: {:.2f}.".format(image_name, value))
            result_text = "FakeFace Score: {:.2f}".format(value)
            color = (0, 0, 255)
        print("Prediction cost {:.2f} s".format(test_speed))
        # cv2.rectangle(
        #     image,
        #     (image_bbox[0], image_bbox[1]),
        #     (image_bbox[0] + image_bbox[2], image_bbox[1] + image_bbox[3]),
        #     color, 2)
        # cv2.putText(
        #     image,
        #     result_text,
        #     (image_bbox[0], image_bbox[1] - 5),
        #     cv2.FONT_HERSHEY_COMPLEX, 0.5*image.shape[0]/1024, color)

        # format_ = os.path.splitext(image_name)[-1]
        # result_image_name = image_name.replace(format_, "_result" + format_)
        # cv2.imwrite(SAMPLE_IMAGE_PATH + result_image_name, image)

        return res


    # if __name__ == "__main__":
    #     desc = "test"
    #     parser = argparse.ArgumentParser(description=desc)
    #     parser.add_argument(
    #         "--device_id",
    #         type=int,
    #         default=0,
    #         help="which gpu id, [0/1/2/3]")
    #     parser.add_argument(
    #         "--model_dir",
    #         type=str,
    #         default="./anti_spoof_models",
    #         help="model_lib used to test")
    #     parser.add_argument(
    #         "--image_name",
    #         type=str,
    #         default="image_F1.jpg",
    #         help="image used to test")
    #     args = parser.parse_args()
    #     print(args)
    result=test(image_name='mihirdai.jpg')
    print(result)
