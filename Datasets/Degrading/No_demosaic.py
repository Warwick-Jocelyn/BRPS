# -*- coding: utf-8 -*-
# RGB2BGGR
import os
from PIL import Image

def convertimg3RGB(kittifile, savedir):
    img = Image.open(kittifile)

    img_rows = img.width
    img_cols = img.height
    bayer_img = Image.new('RGB', (img_rows, img_cols))
    bayer_r, bayer_g, bayer_b = bayer_img.split()
    
    for i in range(0, img_rows, 1):
        for j in range(0, img_cols, 1):
            if i % 2 == 1 and j % 2 == 1:
                r, g, b = img.getpixel((i, j))
                b_out = round(0.022 * r - 0.630 * g + 1.623 * b)
                bayer_b.putpixel((i, j), b_out)
                bayer_b.putpixel((i, j - 1), b_out)
                bayer_b.putpixel((i - 1, j), b_out)
                bayer_b.putpixel((i - 1, j - 1), b_out)
            if i % 2 == 0 and j % 2 == 0:
                r, g, b = img.getpixel((i, j))
                r_out = round(r * 1.844 - g * 0.348 - b * 0.481)
                bayer_r.putpixel((i, j), r_out)
                if j + 1 < img_cols:
                    bayer_r.putpixel((i, j + 1), r_out)
                if i + 1 < img_rows:
                    bayer_r.putpixel((i + 1, j), r_out)
                if i + 1 < img_rows and j + 1 < img_cols:
                    bayer_r.putpixel((i + 1, j + 1), r_out)
            if (i % 2 == 1 and j % 2 == 0) or (i % 2 == 0 and j % 2 == 1):
                r, g, b = img.getpixel((i, j))
                g_out = round(-0.347 * r + 1.363 * g + 0.001 * b)
                bayer_g.putpixel((i, j), g_out)
    
    for i in range(0, img_rows, 1):
        for j in range(0, img_cols, 1):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                num = 0  # sum of channel
                gsum = 0  # sum of green value
                if i - 1 >= 0:  # up
                    r, g, b = img.getpixel((i - 1, j))
                    num = num + 1
                    gsum = gsum + g
                if i + 1 < img_rows :  # down
                    r, g, b = img.getpixel((i + 1, j))
                    num = num + 1
                    gsum = gsum + g
                if j - 1 >= 0:  # left
                    r, g, b = img.getpixel((i, j - 1))
                    num = num + 1
                    gsum = gsum + g
                if j + 1 <img_cols:  # right
                    r, g, b = img.getpixel((i, j + 1))
                    num = num + 1
                    gsum = gsum + g
                gvalue = round(gsum / num)
                bayer_g.putpixel((i, j), gvalue)
    
    bayer_img = Image.merge("RGB", (bayer_r, bayer_g, bayer_b))
    print(os.path.basename(kittifile))
    bayer_img.save(os.path.join(savedir, os.path.basename(kittifile)))

def convert_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    for image_file in image_files:
        input_path = os.path.join(input_folder, image_file)
        convertimg3RGB(input_path, output_folder)

# Example usage:
input_folder = "/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/image_quality/original_val"
output_folder = "/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/bayer/val"
convert_images_in_folder(input_folder, output_folder)

