# Raspberry Pi WiFi Aware Control Service

This directory contains the Raspberry Pi implementation that acts as the WiFi Aware service publisher and coordinator.

## Overview

The RPi serves as the control device in the WiFi Aware investigation, publishing a discoverable service that Android and iOS clients can find and connect to.

## Prerequisites

### Hardware

- Raspberry Pi 4 or newer (recommended)
- WiFi adapter with WiFi Aware (NAN) support
  - Built-in WiFi on RPi 4 (Broadcom BCM43455) supports WiFi Aware
  - Alternative: External USB WiFi adapter with NAN support

### Software

- Raspberry Pi OS (64-bit recommended, Bookworm or newer)
- Python 3.8+
- wpa_supplicant 2.10+ with NAN support
- NetworkManager

## System Setup

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
sudo apt install -y \
    wpasupplicant \
    network-manager \
    python3-pip \
    python3-venv \
    iw \
    git
```

### 3. Verify WiFi Aware Support

```bash
# Check for NAN support
iw list | grep -i "nan"

# Should see "nan" in supported interface modes

# Verify wpa_supplicant version (need 2.10+)
wpa_supplicant -v
```

### 4. Configure NetworkManager

Stop dhcpcd and enable NetworkManager:

```bash
sudo systemctl stop dhcpcd
sudo systemctl disable dhcpcd
sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager
```

## Python Environment Setup

### 1. Navigate to Project

```bash
cd /path/to/wifi_aware_investigation/rpi
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Edit `config/settings.yaml` to customize:

```yaml
wifi_aware:
  service_name: "rpi_control_service"
  service_info: "RPi WiFi Aware Control"

network:
  interface: "wlan0"

logging:
  level: "INFO"
  file: "/var/log/wifi_aware.log"
```

## Running the Service

### Manual Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run with sudo (required for WiFi operations)
sudo python3 main.py
```

### Run as Systemd Service

Install as system service:

```bash
sudo cp scripts/wifi-aware.service /etc/systemd/system/
sudo systemctl enable wifi-aware
sudo systemctl start wifi-aware
```

Check status:

```bash
sudo systemctl status wifi-aware
```

View logs:

```bash
sudo journalctl -u wifi-aware -f
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

## Testing

Run Python tests:

```bash
pytest tests/
```

Manual connection test:

```bash
./scripts/test_connection.sh
```

## Troubleshooting

### WiFi Aware Not Available

```bash
# Check kernel modules
lsmod | grep cfg80211
lsmod | grep brcmfmac

# Reload WiFi module
sudo modprobe -r brcmfmac
sudo modprobe brcmfmac
```

### wpa_supplicant Issues

```bash
# Kill existing instances
sudo killall wpa_supplicant

# Start with debug logging
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -dd
```

### Permission Issues

```bash
# Add user to netdev group
sudo usermod -aG netdev $USER

# Log out and back in for changes to take effect
```

## Current State

🚧 **Entry point created, core implementation pending**

**Implemented:**

- Project structure with virtual environment support
- Entry point (`main.py`) with logging and signal handling
- Configuration structure (`config/settings.yaml`)
- Dependency management (`requirements.txt`)
- Basic startup script (`scripts/start_service.sh`)

**Pending:**

- WiFi Aware manager implementation
- Service publisher
- Discovery handler
- Data path establishment
- Message protocol implementation

## Resources

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [wpa_supplicant Documentation](https://w1.fi/wpa_supplicant/)
- [Architecture Documentation](../docs/architecture.md)

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
