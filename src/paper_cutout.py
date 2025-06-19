"""
Scissor-cut paper cutout effect - simulates cutting with straight scissors
"""

import cv2
import numpy as np
import random
import math

# Scissor-cut specific settings
DEFAULT_EDGE_ROUGHNESS = 0.7
DEFAULT_SHADOW_INTENSITY = 0.8
DEFAULT_SHADOW_OFFSET = (10, 10)
DEFAULT_SHADOW_BLUR = 31     # Changed from 30 to 31 (must be odd)
DEFAULT_CUT_LENGTH_MIN = 8      # Minimum scissor cut length
DEFAULT_CUT_LENGTH_MAX = 25     # Maximum scissor cut length
DEFAULT_CUT_FREQUENCY = 0.3     # How often to make cuts (0.0-1.0)
DEFAULT_CUT_DEPTH = 8           # How deep cuts go into the object


class ScissorCutoutEffect:
    """Create realistic scissor-cut paper cutout effects"""

    def __init__(
        self,
        edge_roughness=DEFAULT_EDGE_ROUGHNESS,
        shadow_intensity=DEFAULT_SHADOW_INTENSITY,
        cut_length_min=DEFAULT_CUT_LENGTH_MIN,
        cut_length_max=DEFAULT_CUT_LENGTH_MAX,
        cut_frequency=DEFAULT_CUT_FREQUENCY,
        cut_depth=DEFAULT_CUT_DEPTH
    ):
        """
        Initialize scissor cutout effect

        Args:
            edge_roughness: Overall roughness multiplier (0.0 - 1.0)
            shadow_intensity: Intensity of shadow drop (0.0 - 1.0)
            cut_length_min: Minimum length of scissor cuts in pixels
            cut_length_max: Maximum length of scissor cuts in pixels
            cut_frequency: How often to make cuts (0.0 - 1.0)
            cut_depth: How deep cuts penetrate into the object
        """
        self.edge_roughness = edge_roughness
        self.shadow_intensity = shadow_intensity
        self.cut_length_min = cut_length_min
        self.cut_length_max = cut_length_max
        self.cut_frequency = cut_frequency
        self.cut_depth = cut_depth
        
        # Set random seed for reproducible results
        random.seed(42)

    def apply(self, image, mask):
        """
        Apply scissor-cut paper cutout effect to image

        Args:
            image (np.ndarray): Input image (BGR format)
            mask (np.ndarray): Binary mask for foreground

        Returns:
            np.ndarray: Image with scissor-cut effect applied
        """
        # Create scissor-cut edges
        cut_mask = self._create_scissor_cuts(mask)

        # Add pronounced shadow
        shadow = self._create_drop_shadow(cut_mask)

        # Composite final image
        result = self._composite_image(image, cut_mask, shadow)

        return result

    def _create_scissor_cuts(self, mask):
        """Create jagged edges by simulating scissor cuts"""
        # Start with original mask
        cut_mask = mask.copy()
        
        if self.edge_roughness <= 0:
            return cut_mask
        
        # Find contours of the object
        try:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        except Exception as e:
            print(f"Error finding contours: {e}")
            return cut_mask
        
        if not contours:
            print("Warning: No contours found in mask")
            return cut_mask
        
        # Work with the largest contour (main object)
        main_contour = max(contours, key=cv2.contourArea)
        contour_area = cv2.contourArea(main_contour)
        
        # Skip very small contours
        if contour_area < 100:  # Minimum 100 pixels
            print(f"Warning: Contour too small (area: {contour_area}), skipping cuts")
            return cut_mask
        
        print(f"Processing contour with area: {contour_area:.0f} pixels")
        
        # Create cuts along the contour
        try:
            cut_mask = self._cut_along_contour(cut_mask, main_contour)
        except Exception as e:
            print(f"Error creating cuts: {e}")
            return mask  # Return original mask if cutting fails
        
        return cut_mask

    def _cut_along_contour(self, mask, contour):
        """Make scissor cuts along the contour"""
        # Flatten contour points
        points = contour.reshape(-1, 2)
        total_points = len(points)
        
        # Safety check for minimum contour size
        if total_points < 10:
            print(f"Warning: Contour too small ({total_points} points), skipping cuts")
            return mask
        
        # Calculate step size based on cut frequency
        step = max(1, int(1.0 / max(0.01, self.cut_frequency * self.edge_roughness)))  # Prevent division by zero
        
        # Create cuts at regular intervals
        cuts_made = 0
        for i in range(0, total_points, step):
            if random.random() < self.cut_frequency * self.edge_roughness:
                try:
                    self._make_scissor_cut(mask, points, i)
                    cuts_made += 1
                except Exception as e:
                    print(f"Warning: Failed to make cut at point {i}: {e}")
                    continue
        
        print(f"Made {cuts_made} scissor cuts along contour")
        return mask

    def _make_scissor_cut(self, mask, contour_points, point_index):
        """Make a single scissor cut at a specific point"""
        if point_index >= len(contour_points):
            return
        
        # Get the cut point
        cut_point = contour_points[point_index]
        x, y = cut_point
        
        # Validate cut point is within mask bounds
        if x < 0 or y < 0 or x >= mask.shape[1] or y >= mask.shape[0]:
            return
        
        # Calculate cut direction (roughly perpendicular to contour)
        try:
            cut_angle = self._calculate_cut_angle(contour_points, point_index)
        except Exception as e:
            print(f"Warning: Failed to calculate cut angle: {e}")
            cut_angle = random.uniform(0, 2 * math.pi)  # Use random angle as fallback
        
        # Random cut length
        cut_length = random.randint(self.cut_length_min, self.cut_length_max)
        cut_length = int(cut_length * self.edge_roughness)
        cut_length = max(1, cut_length)  # Ensure minimum cut length
        
        # Calculate cut end point
        end_x = x + int(cut_length * math.cos(cut_angle))
        end_y = y + int(cut_length * math.sin(cut_angle))
        
        # Clamp end point to mask bounds
        end_x = max(0, min(mask.shape[1] - 1, end_x))
        end_y = max(0, min(mask.shape[0] - 1, end_y))
        
        # Make the cut with varying width to simulate scissor blade
        try:
            self._draw_scissor_cut_line(mask, (x, y), (end_x, end_y))
        except Exception as e:
            print(f"Warning: Failed to draw cut line: {e}")

    def _calculate_cut_angle(self, contour_points, point_index):
        """Calculate the angle for a scissor cut (perpendicular to contour direction)"""
        total_points = len(contour_points)
        
        # Safety check for minimum contour size
        if total_points < 10:
            # For very small contours, use a random angle
            return random.uniform(0, 2 * math.pi)
        
        # Get neighboring points to estimate contour direction
        neighbor_distance = min(5, total_points // 4)  # Adjust based on contour size
        prev_idx = (point_index - neighbor_distance) % total_points
        next_idx = (point_index + neighbor_distance) % total_points
        
        prev_point = contour_points[prev_idx]
        next_point = contour_points[next_idx]
        
        # Calculate contour direction
        dx = next_point[0] - prev_point[0]
        dy = next_point[1] - prev_point[1]
        
        # Handle case where points are the same (very small contour)
        if abs(dx) < 1e-6 and abs(dy) < 1e-6:
            return random.uniform(0, 2 * math.pi)
        
        # Calculate perpendicular angle (cut direction)
        contour_angle = math.atan2(dy, dx)
        cut_angle = contour_angle + math.pi/2
        
        # Add some randomness to make cuts look more natural
        cut_angle += random.uniform(-math.pi/6, math.pi/6)  # ±30 degrees variation
        
        return cut_angle

    def _draw_scissor_cut_line(self, mask, start_point, end_point):
        """Draw a scissor cut line that removes mask pixels"""
        x1, y1 = start_point
        x2, y2 = end_point
        
        # Validate coordinates
        if (x1 == x2 and y1 == y2) or x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
            return
        
        # Create line points
        line_points = self._get_line_points(x1, y1, x2, y2)
        
        # Safety check for empty line
        if not line_points or len(line_points) <= 1:
            return
        
        # Remove pixels along the cut with varying width
        for i, (x, y) in enumerate(line_points):
            # Calculate cut width (wider at the start, tapering toward the end)
            progress = i / max(1, len(line_points) - 1)  # Prevent division by zero
            cut_width = max(1, int(3 * (1 - progress * 0.7)))  # Ensure minimum width
            
            # Remove pixels in a small area around the cut point
            for dy in range(-cut_width, cut_width + 1):
                for dx in range(-cut_width, cut_width + 1):
                    px, py = x + dx, y + dy
                    if 0 <= px < mask.shape[1] and 0 <= py < mask.shape[0]:
                        # Distance from cut line affects removal intensity
                        distance = math.sqrt(dx*dx + dy*dy)
                        if distance <= cut_width:
                            removal_factor = 1.0 - (distance / max(1, cut_width))  # Prevent division by zero
                            current_value = mask[py, px]
                            mask[py, px] = int(current_value * (1 - removal_factor * 0.9))

    def _get_line_points(self, x1, y1, x2, y2):
        """Get all points along a line using Bresenham's algorithm"""
        points = []
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y1
        
        while True:
            points.append((x, y))
            
            if x == x2 and y == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        return points

    def _create_drop_shadow(self, mask):
        """Create pronounced drop shadow"""
        shadow = mask.copy()
        
        # Apply shadow offset
        offset_x, offset_y = DEFAULT_SHADOW_OFFSET
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        shadow = cv2.warpAffine(shadow, M, (mask.shape[1], mask.shape[0]))
        
        # Multiple blur passes for softer shadow - ensure odd kernel sizes
        blur_size = DEFAULT_SHADOW_BLUR
        if blur_size % 2 == 0:  # Make sure it's odd
            blur_size += 1
        
        shadow = cv2.GaussianBlur(shadow, (blur_size, blur_size), 0)
        shadow = cv2.GaussianBlur(shadow, (15, 15), 0)  # Additional blur (15 is already odd)
        
        # Apply shadow intensity
        shadow = (shadow * self.shadow_intensity).astype(np.uint8)
        
        return shadow

    def _composite_image(self, image, mask, shadow, transparent_background=True):
        """Composite image with enhanced contrast"""
        if transparent_background:
            height, width = image.shape[:2]
            result = np.zeros((height, width, 4), dtype=np.uint8)
            
            # Enhance image for paper effect
            enhanced_image = self._enhance_image(image)
            result[:, :, :3] = enhanced_image
            
            # Create alpha channel with shadow effects
            mask_alpha = mask.astype(np.float32) / 255.0
            shadow_alpha = shadow.astype(np.float32) / 255.0
            
            # Combine mask and shadow
            combined_alpha = mask_alpha.copy()
            
            # Add shadow where there's no main object
            shadow_area = (mask_alpha < 0.1) & (shadow_alpha > 0.1)
            combined_alpha[shadow_area] = shadow_alpha[shadow_area] * 0.7
            
            result[:, :, 3] = (combined_alpha * 255).astype(np.uint8)
            
        else:
            # White background version
            background = np.full_like(image, 250, dtype=np.uint8)
            
            # Apply shadow to background
            shadow_3ch = cv2.cvtColor(shadow, cv2.COLOR_GRAY2BGR)
            background = background - (shadow_3ch * 1.5)
            background = np.clip(background, 200, 255).astype(np.uint8)
            
            # Enhanced image
            enhanced_image = self._enhance_image(image)
            
            # Smooth blending
            mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
            
            result = background * (1 - mask_3ch) + enhanced_image * mask_3ch
            result = result.astype(np.uint8)
        
        return result

    def _enhance_image(self, image):
        """Enhance image to look more like printed paper"""
        enhanced = image.astype(np.float32)
        
        # Increase contrast and brightness slightly
        enhanced = enhanced * 1.15 - 15
        enhanced = np.clip(enhanced, 0, 255)
        
        # Boost saturation
        hsv = cv2.cvtColor(enhanced.astype(np.uint8), cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.2)
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Compatibility methods for the original interface
    def _create_rough_edges(self, mask):
        """Compatibility method - redirects to scissor cuts"""
        return self._create_scissor_cuts(mask)