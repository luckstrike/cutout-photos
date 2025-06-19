import sys
import os
import cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.background_removal import BackgroundRemover

def test_background_removal(input_path, output_path):
    """Saves an image of the returned mask"""
    bg_remover = BackgroundRemover(input_path, output_path)

    image_bgr, mask_array = bg_remover.remove_background_to_array()

    cv2.imwrite(output_path, mask_array)

    print(f"Successfully wrote the mask to {output_path}")

if __name__ == "__main__":
    INPUT_PATH = "../examples/input/giraffe.jpg"
    OUTPUT_PATH = "../examples/output/debug_giraffe_mask.png"
    test_background_removal(INPUT_PATH, OUTPUT_PATH)