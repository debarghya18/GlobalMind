#!/usr/bin/env python3
"""
Launch script for GlobalMind Streamlit UI
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Streamlit UI"""
    print("Starting GlobalMind UI...")
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Path to the Streamlit app
    app_path = script_dir / "src" / "ui" / "streamlit_app.py"
    
    # Check if the app file exists
    if not app_path.exists():
        print(f"Error: Streamlit app not found at {app_path}")
        sys.exit(1)
    
    # Set environment variables
    os.environ['PYTHONPATH'] = str(script_dir)
    
    try:
        # Launch Streamlit
        cmd = [
            sys.executable, 
            "-m", 
            "streamlit", 
            "run", 
            str(app_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--theme.base=light",
            "--theme.primaryColor=#667eea",
            "--theme.backgroundColor=#f0f2f6",
            "--theme.secondaryBackgroundColor=#ffffff",
            "--theme.textColor=#2c3e50"
        ]
        
        print(f"Launching Streamlit UI...")
        print(f"URL: http://localhost:8501")
        print(f"Press Ctrl+C to stop the server")
        
        # Run the command
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopping GlobalMind UI...")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
