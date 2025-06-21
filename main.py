"""
Paper Cutout Photo Effect - Scissor-Cut CLI with Enhanced Control
"""

import argparse
import os
import sys
from src.processor import ImageProcessor

def main():
    parser = argparse.ArgumentParser(
        description="Create realistic scissor-cut paper cutout effects from photos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        # Basic usage (moderate cuts)
        python main.py photo.jpg cutout.png
        """
    )
    
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)

    
    # Create processor with selected settings
    processor = ImageProcessor()

    # Process input
    if os.path.isfile(args.input):
        # Process single image
        print(f"📸 Processing single image: {args.input}")
        
        success = processor.process_image(args.input, args.output)

        if success:
            print("✅ Processing completed successfully!")
            print(f"📁 Output saved to: {args.output}")
        else:
            print("❌ Processing failed!")
            sys.exit(1)

    elif os.path.isdir(args.input):
        # Process all images in directory
        print(f"📁 Processing directory: {args.input}")
        
        processor.process_directory(args.input, args.output, args.save_steps)

    else:
        print(f"Error: Input path '{args.input}' is neither a file nor directory")
        sys.exit(1)

if __name__ == "__main__":
    main()