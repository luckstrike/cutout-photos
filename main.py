"""
Paper Cutout Photo Effect - Scissor-Cut CLI with Enhanced Control
"""

import argparse
import os
import sys
from backend.core.processor import ImageProcessor
from backend.core.utils import hex_to_rgb

def main():
    parser = argparse.ArgumentParser(
        description="Create realistic scissor-cut paper cutout effects from photos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        # Basic usage
        python main.py photo.jpg cutout.png
        # Changing the outline thickness, detail level, and color
        python main.py -o 25 -d 50 -b FF0000 photo.jpg cutout.png
        """
    )
    
    parser.add_argument("input", 
                        help="Input image file or directory")
    parser.add_argument("output", 
                        help="Output image file or directory")
    parser.add_argument("-o", '--outline_thickness',
                        default=15,
                        help="Max outline thickness of the cutout")
    parser.add_argument("-d", "--detail",
                        default=25,
                        help="How big the cut lines will be, the higher the detail" \
                        " the more polygonal the cutout will look")
    parser.add_argument("-b", "--background_color",
                        default="#FFFFFF", 
                        help="Hex code for background color of the cutout's outline")
    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    # Create processor with selected settings
    processor = ImageProcessor(
        background_color=hex_to_rgb(args.background_color),
        detail=int(args.detail),
        outline_thickness=int(args.outline_thickness)
    )

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