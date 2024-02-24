from PIL import Image
import os

rain = 'rain5.png'
output_folder = './rain5/'

input_folder = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/image_quality/original_val'


if not os.path.exists(output_folder):
    os.makedirs(output_folder)

rain_mask = Image.open(rain)


for filename in os.listdir(input_folder):
    if filename.endswith(".png"):  # Assuming all images in the folder are PNG files
        img_path = os.path.join(input_folder, filename)
        ground = Image.open(img_path)
        rain_mask_resized = rain_mask.resize(ground.size)
        r, g, b, a = rain_mask_resized.split()
        fusion = Image.composite(rain_mask_resized, ground, a)
        
        output_path = os.path.join(output_folder, filename)
        fusion.save(output_path)



