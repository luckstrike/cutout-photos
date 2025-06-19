"""
Configuration settings for paper cutout effect with enhanced presets
"""

# Enhanced default settings for more noticeable effects
class PaperCutoutConfig:
    """Configuration class for paper cutout effects"""
    
    # Edge roughness settings
    EDGE_ROUGHNESS_SUBTLE = 0.3
    EDGE_ROUGHNESS_MODERATE = 0.6
    EDGE_ROUGHNESS_DRAMATIC = 0.9
    
    # Shadow intensity settings  
    SHADOW_INTENSITY_LIGHT = 0.4
    SHADOW_INTENSITY_MODERATE = 0.8
    SHADOW_INTENSITY_HEAVY = 1.2
    
    # Preset combinations
    PRESET_SUBTLE = {
        'edge_roughness': EDGE_ROUGHNESS_SUBTLE,
        'shadow_intensity': SHADOW_INTENSITY_LIGHT,
        'shadow_offset': (5, 5),
        'shadow_blur': 15,
        'noise_scale': 12.0,
        'edge_threshold': 0.25,
        'tear_radius': 3
    }
    
    PRESET_MODERATE = {
        'edge_roughness': EDGE_ROUGHNESS_MODERATE,
        'shadow_intensity': SHADOW_INTENSITY_MODERATE,
        'shadow_offset': (8, 8),
        'shadow_blur': 25,
        'noise_scale': 8.0,
        'edge_threshold': 0.15,
        'tear_radius': 4
    }
    
    PRESET_DRAMATIC = {
        'edge_roughness': EDGE_ROUGHNESS_DRAMATIC,
        'shadow_intensity': SHADOW_INTENSITY_HEAVY,
        'shadow_offset': (12, 12),
        'shadow_blur': 35,
        'noise_scale': 5.0,
        'edge_threshold': 0.1,
        'tear_radius': 6
    }
    
    # Default preset
    DEFAULT_PRESET = PRESET_MODERATE

# Background removal settings
class BackgroundRemovalConfig:
    """Configuration for background removal"""
    
    # Supported formats
    SUPPORTED_INPUT_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    OUTPUT_FORMAT = '.png'  # Always PNG to preserve transparency
    
    # Processing settings
    BATCH_PROCESSING = True
    PRESERVE_ORIGINAL_SIZE = True

# GUI settings (for future GUI implementation)
class GUIConfig:
    """Configuration for GUI application"""
    
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    PREVIEW_SIZE = (400, 400)
    
    # Real-time preview settings
    ENABLE_REAL_TIME_PREVIEW = True
    PREVIEW_UPDATE_DELAY = 100  # milliseconds