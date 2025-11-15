# Raspberry Pi WiFi Aware - Setup Guide

## Prerequisites

### Hardware Requirements

- Raspberry Pi 4 Model B or newer (recommended)
- WiFi adapter with WiFi Aware (NAN) support
  - **Recommended**: Internal WiFi on RPi 4 (Broadcom BCM43455)
  - **Alternative**: External USB WiFi adapter with NAN support
- MicroSD card (16GB+ recommended)
- Power supply (USB-C, 5V/3A for RPi 4)

### Supported WiFi Chipsets

WiFi Aware requires specific hardware support. Known compatible chipsets:

- Broadcom BCM43455 (RPi 4 built-in)
- Broadcom BCM4339
- Qualcomm QCA6174
- Intel Wireless 8260/8265 (requires USB adapter)

### Software Requirements

- Raspberry Pi OS (64-bit recommended, Bookworm or newer)
- Python 3.8 or higher
- wpa_supplicant with NAN support (version 2.10+)
- NetworkManager with WiFi Aware support

## Initial Setup

### 1. Flash Raspberry Pi OS

Download and flash Raspberry Pi OS:

```bash
# Use Raspberry Pi Imager or manual flash
# https://www.raspberrypi.com/software/

# After flashing, enable SSH by creating an empty file:
touch /boot/ssh
```

### 2. Boot and Update System

```bash
# SSH into your RPi
ssh pi@raspberrypi.local

# Update system
sudo apt update
sudo apt upgrade -y
```

### 3. Check WiFi Hardware

Verify WiFi adapter is detected:

```bash
# Check wireless interface
ip link show

# Should see wlan0 or similar
# Output: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...

# Check WiFi chip info
lsusb  # For USB adapters
iw list | grep -A 10 "Supported interface modes"
```

## Install WiFi Aware Dependencies

### 1. Install Required Packages

```bash
sudo apt install -y \
    wpasupplicant \
    network-manager \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    build-essential \
    iw
```

### 2. Verify wpa_supplicant Version

WiFi Aware requires wpa_supplicant 2.10+:

```bash
wpa_supplicant -v

# Should show version 2.10 or higher
# If not, you may need to compile from source
```

### 3. Install wpa_supplicant with NAN Support (if needed)

If your version doesn't support NAN:

```bash
# Install build dependencies
sudo apt install -y \
    libnl-3-dev \
    libnl-genl-3-dev \
    libssl-dev \
    libdbus-1-dev

# Clone wpa_supplicant
git clone git://w1.fi/srv/git/hostap.git
cd hostap/wpa_supplicant

# Configure build
cp defconfig .config
echo "CONFIG_WIFI_DISPLAY=y" >> .config
echo "CONFIG_WNM=y" >> .config
echo "CONFIG_INTERWORKING=y" >> .config

# Build
make -j4

# Install
sudo make install
```

## Configure NetworkManager

### 1. Stop and Disable dhcpcd

```bash
sudo systemctl stop dhcpcd
sudo systemctl disable dhcpcd
```

### 2. Enable NetworkManager

```bash
sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager
```

### 3. Configure WiFi Interface

Edit `/etc/NetworkManager/NetworkManager.conf`:

```ini
[main]
plugins=ifupdown,keyfile

[ifupdown]
managed=true

[device]
wifi.scan-rand-mac-address=no
```

Restart NetworkManager:

```bash
sudo systemctl restart NetworkManager
```

## Python Environment Setup

### 1. Navigate to Project Directory

```bash
cd /home/pi/wifi_aware_investigation/rpi
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

Example `requirements.txt`:

```plaintext
pyroute2==0.7.9
python-networkmanager==2.2
asyncio==3.4.3
aiohttp==3.9.1
```

## WiFi Aware Configuration

### 1. Enable WiFi Aware in wpa_supplicant

Create `/etc/wpa_supplicant/wpa_supplicant-nan.conf`:

```plaintext
ctrl_interface=/var/run/wpa_supplicant
update_config=1
country=US

# Enable WiFi Aware
nan_enable=1
```

### 2. Test WiFi Aware Capability

```bash
# Check if NAN is supported
iw list | grep -i "nan"

# Should see:
#   * nan
#   in the supported interface modes
```

### 3. Start WiFi Aware Session (Manual Test)

```bash
# Stop NetworkManager temporarily
sudo systemctl stop NetworkManager

# Start wpa_supplicant with NAN support
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant-nan.conf -B

# Check status
sudo wpa_cli -i wlan0 status

# Start NetworkManager again
sudo systemctl start NetworkManager
```

## Project Structure

```plaintext
rpi/
├── src/
│   ├── __init__.py
│   ├── wifi_aware_manager.py    # Main WiFi Aware controller
│   ├── publisher.py              # Service publisher
│   ├── discovery.py              # Device discovery handler
│   ├── data_path.py              # Data exchange handler
│   └── protocol.py               # Message protocol
├── tests/
│   ├── test_publisher.py
│   └── test_discovery.py
├── config/
│   ├── settings.yaml             # Configuration
│   └── logging.yaml              # Logging config
├── scripts/
│   ├── start_service.sh          # Service startup script
│   └── test_connection.sh        # Connection test
├── requirements.txt
├── README.md
└── main.py                       # Entry point
```

## Running the WiFi Aware Service

### 1. Configure Settings

Edit `config/settings.yaml`:

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

### 2. Start the Service

```bash
# Activate virtual environment
source venv/bin/activate

# Run main script
sudo python3 main.py
```

Or using systemd service:

```bash
# Copy service file
sudo cp scripts/wifi-aware.service /etc/systemd/system/

# Enable and start
sudo systemctl enable wifi-aware
sudo systemctl start wifi-aware

# Check status
sudo systemctl status wifi-aware
```

### 3. Monitor Logs

```bash
# Follow service logs
sudo journalctl -u wifi-aware -f

# Or check log file
tail -f /var/log/wifi_aware.log
```

## Testing

### Basic Connection Test

```bash
# Run test script
./scripts/test_connection.sh
```

### Python Interactive Test

```python
from src.wifi_aware_manager import WiFiAwareManager

manager = WiFiAwareManager()
manager.start_publisher(service_name="rpi_control_service")

# Check for subscribers
manager.get_active_subscribers()
```

### Manual Testing Checklist

- [ ] WiFi interface is up and detected
- [ ] wpa_supplicant supports NAN
- [ ] NetworkManager is running
- [ ] Service publishes successfully
- [ ] Android/iOS devices can discover service
- [ ] Data path establishes
- [ ] Messages exchange correctly
- [ ] Service survives disconnect/reconnect
- [ ] Logs capture all events

## Troubleshooting

### WiFi Aware Not Available

```bash
# Check kernel modules
lsmod | grep cfg80211
lsmod | grep brcmfmac  # For RPi built-in WiFi

# Reload modules
sudo modprobe -r brcmfmac
sudo modprobe brcmfmac
```

### wpa_supplicant Issues

```bash
# Kill existing instances
sudo killall wpa_supplicant

# Start with debug logging
sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant-nan.conf -dd

# Check for NAN-related messages in output
```

### NetworkManager Conflicts

```bash
# Check if NetworkManager is managing WiFi
nmcli device status

# Verify wlan0 is managed
# If not, edit /etc/NetworkManager/NetworkManager.conf
```

### Permission Issues

```bash
# Ensure user is in netdev group
sudo usermod -aG netdev $USER

# Reboot or re-login for group changes to take effect
```

### Discovery Not Working

1. Verify WiFi channel compatibility
2. Check that devices are within range (~30m)
3. Ensure no WiFi channel conflicts
4. Verify service name matches on all devices
5. Check firewall rules (if enabled)

## Performance Tuning

### Optimize WiFi Power Management

```bash
# Disable WiFi power saving
sudo iwconfig wlan0 power off

# Make permanent: add to /etc/rc.local
echo "iwconfig wlan0 power off" | sudo tee -a /etc/rc.local
```

### Adjust CPU Governor

```bash
# Set to performance mode
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

## Security Considerations

- Use encrypted data paths when possible
- Implement application-level encryption
- Validate all incoming messages
- Use passphrase-protected services for sensitive applications
- Keep system and packages updated
- Limit physical access to device

## Automation & Service Management

### Systemd Service Example

Create `/etc/systemd/system/wifi-aware.service`:

```ini
[Unit]
Description=WiFi Aware Control Service
After=network.target NetworkManager.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/wifi_aware_investigation/rpi
ExecStart=/home/pi/wifi_aware_investigation/rpi/venv/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Auto-start on Boot

```bash
sudo systemctl enable wifi-aware
```

## Monitoring & Maintenance

### Check System Resources

```bash
# CPU and memory
htop

# WiFi statistics
iw wlan0 station dump
```

### Log Rotation

Configure in `/etc/logrotate.d/wifi-aware`:

```plaintext
/var/log/wifi_aware.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 pi pi
}
```

## Resources

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [wpa_supplicant Documentation](https://w1.fi/wpa_supplicant/)
- [NetworkManager Documentation](https://networkmanager.dev/)
- [WiFi Aware Linux Implementation](https://www.kernel.org/doc/html/latest/networking/mac80211.html)

## Next Steps

Once the RPi is configured:

1. Start the WiFi Aware service
2. Use Android app to discover and connect ([android-setup.md](android-setup.md))
3. Use iOS app to discover and connect ([ios-setup.md](ios-setup.md))
4. Monitor logs and test message exchange
5. Document findings and performance metrics

For general architecture, see [architecture.md](architecture.md).
