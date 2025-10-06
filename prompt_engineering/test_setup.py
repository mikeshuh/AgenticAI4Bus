"""
Test script to verify the setup for all three prompt engineering notebooks.
This script tests that all required dependencies are installed and API access works.
"""

import os
import sys

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    try:
        import pandas as pd
        print("✓ pandas imported successfully")

        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")

        from google import genai
        print("✓ google-genai imported successfully")

        from dotenv import load_dotenv
        print("✓ python-dotenv imported successfully")

        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_env_setup():
    """Test that environment variables are properly configured."""
    print("\nTesting environment setup...")
    from dotenv import load_dotenv

    # Load .env file from parent directory
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(env_path)

    api_key = os.getenv('GEMINI_API_KEY')

    if api_key:
        print(f"✓ GEMINI_API_KEY found (length: {len(api_key)})")
        return True
    else:
        print("✗ GEMINI_API_KEY not found in .env file")
        return False

def test_api_connection():
    """Test that we can connect to the Gemini API."""
    print("\nTesting Gemini API connection...")
    try:
        from google import genai
        from dotenv import load_dotenv

        # Load environment variables
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(env_path)

        # Initialize client
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

        # Make a simple test request
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents='Say "Hello" in one word.'
        )

        print(f"✓ API connection successful")
        print(f"  Response: {response.text.strip()}")
        return True

    except Exception as e:
        print(f"✗ API connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("PROMPT ENGINEERING SETUP TEST")
    print("=" * 80)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Environment", test_env_setup()))
    results.append(("API Connection", test_api_connection()))

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 80)

    if all_passed:
        print("\n🎉 All tests passed! Ready to run the notebooks.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running notebooks.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
