#!/usr/bin/env python3
"""
Setup script for GlobalMind installation
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        "data",
        "logs",
        "models/offline",
        "backups"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def setup_environment():
    """Setup environment variables"""
    print("Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write("# GlobalMind Environment Variables\n")
            f.write("GLOBALMIND_ENV=development\n")
            f.write("GLOBALMIND_LOG_LEVEL=INFO\n")
            f.write("GLOBALMIND_DB_PATH=data/globalmind.db\n")
        print("✓ Created .env file")

def setup_database():
    """Setup database"""
    print("Setting up database...")
    # Database setup will be handled by the application
    print("✓ Database setup configured")

def main():
    """Main setup function"""
    print("=" * 50)
    print("GlobalMind Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Setup database
    setup_database()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nTo start GlobalMind:")
    print("python main.py")
    print("\nTo run tests:")
    print("python -m pytest tests/")

if __name__ == "__main__":
    main()
