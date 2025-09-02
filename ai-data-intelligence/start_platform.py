#!/usr/bin/env python3
"""
AI Data Intelligence Platform - Startup Script

This script starts the complete AI data intelligence and reporting platform.
"""

import sys
import os
import asyncio
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import platform components
try:
    from demo_enterprise_platform import main as run_enterprise_demo
    print("AI Enterprise platform imported successfully")
except ImportError as e:
    print(f"Failed to import enterprise platform: {e}")
    print("Please ensure all dependencies are installed.")
    sys.exit(1)

async def start_platform():
    """Start the AI data intelligence platform"""
    print("Starting AI Data Intelligence Platform...")
    
    try:
        # Run the enterprise demo
        await run_enterprise_demo()
        
    except KeyboardInterrupt:
        print("\nPlatform shutdown requested by user")
    except Exception as e:
        print(f"Platform error: {e}")
        return False
    
    return True

def main():
    """Main entry point"""
    print("*" * 30)
    print("AI DATA INTELLIGENCE PLATFORM")
    print("*" * 30)
    
    # Run the platform
    try:
        asyncio.run(start_platform())
    except Exception as e:
        print(f"Startup failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
