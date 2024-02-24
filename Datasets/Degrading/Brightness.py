from imagecorruptions import corrupt
import cv2
import numpy as np


import imageio
import os
import shutil


def add_brightness(image_path):
    image = cv2.imread(image_path)
    img_aug = corrupt(image, corruption_name='brightness', severity=5)
    return(img_aug)





src_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/noise_val_dataset/original_val'
to_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/imagecorruptions/brightness_5'

count = 0

if os.path.exists(src_dir_path):
    for file in os.listdir(src_dir_path):
        file_path = os.path.join(src_dir_path,file)
        img_aug = add_brightness(file_path)
        img_aug_path = os.path.join(to_dir_path,file)
        cv2.imwrite(img_aug_path, img_aug)
        count = count + 1
        print('{a} noisy image generated'.format(a=count))
