"""
Enhanced Paper cutout effect implementation with more pronounced effects
"""

import cv2
import numpy as np
import opensimplex

# Enhanced default settings for more noticeable effects
DEFAULT_EDGE_ROUGHNESS = 0.6  # Increased from 0.3
DEFAULT_SHADOW_INTENSITY = 0.8  # Increased from 0.5
DEFAULT_SHADOW_OFFSET = (8, 8)  # Increased from (5, 5)
DEFAULT_SHADOW_BLUR = 25  # Increased from 15
NOISE_SCALE = 8.0  # Decreased from 20.0 for more detailed tears
EDGE_THRESHOLD = 0.15  # Decreased from 0.3 for more aggressive tearing
TEAR_RADIUS = 4  # Increased from 2 for larger torn areas


class PaperCutoutEffect:
    """Create realistic paper cutout effects with enhanced visibility"""

    def __init__(
        self,
        edge_roughness=DEFAULT_EDGE_ROUGHNESS,
        shadow_intensity=DEFAULT_SHADOW_INTENSITY,
    ):
        """
        Initialize paper cutout effect

        Args:
            edge_roughness: How rough the edges should be (0.0 - 1.0)
            shadow_intensity: Intensity of shadow drop (0.0 - 1.0)
        """
        self.edge_roughness = edge_roughness
        self.shadow_intensity = shadow_intensity
        self.noise_generator = opensimplex.OpenSimplex(seed=42)

    def apply(self, image, mask):
        """
        Apply paper cutout effect to image

        Args:
            image (np.ndarray): Input image (BGR format)
            mask (np.ndarray): Binary mask for foreground

        Returns:
            np.ndarray: Image with paper cutout effect applied
        """
        # Create rough edges with enhanced algorithm
        rough_mask = self._create_rough_edges_enhanced(mask)

        # Add more pronounced shadow
        shadow = self._create_drop_shadow_enhanced(rough_mask)

        # Composite final image with better contrast
        result = self._composite_image_enhanced(image, rough_mask, shadow)

        return result

    def _create_rough_edges_enhanced(self, mask):
        """Create more pronounced natural torn edges using noise"""
        mask_float = mask.astype(np.float32) / 255.0
        height, width = mask.shape
        rough_mask = mask_float.copy()
        
        if self.edge_roughness > 0:
            # Use dilated edges for wider tear effect
            edges = cv2.Canny(mask, 30, 100)  # Lower thresholds for more edges
            kernel = np.ones((3, 3), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=2)  # Widen edge detection
            
            # Create distance transform for gradual tearing
            distance = cv2.distanceTransform(255 - edges, cv2.DIST_L2, 5)
            
            # Apply noise-based tearing
            for y in range(height):
                for x in range(width):
                    if distance[y, x] <= TEAR_RADIUS:  # Within tear radius of an edge
                        # Generate multiple octaves of noise for more complex patterns
                        noise1 = self.noise_generator.noise2(x / NOISE_SCALE, y / NOISE_SCALE)
                        noise2 = self.noise_generator.noise2(x / (NOISE_SCALE * 0.5), y / (NOISE_SCALE * 0.5)) * 0.5
                        combined_noise = (noise1 + noise2) * self.edge_roughness
                        
                        # More aggressive tearing based on distance from edge
                        distance_factor = 1.0 - (distance[y, x] / TEAR_RADIUS)
                        tear_intensity = combined_noise * distance_factor
                        
                        if tear_intensity < -EDGE_THRESHOLD:
                            # Create more dramatic tears
                            tear_amount = abs(tear_intensity) * 2.0
                            rough_mask[y, x] *= max(0.0, 1.0 - tear_amount)
                        elif tear_intensity > EDGE_THRESHOLD:
                            # Slight expansion in some areas for natural variation
                            rough_mask[y, x] = min(1.0, rough_mask[y, x] * (1.0 + tear_intensity * 0.3))
        
        return (rough_mask * 255).astype(np.uint8)

    def _create_drop_shadow_enhanced(self, mask):
        """Create more pronounced drop shadow"""
        shadow = mask.copy()
        
        # Multiple shadow layers for depth
        offset_x, offset_y = DEFAULT_SHADOW_OFFSET
        
        # Main shadow
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        shadow = cv2.warpAffine(shadow, M, (mask.shape[1], mask.shape[0]))
        
        # Secondary shadow for depth
        M2 = np.float32([[1, 0, offset_x // 2], [0, 1, offset_y // 2]])
        shadow2 = cv2.warpAffine(mask, M2, (mask.shape[1], mask.shape[0]))
        
        # Combine shadows
        shadow = cv2.maximum(shadow, shadow2)
        
        # Enhanced blur
        shadow = cv2.GaussianBlur(shadow, (DEFAULT_SHADOW_BLUR, DEFAULT_SHADOW_BLUR), 0)
        
        # Apply stronger shadow intensity
        shadow = (shadow * self.shadow_intensity).astype(np.uint8)
        
        return shadow

    def _composite_image_enhanced(self, image, mask, shadow, transparent_background=True):
        """Enhanced compositing with better contrast and paper texture simulation"""
        if transparent_background:
            height, width = image.shape[:2]
            result = np.zeros((height, width, 4), dtype=np.uint8)
            
            # Enhance image contrast slightly for paper effect
            enhanced_image = self._enhance_for_paper_effect(image)
            result[:, :, :3] = enhanced_image
            
            # Create more realistic alpha with shadow
            mask_alpha = mask.astype(np.float32) / 255.0
            shadow_alpha = shadow.astype(np.float32) / 255.0
            
            # Shadow creates partial transparency behind the cutout
            combined_alpha = mask_alpha.copy()
            shadow_effect = shadow_alpha * 0.6  # Stronger shadow effect
            
            # Apply shadow where there's no main object
            shadow_area = (mask_alpha < 0.1) & (shadow_alpha > 0.1)
            combined_alpha[shadow_area] = shadow_effect[shadow_area]
            
            result[:, :, 3] = (combined_alpha * 255).astype(np.uint8)
            
        else:
            # White background with more pronounced shadow
            background = np.full_like(image, 245, dtype=np.uint8)  # Slightly off-white
            
            # Create shadow gradient
            shadow_3ch = cv2.cvtColor(shadow, cv2.COLOR_GRAY2BGR)
            shadow_strength = 1.5  # Stronger shadow
            background = background - (shadow_3ch * shadow_strength)
            background = np.clip(background, 180, 255).astype(np.uint8)  # Keep some lightness
            
            # Enhanced image
            enhanced_image = self._enhance_for_paper_effect(image)
            
            # Smooth mask blending
            mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
            mask_smooth = cv2.GaussianBlur(mask_3ch, (3, 3), 0)  # Slight blur for natural blending
            
            result = background * (1 - mask_smooth) + enhanced_image * mask_smooth
            result = result.astype(np.uint8)
        
        return result

    def _enhance_for_paper_effect(self, image):
        """Enhance image to look more like it was printed on paper"""
        # Slightly increase contrast and saturation
        enhanced = image.astype(np.float32)
        
        # Increase contrast slightly
        enhanced = enhanced * 1.1 - 12
        enhanced = np.clip(enhanced, 0, 255)
        
        # Convert to HSV for saturation adjustment
        hsv = cv2.cvtColor(enhanced.astype(np.uint8), cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.15)  # Increase saturation
        
        # Convert back to BGR
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return enhanced

    def _create_rough_edges(self, mask):
        """Original method - kept for compatibility"""
        return self._create_rough_edges_enhanced(mask)

    def _create_drop_shadow(self, mask):
        """Original method - kept for compatibility"""
        return self._create_drop_shadow_enhanced(mask)

    def _composite_image(self, image, mask, shadow, transparent_background=True):
        """Original method - kept for compatibility"""
        return self._composite_image_enhanced(image, mask, shadow, transparent_background)