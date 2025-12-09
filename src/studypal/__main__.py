"""Entry point for running StudyPal as a module."""

import sys
import os
from pathlib import Path

# Fix Windows console encoding to support Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7 fallback
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from .cli import CLI

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required if env vars set manually


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
