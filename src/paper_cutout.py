"""
Paper cutout effect implementation
"""

import cv2
import numpy as np
import opensimplex

# Default settings
DEFAULT_EDGE_ROUGHNESS = 0.3
DEFAULT_SHADOW_INTENSITY = 0.5
DEFAULT_SHADOW_OFFSET = (5, 5)
DEFAULT_SHADOW_BLUR = 15
NOISE_SCALE = 20.0
EDGE_THRESHOLD = 0.3


class PaperCutoutEffect:
    """Create realistic paper cutout effects"""

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
        # Create rough edges
        rough_mask = self._create_rough_edges(mask)

        # Add shadow drop
        shadow = self._create_drop_shadow(rough_mask)

        # Composite final image
        result = self._composite_image(image, rough_mask, shadow)

        return result

    def _create_rough_edges(self, mask):
        """Create natural torn edges using noise"""
        # Convert mask to float for processing
        mask_float = mask.astype(np.float32) / 255.0
        
        # Create noise for edge roughness
        height, width = mask.shape
        rough_mask = mask_float.copy()
        
        # Only apply roughness if edge_roughness > 0
        if self.edge_roughness > 0:
            # Find edges
            edges = cv2.Canny(mask, 50, 150)
            edge_pixels = np.where(edges > 0)
            
            # Add noise to edge pixels
            for y, x in zip(edge_pixels[0], edge_pixels[1]):
                # Generate noise value
                noise = self.noise_generator.noise2(x / NOISE_SCALE, y / NOISE_SCALE)
                # Scale noise by roughness parameter
                noise_scaled = noise * self.edge_roughness
                
                # Apply noise to nearby pixels
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            # Reduce mask value based on noise
                            if noise_scaled < -EDGE_THRESHOLD:
                                rough_mask[ny, nx] *= (1.0 + noise_scaled)
                                rough_mask[ny, nx] = max(0, rough_mask[ny, nx])
        
        # Convert back to uint8
        return (rough_mask * 255).astype(np.uint8)

    def _create_drop_shadow(self, mask):
        """Create drop shadow from mask"""
        # Create shadow by shifting and blurring the mask
        shadow = mask.copy()
        
        # Shift shadow (offset)
        offset_x, offset_y = DEFAULT_SHADOW_OFFSET
        M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        shadow = cv2.warpAffine(shadow, M, (mask.shape[1], mask.shape[0]))
        
        # Blur shadow
        shadow = cv2.GaussianBlur(shadow, (DEFAULT_SHADOW_BLUR, DEFAULT_SHADOW_BLUR), 0)
        
        # Apply shadow intensity
        shadow = (shadow * self.shadow_intensity).astype(np.uint8)
        
        return shadow

    def _composite_image(self, image, mask, shadow, transparent_background=True):
        """Composite image with mask and shadow"""
        if transparent_background:
            # Create RGBA image with transparent background
            height, width = image.shape[:2]
            result = np.zeros((height, width, 4), dtype=np.uint8)
            
            # Set RGB channels from original image
            result[:, :, :3] = image
            
            # Set alpha channel from mask
            result[:, :, 3] = mask
            
            # Apply shadow to alpha channel (darken but keep some transparency)
            shadow_alpha = mask.astype(np.float32) / 255.0
            shadow_effect = (shadow.astype(np.float32) / 255.0) * 0.3  # Subtle shadow on alpha
            result[:, :, 3] = ((shadow_alpha - shadow_effect) * 255).clip(0, 255).astype(np.uint8)
            
        else:
            # Original white background method
            background = np.full_like(image, 255, dtype=np.uint8)
            
            # Apply shadow to background
            shadow_3ch = cv2.cvtColor(shadow, cv2.COLOR_GRAY2BGR)
            background = background - shadow_3ch
            background = np.clip(background, 0, 255).astype(np.uint8)
            
            # Apply main mask
            mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
            
            # Composite: background where mask is 0, image where mask is 1
            result = background * (1 - mask_3ch) + image * mask_3ch
            result = result.astype(np.uint8)
        
        return result

    def _tear_around_pixel(self, mask, x, y, size=3):
        """Create small torn area around a pixel"""
        # This method can be used for more detailed tearing effects
        # For now, it's not used in the main pipeline
        pass