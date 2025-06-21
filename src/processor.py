"""
Updated processing pipeline with scissor-cut paper cutout effects
"""

import os
from PIL import Image
from .background_removal import BackgroundRemover
from .paper_cutout import PaperCutoutEffect  # Import the new scissor-cut effect

class ImageProcessor:
    """Main processor for creating realistic scissor-cut paper cutout effects"""

    def __init__(self, simplification=0.001, thickness=3, color=(255, 0, 0)):
        self.simplification = simplification
        self.thickness = thickness
        self.color = color
    
    def process_image(self, input_path, output_path):
        """
        Process a single image: remove background + apply scissor-cut effect

        Args:
            input_path (str): Path to input image
            output_path (str): Path for output image
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Processing {input_path}...")

            # Step 1: Remove background
            print("Removing the background...")
            bg_remover = BackgroundRemover(input_path, output_path)
            image_bgr, mask_array = bg_remover.remove_background_to_array()

            # Step 2: Creating a polygonal approximation of the cutout's outline
            outline_processor = PaperCutoutEffect(image_bgr, mask_array)

            outlined_image = outline_processor.add_outline_to_image()

            Image.fromarray(outlined_image).save(output_path)

            return True

        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False
    
    def process_directory(self, input_dir, output_dir):
        """
        Process all images in a directory

        Args:
            input_dir (str): Input directory path
            output_dir (str): Output directory path
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Supported image extensions
        extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

        # Find all image files
        image_files = []
        for filename in os.listdir(input_dir):
            if any(filename.lower().endswith(ext) for ext in extensions):
                image_files.append(filename)
        
        if not image_files:
            print(f"No image files found in {input_dir}")
            return
        
        print(f"Found {len(image_files)} images to process")

        # Process each image
        successful = 0
        for i, filename in enumerate(image_files, 1):
            print(f"[{i}/{len(image_files)}] Processing {filename}")
            
            input_path = os.path.join(input_dir, filename)

            # Change extension to .png to preserve transparency
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_cutout.png")

            if self.process_image(input_path, output_path):
                successful += 1
            
            print()  # Add spacing between files
        
        print(f"Batch processing complete: {successful}/{len(image_files)} images processed successfully")