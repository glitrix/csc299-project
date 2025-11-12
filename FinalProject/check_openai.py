"""Check OpenAI API configuration for StudyPal."""

import os
import sys

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ python-dotenv is installed")
except ImportError:
    print("✗ python-dotenv is not installed")
    print("  Install with: pip install python-dotenv")

# Check for OpenAI package
try:
    import openai
    print("✓ openai package is installed")
    print(f"  Version: {openai.__version__}")
except ImportError:
    print("✗ openai package is not installed")
    print("  Install with: pip install openai")
    sys.exit(1)

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    # Don't print the full key for security
    print("✓ OPENAI_API_KEY is configured")
    print(f"  Key starts with: {api_key[:10]}...")
    
    # Test the API key
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Make a minimal test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'hello'"}],
            max_tokens=5
        )
        print("✓ API key is valid and working!")
        print("  Your StudyPal planning commands will use AI enhancement.")
        
    except Exception as e:
        print(f"✗ API key validation failed: {e}")
        print("  Check your API key or billing settings at https://platform.openai.com")
else:
    print("✗ OPENAI_API_KEY is not set")
    print("  StudyPal will use basic planning mode (still fully functional)")
    print("\n  To enable AI features:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your OpenAI API key to the .env file")
    print("  3. See OPENAI_SETUP.md for detailed instructions")

print("\n" + "="*60)
print("Configuration check complete!")
print("="*60)
