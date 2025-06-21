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
    
    def create_outline(self, simplification=0.02, thickness=3):
        """
        Create polygonal outline from the mask
        
        Args:
            simplification: Higher = more angular (0.01-0.05)
            thickness: Line thickness in pixels
            
        Returns:
            outline_mask: Binary mask of the outline
        """
        thickness = int(thickness)

        # Find and simplify contours
        contours, _ = cv2.findContours(self.mask_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        simplified_contours = []
        for contour in contours:
            epsilon = simplification * cv2.arcLength(contour, True)
            poly = cv2.approxPolyDP(contour, epsilon, True)
            simplified_contours.append(poly)
        
        # Create outline mask
        outline_mask = np.zeros_like(self.mask_array, dtype=np.uint8)
        cv2.drawContours(outline_mask, simplified_contours, -1, 255, thickness)
        
        return outline_mask
    
    def add_outline_to_image(self, color=(255, 0, 0), simplification=0.02, thickness=3):
        """
        Add colored outline to the image
        
        Args:
            color: RGB color tuple (default red)
            simplification: Higher = more angular
            thickness: Line thickness
            
        Returns:
            image with outline added (RGB format)
        """
        outline_mask = self.create_outline(simplification, thickness)
        result = self.image_rgb.copy()
        result[outline_mask > 0] = color
        return result
    
    def get_outline_only(self, color=(255, 0, 0), simplification=0.02, thickness=3):
        """
        Get just the outline on transparent background
        
        Returns:
            RGBA image with just the outline
        """
        outline_mask = self.create_outline(simplification, thickness)
        
        # Create RGBA image
        outline_rgba = np.zeros((*self.mask_array.shape, 4), dtype=np.uint8)
        outline_rgba[outline_mask > 0] = (*color, 255)  # Color with full alpha
        
        return outline_rgba