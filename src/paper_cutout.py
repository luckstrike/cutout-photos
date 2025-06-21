import cv2
import numpy as np

class PaperCutoutEffect:
    def __init__(self, image_bgr, mask_array):
        """
        Initialize with results from remove_background_to_array()
        
        Args:
            image_bgr: Background-removed image in BGR format
            mask_array: Alpha mask array
        """
        self.image_bgr = image_bgr
        self.mask_array = mask_array.astype(np.uint8)
        self.image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    def create_outline(self, detail_level=5, thickness=3, smooth=True):
        """
        Create polygonal outline
        
        Args:
            detail_level: 1-10 (higher = more detailed)
            thickness: Line thickness
            smooth: Whether to smooth out jaggedness
        """
        mask = self.mask_array.copy()
        
        # Simple smoothing: just blur and re-threshold
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
    
    def add_outline_to_image(self, color=(255, 0, 0), detail_level=5, thickness=3, smooth=True):
        """Add outline to image"""
        outline_mask = self.create_outline(detail_level, thickness, smooth)
        result = self.image_rgb.copy()
        result[outline_mask > 0] = color
        return result