"""
Paper Cutout Photo Effect - Command Line Interface
"""

import argparse
import os
import sys
from src.processor import ImageProcessor

def main():
    parser = argparse.ArgumentParser(
        description="Create paper cutout effects from photos"
    )
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")
    parser.add_argument("--edge-roughness", type=float, default=0.3,
                        help="Edge roughness (0.0-1.0, default: 0.3)")
    parser.add_argument("--shadow-intensity", type=float, default=0.5,
                        help="Shadow intensity (0.0-1.0, default: 0.5)")

    args = parser.parse_args()

    # Validating the inputs
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Create the processor with user settings
    processor = ImageProcessor(
        edge_roughness=args.edge_roughness,
        shadow_intensity=args.shadow_intensity
    )

    # Process input
    if os.path.isfile(args.input):
        # Process single image
        print(f"Processing single image: {args.input}")
        success = processor.process_image(args.input, args.output)

        if success:
            print("Processing completed successfully!")
        else:
            print("Processing failed!")
            sys.exit(1)

    elif os.path.isdir(args.input):
        # Process all images in a directory
        print(f"Processing directory: {args.input}")
        processor.process_directory(args.input, args.output)

    else:
        print(f"Error: Input path '{args.input}' is neither a file nor directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
