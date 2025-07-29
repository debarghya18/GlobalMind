#!/usr/bin/env python3
"""
GlobalMind: Culturally-Adaptive Mental Health AI Support System
Main application entry point
"""

import asyncio
import sys
from pathlib import Path
from loguru import logger

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.app import GlobalMindApp
from src.core.config import load_config
from src.core.exceptions import GlobalMindException


async def main():
    """Main application entry point"""
    try:
        logger.info("Starting GlobalMind Mental Health AI Support System")
        
        # Load configuration
        config = load_config()
        
        # Initialize the application
        app = GlobalMindApp(config)
        
        # Start the application
        await app.start()
        
    except GlobalMindException as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
