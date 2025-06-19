"""
Updated processing pipeline with scissor-cut paper cutout effects
"""

import cv2
import os
from .background_removal import BackgroundRemover
from .paper_cutout import ScissorCutoutEffect  # Import the new scissor-cut effect

class ImageProcessor:
    """Main processor for creating realistic scissor-cut paper cutout effects"""

    def __init__(self, edge_roughness=0.7, shadow_intensity=0.8, 
                 cut_length_min=10, cut_length_max=25, cut_frequency=0.3, cut_depth=8):
        """
        Initialize with scissor-cut parameters
        
        Args:
            edge_roughness: Overall effect intensity (0.0-1.0)
            shadow_intensity: Shadow darkness (0.0-1.5)
            cut_length_min: Minimum scissor cut length in pixels
            cut_length_max: Maximum scissor cut length in pixels
            cut_frequency: How often to make cuts (0.0-1.0)
            cut_depth: How deep cuts penetrate into object
        """
        self.edge_roughness = edge_roughness
        self.shadow_intensity = shadow_intensity
        self.cut_length_min = cut_length_min
        self.cut_length_max = cut_length_max
        self.cut_frequency = cut_frequency
        self.cut_depth = cut_depth
        
        # Create the scissor-cut effect processor
        self.paper_effect = ScissorCutoutEffect(
            edge_roughness=edge_roughness,
            shadow_intensity=shadow_intensity,
            cut_length_min=cut_length_min,
            cut_length_max=cut_length_max,
            cut_frequency=cut_frequency,
            cut_depth=cut_depth
        )
    
    def process_image(self, input_path, output_path, save_steps=False):
        """
        Process a single image: remove background + apply scissor-cut effect

        Args:
            input_path (str): Path to input image
            output_path (str): Path for output image
            save_steps (bool): Save intermediate processing steps
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Processing {input_path}...")

            # Step 1: Remove background
            print("Removing the background...")
            bg_remover = BackgroundRemover(input_path, output_path)
            image_bgr, mask_array = bg_remover.remove_background_to_array()

            # Save intermediate step if requested
            if save_steps:
                step_dir = os.path.dirname(output_path)
                base_name = os.path.splitext(os.path.basename(output_path))[0]
                
                cv2.imwrite(os.path.join(step_dir, f"{base_name}_01_original_mask.png"), mask_array)
                cv2.imwrite(os.path.join(step_dir, f"{base_name}_02_no_background.png"), 
                           cv2.bitwise_and(image_bgr, image_bgr, mask=mask_array))

            # Step 2: Apply scissor-cut paper cutout effect
            print("Applying scissor-cut paper cutout effect...")
            print(f"  Cut length: {self.cut_length_min}-{self.cut_length_max} pixels")
            print(f"  Cut frequency: {self.cut_frequency:.1%}")
            print(f"  Cut depth: {self.cut_depth} pixels")
            
            result = self.paper_effect.apply(image_bgr, mask_array)

            # Save intermediate steps if requested
            if save_steps:
                # Save the cut mask
                cut_mask = self.paper_effect._create_scissor_cuts(mask_array)
                cv2.imwrite(os.path.join(step_dir, f"{base_name}_03_cut_mask.png"), cut_mask)
                
                # Save the shadow
                shadow = self.paper_effect._create_drop_shadow(cut_mask)
                cv2.imwrite(os.path.join(step_dir, f"{base_name}_04_shadow.png"), shadow)

            # Step 3: Save result
            print("Saving result...")
            cv2.imwrite(output_path, result)

            print(f"Completed! File written to: {output_path}")
            
            if save_steps:
                print(f"Intermediate steps saved to: {step_dir}")
            
            return True
            
        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            return False
    
    def process_directory(self, input_dir, output_dir, save_steps=False):
        """
        Process all images in a directory

        Args:
            input_dir (str): Input directory path
            output_dir (str): Output directory path
            save_steps (bool): Save intermediate steps for each image
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
        print(f"Effect settings:")
        print(f"  Edge roughness: {self.edge_roughness}")
        print(f"  Cut range: {self.cut_length_min}-{self.cut_length_max} pixels")
        print(f"  Cut frequency: {self.cut_frequency:.1%}")
        print()

        # Process each image
        successful = 0
        for i, filename in enumerate(image_files, 1):
            print(f"[{i}/{len(image_files)}] Processing {filename}")
            
            input_path = os.path.join(input_dir, filename)

            # Change extension to .png to preserve transparency
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}_cutout.png")

            if self.process_image(input_path, output_path, save_steps):
                successful += 1
            
            print()  # Add spacing between files
        
        print(f"Batch processing complete: {successful}/{len(image_files)} images processed successfully")

    def update_settings(self, **kwargs):
        """Update effect settings and recreate the effect processor"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Recreate the effect with new settings
        self.paper_effect = ScissorCutoutEffect(
            edge_roughness=self.edge_roughness,
            shadow_intensity=self.shadow_intensity,
            cut_length_min=self.cut_length_min,
            cut_length_max=self.cut_length_max,
            cut_frequency=self.cut_frequency,
            cut_depth=self.cut_depth
        )