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
        outline_mask = self.create_outline(detail_level, thickness, smooth, alpha_threshold)
        result = self.image_rgb.copy()
        result[outline_mask > 0] = color
        return result