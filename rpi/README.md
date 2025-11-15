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
- Python 3.9+
- wpa_supplicant 2.10+ with NAN support
- NetworkManager
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

For complete setup details, see [docs/rpi-setup.md](../docs/rpi-setup.md)

## System Setup

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install System Dependencies

```bash
# Core system packages
sudo apt install -y \
    wpasupplicant \
    network-manager \
    iw \
    git

# Development libraries (required for Python dependencies)
sudo apt install -y \
    libdbus-1-dev \
    libglib2.0-dev
```

**Note**: The `libdbus-1-dev` and `libglib2.0-dev` packages are required to build the `dbus-python` dependency used by `python-networkmanager`.

### 3. Verify WiFi Aware Support

⚠️ **Hardware Support Investigation Required**

WiFi Aware (NAN - Neighbor Awareness Networking) support requires both hardware and software capabilities. Use the provided verification script to check your system:

```bash
# Check NAN support on default interface (wlan0)
uv run python scripts/check_nan_support.py

# Check specific interface
uv run python scripts/check_nan_support.py wlan1
```

This script uses the **pyroute2** library to query the Linux kernel's nl80211 netlink API, checking if the driver reports the `NL80211_IFTYPE_NAN` interface type. See [`scripts/check_nan_support.py`](scripts/check_nan_support.py) for the implementation.

**References:**

- [pyroute2 Documentation](https://pyroute2.org/) - Python netlink interface
- [Linux nl80211 API](https://www.kernel.org/doc/html/latest/userspace-api/netlink/intro.html) - Kernel wireless subsystem API
- [nl80211.h Interface Types](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/uapi/linux/nl80211.h) - Official kernel header defining `NL80211_IFTYPE_NAN`

**Hardware Notes:**

- Raspberry Pi 4 uses Broadcom BCM43455 WiFi chip ([RPi 4 Specifications](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/))
- NAN support in BCM43455 requires verification through testing
- Linux kernel 4.9+ includes [cfg80211 NAN infrastructure](https://www.kernel.org/doc/html/latest/networking/mac80211.html)
- Driver support depends on brcmfmac module with NAN compiled in
- wpa_supplicant 2.10+ required for NAN operations ([ChangeLog](https://w1.fi/cgit/hostap/plain/wpa_supplicant/ChangeLog))

**Alternative:** If built-in WiFi doesn't support NAN, consider USB WiFi adapters with confirmed 802.11 NAN support.

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

### 2. Install Dependencies with uv

```bash
# Install dependencies (uv automatically creates a virtual environment)
uv sync
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
# Run with sudo (required for WiFi operations)
sudo uv run python main.py
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
├── pyproject.toml                # Python dependencies
└── main.py                       # Entry point
```

## Testing

Run Python tests:

```bash
uv run pytest tests/
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
- [Raspberry Pi 4 Specifications](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)
- [wpa_supplicant Documentation](https://w1.fi/wpa_supplicant/)
- [wpa_supplicant ChangeLog (NAN support)](https://w1.fi/cgit/hostap/plain/wpa_supplicant/ChangeLog)
- [Linux Wireless Wiki - NAN](https://wireless.wiki.kernel.org/en/users/documentation/nan)
- [WiFi Alliance - WiFi Aware Overview](https://www.wi-fi.org/discover-wi-fi/wi-fi-aware)
- [cfg80211 MAC80211 Documentation](https://www.kernel.org/doc/html/latest/networking/mac80211.html)
- [Architecture Documentation](../docs/architecture.md)
