import sys
import os
import cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.background_removal import BackgroundRemover
from src.paper_cutout import PaperCutoutEffect

def test_paper_cutout(image_bgr, mask_array):
    pass

if __name__ == "__main__":
    INPUT_PATH = "../examples/input/giraffe.jpg"
    OUTPUT_PATH = "../examples/output/debug_giraffe_mask.png"

    bg_remover = BackgroundRemover(INPUT_PATH, OUTPUT_PATH)
    cutout_effect = PaperCutoutEffect() # Run with the defaults

    # This test assumes that the mask is created correctly
    image_bgr, mask_array = bg_remover.remove_background_to_array()

    rough_mask = cutout_effect._create_rough_edges(mask_array)
    cv2.imwrite("../examples/output/01_test_rough_mask.png", rough_mask)

    shadow = cutout_effect._create_drop_shadow(rough_mask)
    cv2.imwrite("../examples/output/02_test_shadow.png", shadow)

    result = cutout_effect._composite_image(image_bgr, rough_mask, shadow)
    cv2.imwrite("../examples/output/03_test_result.png", result)