from imgaug import augmenters as iaa
import imageio
import imgaug as ia
import os
import shutil

src_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/noise_val_dataset/original_val'
to_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/imgaug/unfocus_5'

# aug = iaa.AdditivePoissonNoise(lam=(0.0, 15.0), per_channel=True)
# Adds poisson noise sampled from Poisson(x) to images,
# with x being sampled from uniform(0.0, 15.0) per image and channel.
# This is the recommended configuration.

aug = iaa.imgcorruptlike.DefocusBlur(severity=5)

# Adds poisson noise sampled from Poisson(5.0) to images,
# where the values are different per image and pixel and channel
# (e.g. a different one for red, green and blue channels for the same pixel).




count = 0

if os.path.exists(src_dir_path):
    for file in os.listdir(src_dir_path):
        file_path = os.path.join(src_dir_path,file)
        image = imageio.imread(file_path)
        img_aug = aug(image=image)
        img_aug_path = os.path.join(to_dir_path,file)
        imageio.imwrite(img_aug_path, img_aug)
        count = count + 1
        print('{a} noisy image generated'.format(a=count))

