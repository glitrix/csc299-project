"""Entry point for running StudyPal as a module."""

import sys
import os
from pathlib import Path
from .cli import CLI


def main():
    """Main entry point for StudyPal."""
    # Determine data directory
    # Default to ./data relative to current working directory
    data_dir = os.getenv("STUDYPAL_DATA", "data")
    
    # Parse command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print("StudyPal - A terminal-based study assistant")
            print("\nUsage: python -m studypal [options]")
            print("\nOptions:")
            print("  --data-dir PATH    Custom data directory (default: ./data)")
            print("  --help, -h         Show this help message")
            sys.exit(0)
        elif sys.argv[1] == "--data-dir" and len(sys.argv) > 2:
            data_dir = sys.argv[2]
    
    # Create and run CLI
    try:
        cli = CLI(data_dir)
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
