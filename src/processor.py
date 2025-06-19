"""
Main processing pipeline, combining the background removal and
paper cutout effects
"""

import cv2
import os
from .background_removal import BackgroundRemover
from .paper_cutout import PaperCutoutEffect

class ImageProcessor:
    """Main process or used to create paper cutout effects"""

    def __init__(self, edge_roughness=0.3, shadow_intensity=0.5):
        self.edge_roughness = edge_roughness
        self.shadow_intensity = shadow_intensity
        self.paper_effect = PaperCutoutEffect(edge_roughness, shadow_intensity)
    
    def process_image(self, input_path, output_path):
        """
        Process a single image: remove background + apply paper cutout effect

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

            # Step 2: Applying the paper cutout effect
            print("Applying the paper cutout effect...")
            result = self.paper_effect.apply(image_bgr, mask_array)

            # Step 3: Save result
            print("Saving result...")
            cv2.imwrite(output_path, result)

            print(f"Completed! File written to: {output_path}")
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
    
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
        extensions = {'.jpg', 'jpeg', '.png', '.bmp', '.tiff', '.tif'}

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
        for filename in image_files:
            input_path = os.path.join(input_dir, filename)

            #Change extension to .png to preserver transparency
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_cutout.png")

            if self.process_image(input_path, output_path):
                successful += 1
        
        print(f"\nProcessed {successful} / {len(image_files)} images successfully")