# Raspberry Pi WiFi Aware Control Service

This directory contains the Raspberry Pi implementation that acts as the WiFi Aware service publisher and coordinator.

## Overview

The RPi serves as the control device in the WiFi Aware investigation, publishing a discoverable service that Android and iOS clients can find and connect to.

## Prerequisites

- Raspberry Pi 4 or newer
- WiFi Aware capable hardware
- Python 3.8+
- See [docs/rpi-setup.md](../docs/rpi-setup.md) for complete setup instructions

## Quick Start

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the service
sudo python3 main.py
```

## Project Structure

```plaintext
rpi/
├── src/                          # Source code
│   ├── wifi_aware_manager.py    # Main WiFi Aware controller
│   ├── publisher.py              # Service publisher
│   ├── discovery.py              # Device discovery handler
│   ├── data_path.py              # Data exchange handler
│   └── protocol.py               # Message protocol
├── tests/                        # Unit tests
├── config/                       # Configuration files
│   ├── settings.yaml
│   └── logging.yaml
├── scripts/                      # Utility scripts
│   ├── start_service.sh
│   └── test_connection.sh
├── requirements.txt              # Python dependencies
└── main.py                       # Entry point
```

## Configuration

Edit `config/settings.yaml` to customize:

- Service name
- Network interface
- Logging levels
- Message protocols

## Running as a Service

Install as systemd service:

```bash
sudo cp scripts/wifi-aware.service /etc/systemd/system/
sudo systemctl enable wifi-aware
sudo systemctl start wifi-aware
```

## Testing

Run unit tests:

```bash
pytest tests/
```

Manual testing:

```bash
./scripts/test_connection.sh
```

## Documentation

For detailed setup and troubleshooting, see:
- [RPi Setup Guide](../docs/rpi-setup.md)
- [Architecture Documentation](../docs/architecture.md)

## Current State

🚧 **Entry point created, core implementation pending**

**Implemented:**

- Project structure with virtual environment support
- Entry point (`main.py`) with logging and signal handling
- Configuration structure (`config/settings.yaml`)
- Dependency management (`requirements.txt`)
- Basic startup script (`scripts/start_service.sh`)

**Pending:**

- Core WiFi Aware manager (`src/wifi_aware_manager.py`)
- wpa_supplicant integration for NAN operations
- Service publisher implementation
- Device discovery and connection handlers
- Data path and message protocol
- Network interface management
- Test utilities and validation scripts

**Note:** Requires root privileges to run due to WiFi interface management requirements.
