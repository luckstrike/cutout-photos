"""
Paper Cutout Photo Effect - Enhanced Command Line Interface with Presets
"""

import argparse
import os
import sys
from src.processor import ImageProcessor
from src.config import PaperCutoutConfig

def main():
    parser = argparse.ArgumentParser(
        description="Create paper cutout effects from photos with enhanced presets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                Preset Examples:
                --preset subtle    : Light effect for professional photos
                --preset moderate  : Balanced effect (default)
                --preset dramatic  : Strong effect for artistic photos

                Custom Examples:
                python main.py input.jpg output.png --edge-roughness 0.8 --shadow-intensity 1.0
                python main.py input_folder/ output_folder/ --preset dramatic
                """
    )
    
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")
    
    # Preset selection
    parser.add_argument("--preset", choices=['subtle', 'moderate', 'dramatic'],
                        default='moderate',
                        help="Use predefined effect presets (default: moderate)")
    
    # Manual parameter overrides
    parser.add_argument("--edge-roughness", type=float,
                        help="Edge roughness (0.0-1.0). Overrides preset setting.")
    parser.add_argument("--shadow-intensity", type=float,
                        help="Shadow intensity (0.0-1.5). Overrides preset setting.")
    
    # Advanced options
    parser.add_argument("--no-enhancement", action="store_true",
                        help="Disable image enhancement (contrast/saturation boost)")
    parser.add_argument("--white-background", action="store_true",
                        help="Use white background instead of transparent")
    parser.add_argument("--preview-steps", action="store_true",
                        help="Save intermediate processing steps for debugging")

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Get preset configuration
    preset_map = {
        'subtle': PaperCutoutConfig.PRESET_SUBTLE,
        'moderate': PaperCutoutConfig.PRESET_MODERATE,
        'dramatic': PaperCutoutConfig.PRESET_DRAMATIC
    }
    
    config = preset_map[args.preset].copy()
    
    # Override with manual parameters if provided
    if args.edge_roughness is not None:
        config['edge_roughness'] = args.edge_roughness
    if args.shadow_intensity is not None:
        config['shadow_intensity'] = args.shadow_intensity
    
    # Display selected settings
    print(f"Using '{args.preset}' preset with settings:")
    print(f"  Edge Roughness: {config['edge_roughness']:.2f}")
    print(f"  Shadow Intensity: {config['shadow_intensity']:.2f}")
    print(f"  Enhancement: {'Disabled' if args.no_enhancement else 'Enabled'}")
    print(f"  Background: {'White' if args.white_background else 'Transparent'}")
    print()
    
    # Create processor with selected settings
    processor = ImageProcessor(
        edge_roughness=config['edge_roughness'],
        shadow_intensity=config['shadow_intensity']
    )
    
    # Configure additional options
    if hasattr(processor, 'paper_effect'):
        processor.paper_effect.use_enhancement = not args.no_enhancement
        processor.paper_effect.transparent_background = not args.white_background
        processor.paper_effect.save_preview_steps = args.preview_steps

    # Process input
    if os.path.isfile(args.input):
        # Process single image
        print(f"Processing single image: {args.input}")
        success = processor.process_image(args.input, args.output)

        if success:
            print("Processing completed successfully!")
            print(f"Output saved to: {args.output}")
        else:
            print("Processing failed!")
            sys.exit(1)

    elif os.path.isdir(args.input):
        # Process all images in directory
        print(f"Processing directory: {args.input}")
        processor.process_directory(args.input, args.output)

    else:
        print(f"Error: Input path '{args.input}' is neither a file nor directory")
        sys.exit(1)

def print_examples():
    """Print usage examples"""
    print("\nUsage Examples:")
    print("  # Basic usage with moderate preset:")
    print("  python main.py photo.jpg cutout.png")
    print()
    print("  # Dramatic effect:")
    print("  python main.py photo.jpg cutout.png --preset dramatic")
    print()
    print("  # Custom settings:")
    print("  python main.py photo.jpg cutout.png --edge-roughness 0.9 --shadow-intensity 1.2")
    print()
    print("  # Process entire directory:")
    print("  python main.py input_photos/ output_cutouts/ --preset dramatic")
    print()
    print("  # White background instead of transparent:")
    print("  python main.py photo.jpg cutout.png --white-background")

if __name__ == "__main__":
    main()