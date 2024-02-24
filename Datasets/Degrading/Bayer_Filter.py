import cv2
import os

# Input and output directories
input_folder = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/image_quality/original_val'
output_folder = '/home/wang3_y@WMGDS.WMG.WARWICK.AC.UK/Desktop/Codes/grayscale/grayscale_val'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all files in the input folder
file_list = os.listdir(input_folder)

# Iterate through the files and convert to grayscale
for file in file_list:
    # Check if the file is an image (you can add more image extensions if needed)
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Read the image
        image = cv2.imread(os.path.join(input_folder, file))
        
        if image is not None:
            # Convert the image to grayscale
            grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Save the grayscale image to the output folder
            output_file = os.path.join(output_folder, file)
            cv2.imwrite(output_file, grayscale_image)
            print(f'Converted {file} to grayscale and saved as {output_file}')
        else:
            print(f'Could not read {file}')
    else:
        print(f'Skipping non-image file: {file}')

print('Conversion complete.')
