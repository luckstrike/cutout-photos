"""
Configuration settings for paper cutout effect with enhanced presets
"""

class ScissorCutoutConfig:
    """Configuration class for scissor-cut paper cutout effects"""
    
    # Scissor-cut presets
    PRESET_GENTLE_CUTS = {
        'edge_roughness': 0.4,
        'shadow_intensity': 0.6,
        'cut_length_min': 6,
        'cut_length_max': 15,
        'cut_frequency': 0.2,
        'cut_depth': 5,
        'shadow_offset': (6, 6),
        'shadow_blur': 20
    }
    
    PRESET_MODERATE_CUTS = {
        'edge_roughness': 0.7,
        'shadow_intensity': 0.8,
        'cut_length_min': 10,
        'cut_length_max': 25,
        'cut_frequency': 0.3,
        'cut_depth': 8,
        'shadow_offset': (10, 10),
        'shadow_blur': 30
    }
    
    PRESET_AGGRESSIVE_CUTS = {
        'edge_roughness': 0.9,
        'shadow_intensity': 1.0,
        'cut_length_min': 15,
        'cut_length_max': 35,
        'cut_frequency': 0.5,
        'cut_depth': 12,
        'shadow_offset': (15, 15),
        'shadow_blur': 40
    }
    
    PRESET_DRAMATIC_CUTS = {
        'edge_roughness': 1.0,
        'shadow_intensity': 1.2,
        'cut_length_min': 20,
        'cut_length_max': 50,
        'cut_frequency': 0.7,
        'cut_depth': 15,
        'shadow_offset': (18, 18),
        'shadow_blur': 45
    }
    
    # Default preset
    DEFAULT_PRESET = PRESET_MODERATE_CUTS