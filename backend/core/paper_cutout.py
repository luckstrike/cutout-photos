import cv2
import numpy as np

class PaperCutoutEffect:
    def __init__(self, image_bgr, mask_array, alpha_threshold=200):
        self.image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        self.mask = self._clean_mask(mask_array, alpha_threshold)
    
    def create_cutout(self, background_color=(255, 255, 255), outline_thickness=30, detail=5):
        """
        Create paper cutout with transparency outside border
        
        Args:
            background_color: RGB color for background and outline
            outline_thickness: Thickness of outline around subject
            detail: Border detail level (1-10, higher = more detailed)
        """
        # Create subject + outline shape
        subject_with_outline = self._create_subject_with_outline(outline_thickness)
        
        # Create invisible border around the shape (fixed thickness for clean cutoff)
        border = self._create_border(subject_with_outline, thickness=3, detail=detail)
        
        # Create final RGBA image
        return self._create_final_image(border, background_color)
    
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
    
    def _create_subject_with_outline(self, thickness):
        """Create subject mask expanded with outline"""
        smoothed = self._smooth(self.mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness*2+1, thickness*2+1))
        expanded = cv2.dilate(smoothed, kernel, iterations=1)
        return self._smooth(expanded)
    
    def _create_border(self, shape_mask, thickness, detail):
        """Create border around shape"""
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
    
    def _create_final_image(self, border, background_color):
        """Create final RGBA image with transparency outside border"""
        height, width = self.image.shape[:2]
        result = np.zeros((height, width, 4), dtype=np.uint8)
        
        # Find area inside the border
        contours, _ = cv2.findContours(border, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        inside_area = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(inside_area, contours, 255)
        
        # Set transparency: only inside area is visible
        result[inside_area > 0, 3] = 255  # Opaque inside
        
        # Fill with background color
        result[inside_area > 0, :3] = background_color
        
        # Add original subject on top
        subject_mask = (self.mask > 0) & (inside_area > 0)
        result[subject_mask, :3] = self.image[subject_mask]
        
        return result