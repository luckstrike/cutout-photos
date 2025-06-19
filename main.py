"""
Paper Cutout Photo Effect - Scissor-Cut CLI with Enhanced Control
"""

import argparse
import os
import sys
from src.processor import ImageProcessor
from src.config import ScissorCutoutConfig

def main():
    parser = argparse.ArgumentParser(
        description="Create realistic scissor-cut paper cutout effects from photos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scissor-Cut Presets:
  --preset gentle     : Light, subtle scissor cuts
  --preset moderate   : Balanced cuts (default)
  --preset aggressive : Pronounced jagged cuts
  --preset dramatic   : Very dramatic cuts with long tears

Examples:
  # Basic usage (moderate cuts)
  python main.py photo.jpg cutout.png

  # Aggressive cuts for artistic effect
  python main.py photo.jpg cutout.png --preset aggressive

  # Custom scissor settings
  python main.py photo.jpg cutout.png --cut-length 15-40 --cut-frequency 0.6

  # Process directory with dramatic cuts
  python main.py photos/ cutouts/ --preset dramatic --save-steps
        """
    )
    
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")
    
    # Preset selection
    parser.add_argument("--preset", choices=['gentle', 'moderate', 'aggressive', 'dramatic'],
                        default='moderate',
                        help="Use predefined scissor-cut presets (default: moderate)")
    
    # Scissor-specific parameters
    parser.add_argument("--cut-length", type=str, metavar="MIN-MAX",
                        help="Scissor cut length range in pixels (e.g., '10-25')")
    parser.add_argument("--cut-frequency", type=float, metavar="0.0-1.0",
                        help="How often to make cuts (0.0=none, 1.0=maximum)")
    parser.add_argument("--cut-depth", type=int, metavar="PIXELS",
                        help="How deep cuts penetrate into the object")
    
    # General effect parameters
    parser.add_argument("--edge-roughness", type=float, metavar="0.0-1.0",
                        help="Overall effect intensity")
    parser.add_argument("--shadow-intensity", type=float, metavar="0.0-1.5",
                        help="Shadow darkness")
    
    # Processing options
    parser.add_argument("--white-background", action="store_true",
                        help="Use white background instead of transparent")
    parser.add_argument("--save-steps", action="store_true",
                        help="Save intermediate processing steps for debugging")
    parser.add_argument("--quiet", action="store_true",
                        help="Reduce output verbosity")

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Get preset configuration
    preset_map = {
        'gentle': ScissorCutoutConfig.PRESET_GENTLE_CUTS,
        'moderate': ScissorCutoutConfig.PRESET_MODERATE_CUTS,
        'aggressive': ScissorCutoutConfig.PRESET_AGGRESSIVE_CUTS,
        'dramatic': ScissorCutoutConfig.PRESET_DRAMATIC_CUTS
    }
    
    config = preset_map[args.preset].copy()
    
    # Parse and apply manual parameter overrides
    if args.cut_length:
        try:
            min_val, max_val = map(int, args.cut_length.split('-'))
            config['cut_length_min'] = min_val
            config['cut_length_max'] = max_val
        except ValueError:
            print(f"Error: Invalid cut-length format. Use 'MIN-MAX' (e.g., '10-25')")
            sys.exit(1)
    
    if args.cut_frequency is not None:
        if 0.0 <= args.cut_frequency <= 1.0:
            config['cut_frequency'] = args.cut_frequency
        else:
            print(f"Error: cut-frequency must be between 0.0 and 1.0")
            sys.exit(1)
    
    if args.cut_depth is not None:
        if args.cut_depth > 0:
            config['cut_depth'] = args.cut_depth
        else:
            print(f"Error: cut-depth must be positive")
            sys.exit(1)
    
    if args.edge_roughness is not None:
        if 0.0 <= args.edge_roughness <= 1.0:
            config['edge_roughness'] = args.edge_roughness
        else:
            print(f"Error: edge-roughness must be between 0.0 and 1.0")
            sys.exit(1)
    
    if args.shadow_intensity is not None:
        if 0.0 <= args.shadow_intensity <= 1.5:
            config['shadow_intensity'] = args.shadow_intensity
        else:
            print(f"Error: shadow-intensity must be between 0.0 and 1.5")
            sys.exit(1)
    
    # Display selected settings
    if not args.quiet:
        print(f"🪄 Scissor-Cut Paper Cutout Effect")
        print(f"📋 Using '{args.preset}' preset with settings:")
        print(f"   Edge Roughness: {config['edge_roughness']:.2f}")
        print(f"   Cut Length: {config['cut_length_min']}-{config['cut_length_max']} pixels")
        print(f"   Cut Frequency: {config['cut_frequency']:.1%}")
        print(f"   Cut Depth: {config['cut_depth']} pixels")
        print(f"   Shadow Intensity: {config['shadow_intensity']:.2f}")
        print(f"   Background: {'White' if args.white_background else 'Transparent'}")
        print(f"   Save Steps: {'Yes' if args.save_steps else 'No'}")
        print()
    
    # Create processor with selected settings
    processor = ImageProcessor(
        edge_roughness=config['edge_roughness'],
        shadow_intensity=config['shadow_intensity'],
        cut_length_min=config['cut_length_min'],
        cut_length_max=config['cut_length_max'],
        cut_frequency=config['cut_frequency'],
        cut_depth=config['cut_depth']
    )
    
    # Configure additional options
    if hasattr(processor.paper_effect, '_composite_image'):
        # These would need to be added to the effect class if we want them configurable
        pass

    # Process input
    if os.path.isfile(args.input):
        # Process single image
        if not args.quiet:
            print(f"📸 Processing single image: {args.input}")
        
        success = processor.process_image(args.input, args.output, args.save_steps)

        if success:
            if not args.quiet:
                print("✅ Processing completed successfully!")
                print(f"📁 Output saved to: {args.output}")
        else:
            print("❌ Processing failed!")
            sys.exit(1)

    elif os.path.isdir(args.input):
        # Process all images in directory
        if not args.quiet:
            print(f"📁 Processing directory: {args.input}")
        
        processor.process_directory(args.input, args.output, args.save_steps)

    else:
        print(f"Error: Input path '{args.input}' is neither a file nor directory")
        sys.exit(1)

def print_examples():
    """Print detailed usage examples"""
    print("\n🔗 Usage Examples:")
    print("\n📌 Basic Examples:")
    print("  python main.py photo.jpg cutout.png")
    print("  python main.py photo.jpg cutout.png --preset aggressive")
    print("\n📌 Custom Scissor Settings:")
    print("  python main.py photo.jpg cutout.png --cut-length 20-50 --cut-frequency 0.8")
    print("  python main.py photo.jpg cutout.png --cut-depth 15 --edge-roughness 0.9")
    print("\n📌 Batch Processing:")
    print("  python main.py photos/ cutouts/ --preset dramatic")
    print("  python main.py photos/ cutouts/ --save-steps --quiet")
    print("\n📌 Advanced Options:")
    print("  python main.py photo.jpg cutout.png --white-background --save-steps")

if __name__ == "__main__":
    main()