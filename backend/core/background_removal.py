"""
Background removal functionality using rembg
"""

import cv2
import numpy as np
from PIL import Image
from rembg import remove


# TODO: Add in smart format detection
#       to detect how a file should be saved (.png/.jpg/etc...)
class BackgroundRemover:
    """Handle background removal from images"""

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def remove_background_to_image(self):
        input = Image.open(self.input_path)
        output = remove(input)
        output.save(self.output_path)

    def remove_background_to_array(self):
        input_img = Image.open(self.input_path)
        output = remove(input_img)

        # Converting the PIL Image to Numpy Arrays
        image_array = np.array(output.convert("RGB"))
        mask_array = np.array(output)[:, :, 3]

        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        return image_bgr, mask_array
    
if __name__ == "__main__":
    INPUT_PATH = "../examples/input/giraffe.jpg"
    OUTPUT_PATH = "../examples/output/giraffe_no_background.png"

    bg_removal_obj = BackgroundRemover(INPUT_PATH, OUTPUT_PATH)
    bg_removal_obj.remove_background_to_image()