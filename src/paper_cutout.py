import cv2
import numpy as np

class PaperCutoutEffect:
    def __init__(self, image_bgr, mask_array, alpha_threshold=200):
        self.image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        self.mask = self._clean_mask(mask_array, alpha_threshold)
    
    def create_cutout(self, outline_color=(255, 0, 0), white_thickness=30, 
                     red_thickness=3, detail=5):
        """
        Create paper cutout with transparency outside red border
        Everything inside border gets white background
        """
        # Create white outline around subject
        white_outline = self._create_outline(white_thickness)
        
        # Combine subject + white outline
        combined_shape = self.mask.copy()
        combined_shape[white_outline > 0] = 255
        combined_shape = self._smooth(combined_shape)
        
        # Create red border around the combined shape
        red_border = self._create_border(combined_shape, red_thickness, detail)
        
        # Create final RGBA image
        return self._compose_image(white_outline, red_border, outline_color)
    
    def _clean_mask(self, mask_array, threshold):
        """Clean and binarize mask"""
        mask = mask_array.astype(np.uint8)
        mask[mask < threshold] = 0
        mask[mask >= threshold] = 255
        return mask
    
    def _smooth(self, mask):
        """Apply smoothing to mask"""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        smooth = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        smooth = cv2.GaussianBlur(smooth, (5, 5), 1.0)
        _, smooth = cv2.threshold(smooth, 127, 255, cv2.THRESH_BINARY)
        return smooth
    
    def _create_outline(self, thickness):
        """Create white outline extending outward from subject"""
        smoothed = self._smooth(self.mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness*2+1, thickness*2+1))
        dilated = cv2.dilate(smoothed, kernel, iterations=1)
        return dilated - smoothed
    
    def _create_border(self, shape_mask, thickness, detail):
        """Create red border around shape"""
        # Smooth for cleaner contours
        mask = cv2.GaussianBlur(shape_mask, (7, 7), 2.0)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Find and simplify contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        simplified = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:
                epsilon = (0.08 / detail) * cv2.arcLength(contour, True)
                poly = cv2.approxPolyDP(contour, epsilon, True)
                simplified.append(poly)
        
        # Draw border
        border = np.zeros_like(mask)
        cv2.drawContours(border, simplified, -1, 255, thickness)
        return border
    
    def _compose_image(self, white_outline, red_border, outline_color):
        """Create final RGBA image with transparency outside red border"""
        height, width = self.image.shape[:2]
        result = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Find what's inside the red border
        contours, _ = cv2.findContours(red_border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        inside_border = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(inside_border, contours, 255)
        
        # Set alpha channel - only inside area is opaque (border itself is transparent)
        result[:, :, 3] = 0  # Everything transparent
        result[inside_border > 0, 3] = 255  # Only inside area opaque
        
        # Fill inside with white background
        result[inside_border > 0, :3] = (255, 255, 255)
        
        # Add original subject (only where it exists inside border)
        subject_inside = (self.mask > 0) & (inside_border > 0)
        result[subject_inside, :3] = self.image[subject_inside]
        
        # Add white outline (only inside border)
        white_inside = (white_outline > 0) & (inside_border > 0)
        result[white_inside, :3] = (255, 255, 255)
        
        # Red border is now transparent - it only defines the boundary
        
        return result