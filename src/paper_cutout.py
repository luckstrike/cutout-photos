import cv2
import numpy as np

class PaperCutoutEffect:
    def __init__(self, image_bgr, mask_array, alpha_threshold=200):
        self.image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        self.mask = self._clean_mask(mask_array, alpha_threshold)
    
    def create_paper_cutout(self, outline_color=(255, 0, 0), white_thickness=30, 
                           red_thickness=3, detail=5):
        """
        Create complete paper cutout effect: subject + white outline + red border
        
        Args:
            outline_color: RGB color for outer border
            white_thickness: Thickness of white outline (pixels)
            red_thickness: Thickness of red border line
            detail: Border detail level (1-10, higher = more detailed)
        """
        # Create white outline
        white_outline = self._create_white_outline(white_thickness)
        
        # Create combined shape (subject + white outline)
        combined_shape = self._create_combined_shape(white_outline)
        
        # Create red border around combined shape
        red_border = self._create_border(combined_shape, red_thickness, detail)
        
        # Compose final image
        return self._compose_final_image(white_outline, red_border, outline_color)
    
    def create_white_outline_only(self, thickness=30, background=(255, 255, 255)):
        """Create just subject with white outline, no red border"""
        white_outline = self._create_white_outline(thickness)
        
        result = np.full_like(self.image, background)
        result[self.mask > 0] = self.image[self.mask > 0]  # Subject
        result[white_outline > 0] = (255, 255, 255)       # White outline
        
        return result
    
    # Private methods (implementation details)
    def _clean_mask(self, mask_array, threshold):
        """Clean and binarize mask"""
        mask = mask_array.astype(np.uint8)
        mask[mask < threshold] = 0
        mask[mask >= threshold] = 255
        return mask
    
    def _smooth(self, mask):
        """Apply consistent smoothing"""
        # Morphological smoothing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        smooth = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        smooth = cv2.morphologyEx(smooth, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Gaussian smoothing
        smooth = cv2.GaussianBlur(smooth, (5, 5), 1.0)
        _, smooth = cv2.threshold(smooth, 127, 255, cv2.THRESH_BINARY)
        
        return smooth
    
    def _create_white_outline(self, thickness):
        """Create smooth white outline extending outward"""
        smoothed = self._smooth(self.mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness*2+1, thickness*2+1))
        dilated = cv2.dilate(smoothed, kernel, iterations=1)
        return dilated - smoothed
    
    def _create_combined_shape(self, white_outline):
        """Combine original subject with white outline"""
        combined = self.mask.copy()
        combined[white_outline > 0] = 255
        return self._smooth(combined)
    
    def _create_border(self, shape_mask, thickness, detail):
        """Create polygonal border around shape"""
        # Extra smoothing for polygonal border
        mask = cv2.GaussianBlur(shape_mask, (7, 7), 2.0)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Find and simplify contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        simplified = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Skip noise
                epsilon = (0.08 / detail) * cv2.arcLength(contour, True)
                poly = cv2.approxPolyDP(contour, epsilon, True)
                simplified.append(poly)
        
        # Draw border
        border = np.zeros_like(mask)
        cv2.drawContours(border, simplified, -1, 255, thickness)
        return border
    
    def _compose_final_image(self, white_outline, red_border, outline_color):
        """Compose final image with all elements"""
        result = self.image.copy()
        result[white_outline > 0] = (255, 255, 255)  # White outline
        result[red_border > 0] = outline_color        # Red border
        return result