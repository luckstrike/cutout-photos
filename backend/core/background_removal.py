"""
Background removal functionality using rembg
"""

import cv2
import numpy as np
from PIL import Image
from rembg import remove


class BackgroundRemover:
    """Handle background removal from images"""
    def __init__(self):
        pass

    def image_to_lists(self, input_image: Image):
        if input_image is None:
            return None
        
        output = remove(input_image)

        # Converting the PIL Image to Numpy Arrays
        image_array = np.array(output.convert("RGB"))
        mask_array = np.array(output)[:, :, 3]

        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        return image_bgr, mask_array
    
    def file_to_lists(self, input_path):
        if input_path is None:
            return None
        
        input_image = Image.open(input_path)

        image_bgr, mask_array = self.image_to_lists(input_image)

        return image_bgr, mask_array
    
    def save_to_disk(self, input_path, output_path):
        try:
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            output_image.save(output_path)
        except Exception as e:
            print(f"file_to_disk: {e}")

if __name__ == "__main__":
    INPUT_PATH = "../../examples/input/giraffe.jpg"
    OUTPUT_PATH = "../../examples/output/giraffe_no_background.png"

    bg_removal_obj = BackgroundRemover()
    bg_removal_obj.save_to_disk(INPUT_PATH, OUTPUT_PATH)