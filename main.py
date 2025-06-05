"""
Paper Cutout Photo Effect - Command Line Interface
"""

import argparse
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create paper cutout effects from photos"
    )
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")

    args = parser.parse_args()

    # Validating the inputs
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)

    # Process input
    if os.path.isfile(args.input):
        # process image here
        pass
    elif os.path.isdir(args.input):
        # process all of the images in the directory here
        pass
    else:
        print(f"Error: Input path '{args.input}' is neither a file nor directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
