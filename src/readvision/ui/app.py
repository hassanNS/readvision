#!/usr/bin/env python3
"""
Simple launcher for the ReadVision Streamlit UI
"""

import subprocess
import sys
from pathlib import Path


def launch_ui():
    """Launch the Streamlit UI."""
    # Get the path to the streamlit app
    ui_path = Path(__file__).parent / "streamlit_app.py"

    # Launch streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(ui_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching UI: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down ReadVision UI...")
        sys.exit(0)


if __name__ == "__main__":
    launch_ui()