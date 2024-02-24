from imgaug import augmenters as iaa
import imageio
import imgaug as ia
import os
import shutil

src_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/noise_val_dataset/original_val'
to_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/imgaug/motionblur_1'

count = 0

if os.path.exists(src_dir_path):
    for file in os.listdir(src_dir_path):
        file_path = os.path.join(src_dir_path,file)
        image = imageio.imread(file_path)
        img_aug = iaa.imgcorruptlike.apply_motion_blur(image, severity=1, seed=None)
        img_aug_path = os.path.join(to_dir_path,file)
        imageio.imwrite(img_aug_path, img_aug)
        count = count + 1
        print('{a} noisy image generated'.format(a=count))


# image = imageio.imread('/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/add_noise/compress/image3.png')
# img_aug = iaa.imgcorruptlike.apply_motion_blur(image, severity=5, seed=None)

# # img_aug = blur(image = image)

# to_dir_path = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/imgaug/img.png'

# imageio.imwrite(to_dir_path, img_aug)


# for batch_idx in range(1000):
#     # 'images' should be either a 4D numpy array of shape (N, height, width, channels)
#     # or a list of 3D numpy arrays, each having shape (height, width, channels).
#     # Grayscale images must have shape (height, width, 1) each.
#     # All images must have numpy's dtype uint8. Values are expected to be in
#     # range 0-255.
#     images = load_batch(batch_idx)
#     images_aug = seq(images=images)
#     train_on_images(images_aug)
