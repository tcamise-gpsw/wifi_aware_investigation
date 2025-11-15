#!/usr/bin/env python3
"""
WiFi Aware Control Service - Main Entry Point

This script initializes and runs the WiFi Aware service on Raspberry Pi.
"""

import sys
import logging
import signal
from pathlib import Path

# TODO: Implement WiFi Aware manager
# from src.wifi_aware_manager import WiFiAwareManager


def setup_logging():
    """Configure logging for the service."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/wifi_aware.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger = logging.getLogger(__name__)
    logger.info(f"Received signal {signum}, shutting down...")
    # TODO: Cleanup WiFi Aware session
    sys.exit(0)


def main():
    """Main entry point for the WiFi Aware service."""
    logger = setup_logging()
    logger.info("Starting WiFi Aware Control Service")

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # TODO: Initialize WiFi Aware manager
        # manager = WiFiAwareManager()
        # manager.start_publisher(service_name="rpi_control_service")

        logger.info("WiFi Aware service is running...")
        logger.info("Press Ctrl+C to stop")

        # Keep the service running
        signal.pause()

    except Exception as e:
        logger.error(f"Failed to start WiFi Aware service: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
