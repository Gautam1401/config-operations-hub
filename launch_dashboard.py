"""
Launch script for ARC Configuration Dashboard
Simple one-click launcher
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Streamlit dashboard"""
    
    # Get the path to the app
    app_path = Path(__file__).parent / "arc_dashboard" / "app.py"
    
    print("=" * 60)
    print("🚀 Launching ARC Configuration Dashboard")
    print("=" * 60)
    print(f"\nApp Path: {app_path}")
    print("\nStarting Streamlit server...")
    print("\nThe dashboard will open in your default browser.")
    print("Press Ctrl+C to stop the server.\n")
    print("=" * 60)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped successfully")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

