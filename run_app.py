"""
Run Hospital Management System GUI Application
Streamlit Web Application
"""

import sys
import os
import subprocess

if __name__ == "__main__":
    print("=" * 70)
    print("Hospital Management System - Starting Streamlit Application")
    print("=" * 70)
    print("\nThe application will open in your web browser.")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the application.")
    print("=" * 70 + "\n")
    
    try:
        # Run Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\nError starting application: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Streamlit is installed: python -m pip install streamlit")
        print("2. Check that app.py exists in the project root")
        print("3. Verify all dependencies are installed: python -m pip install -r requirements.txt")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: Could not find Python or Streamlit.")
        print("Make sure Python is installed and Streamlit is available:")
        print("  python -m pip install streamlit")
        sys.exit(1)
