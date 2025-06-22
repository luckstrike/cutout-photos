import cv2
import numpy as np
from PIL import Image

class PaperCutoutEffect:
    def __init__(self, image_bgr, mask_array):
        self.image_bgr = image_bgr
        self.mask_array = mask_array.astype(np.uint8)
        self.image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    def clean_mask(self, alpha_threshold=200):
        """
        Remove semi-transparent pixels from mask
        
        Args:
            alpha_threshold: Pixels below this alpha value become transparent (0-255)
                           255 = only fully opaque pixels
                           200 = mostly opaque pixels
                           128 = half-transparent and above
        """
        mask = self.mask_array.copy()
        
        # Set pixels below threshold to 0 (transparent)
        mask[mask < alpha_threshold] = 0
        # Set pixels above threshold to 255 (fully opaque)
        mask[mask >= alpha_threshold] = 255
        
        return mask
    
    def create_outline(self, detail_level=5, thickness=3, smooth=True, alpha_threshold=200):
        """
        Create polygonal outline with alpha cleanup
        
        Args:
            detail_level: 1-10 (higher = more detailed)
            thickness: Line thickness
            smooth: Whether to smooth out jaggedness
            alpha_threshold: Remove pixels below this alpha value (0-255)
        """
        # Clean up semi-transparent pixels first
        mask = self.clean_mask(alpha_threshold)
        
        # Simple smoothing
        if smooth:
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Find contours and simplify
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        simplified_contours = []
        for contour in contours:
            # Skip tiny contours (noise)
            if cv2.contourArea(contour) > 100:
                simplification = 0.08 / detail_level
                epsilon = simplification * cv2.arcLength(contour, True)
                poly = cv2.approxPolyDP(contour, epsilon, True)
                simplified_contours.append(poly)
        
        # Draw outline
        outline_mask = np.zeros_like(mask)
        cv2.drawContours(outline_mask, simplified_contours, -1, 255, int(thickness))
        
        return outline_mask
    
    def add_outline_to_image(self, color=(255, 0, 0), detail_level=5, thickness=3, 
                           smooth=True, alpha_threshold=200):
        """Add outline to image with alpha cleanup"""
        polygonal_outline = self.create_outline(detail_level, thickness, smooth, alpha_threshold)
        outward_outline = self.create_smooth_outward_outline()

        result = self.image_rgb.copy()
        
        result[outward_outline > 0] = (255, 255, 255)
        result[polygonal_outline > 0] = color # mask to be used when cutting out the image
        return result
    
    def create_smooth_outward_outline(self, thickness=30, smooth_iterations=2):
        """
        Create smooth outline by pre-processing the mask
        """
        mask = self.mask_array.copy()

        # Ensure binary mask
        if mask.dtype == bool:
            mask = mask.astype(np.uint8) * 255
        elif mask.max() <= 1:
            mask = (mask * 255).astype(np.uint8)
        
        # Step 1: Smooth the original mask first
        # Use morphological opening/closing to smooth edges
        kernel_smooth = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        
        # Close small gaps and smooth edges
        smoothed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_smooth, iterations=smooth_iterations)
        smoothed_mask = cv2.morphologyEx(smoothed_mask, cv2.MORPH_OPEN, kernel_smooth, iterations=1)
        
        # Step 2: Apply Gaussian blur for extra smoothness
        smoothed_mask = cv2.GaussianBlur(smoothed_mask, (5, 5), 1.0)
        
        # Re-threshold to binary
        _, smoothed_mask = cv2.threshold(smoothed_mask, 127, 255, cv2.THRESH_BINARY)
        
        # Step 3: Create outline with larger elliptical kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness*2+1, thickness*2+1))
        dilated = cv2.dilate(smoothed_mask, kernel, iterations=1)
        outline = dilated - smoothed_mask
        
        return outline