# WiFi Aware Investigation - Architecture

## System Overview

This proof-of-concept demonstrates WiFi Aware (NAN - Neighbor Awareness Networking) functionality across multiple platforms using a coordinated architecture.

## Component Architecture

```plaintext
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Android App   │         │  Raspberry Pi   │         │    iOS App      │
│                 │         │   (Control)     │         │                 │
│  WiFi Aware API │◄───────►│  WiFi Aware     │◄───────►│ WiFi Aware      │
│                 │         │  Coordinator    │         │ Framework       │
└─────────────────┘         └─────────────────┘         └─────────────────┘
        │                            │                            │
        └────────────────────────────┴────────────────────────────┘
                          WiFi Aware Network
                         (Peer-to-Peer Discovery)
```

## WiFi Aware Workflow

### 1. Service Discovery Phase

- **Publisher**: RPi advertises a service using WiFi Aware
- **Subscribers**: Android and iOS devices discover the advertised service
- **Handshake**: Devices exchange discovery messages

### 2. Connection Establishment

- Devices use WiFi Aware data path to establish direct communication
- No internet or traditional WiFi AP required
- Ultra-low latency peer-to-peer connection

### 3. Data Exchange

- Bi-directional communication between devices
- Message passing for control and telemetry
- Real-time status updates

## Platform Responsibilities

### Raspberry Pi (Control Device)

**Role**: Service Publisher & Coordinator

- Initializes WiFi Aware sessions
- Publishes discoverable service
- Manages connection lifecycle
- Coordinates test scenarios
- Logs all interactions

**Key Technologies**:

- Python 3.8+
- Linux WiFi Aware stack (wpa_supplicant)
- Network Manager with WiFi Aware support

### Android Application

**Role**: Service Subscriber & Client

- Discovers RPi published service
- Subscribes to WiFi Aware sessions
- Establishes data path
- Sends/receives messages
- UI for monitoring connection state

**Key Technologies**:

- Android 8.0+ (API 26+)
- `android.net.wifi.aware` package
- Kotlin/Java
- Jetpack Compose (UI)

### iOS Application

**Role**: Service Subscriber & Client

- Discovers RPi published service
- Subscribes to WiFi Aware sessions
- Establishes data path
- Sends/receives messages
- UI for monitoring connection state

**Key Technologies**:

- iOS 18.0+
- `WiFiAware` framework
- Swift
- SwiftUI

## Communication Protocol

### Discovery Message Format

```json
{
  "type": "discovery",
  "device_id": "unique-identifier",
  "platform": "android|ios|rpi",
  "timestamp": "ISO-8601",
  "capabilities": []
}
```

### Data Message Format

```json
{
  "type": "data",
  "sender": "device-id",
  "sequence": 123,
  "payload": {
    "command": "ping|status|test",
    "data": {}
  },
  "timestamp": "ISO-8601"
}
```

## Test Scenarios

### Scenario 1: Basic Discovery

- RPi publishes service
- Android/iOS discover and connect
- Verify discovery latency

### Scenario 2: Message Exchange

- Establish data paths
- Exchange messages
- Measure throughput and latency

### Scenario 3: Connection Resilience

- Test connection stability
- Handle disconnections
- Automatic reconnection

### Scenario 4: Multi-Device

- Multiple subscribers simultaneously
- Broadcast vs unicast messages
- Resource management

## Security Considerations

- WiFi Aware supports encrypted data paths
- Service discovery can be open or passphrase-protected
- Implement application-level encryption for sensitive data
- Validate all incoming messages

## Performance Metrics

Metrics to collect during POC:

- **Discovery Time**: Time from service publish to discovery
- **Connection Time**: Time to establish data path
- **Latency**: Round-trip time for messages
- **Throughput**: Data transfer rates
- **Range**: Effective distance for reliable communication
- **Battery Impact**: Power consumption during active sessions

## Limitations & Known Issues

- WiFi Aware hardware support varies by device
- iOS support limited to iOS 18.0+
- RPi requires specific WiFi chipset with NAN support
- Not all Android devices support WiFi Aware (hardware dependent)

## Future Enhancements

- Group messaging support
- File transfer capabilities
- Location-based service filtering
- Integration with other proximity technologies (BLE, UWB)

## References

- [WiFi Alliance - Wi-Fi Aware](https://www.wi-fi.org/discover-wi-fi/wi-fi-aware)
- [Android WiFi Aware Developer Guide](https://developer.android.com/develop/connectivity/wifi/wifi-aware)
- [Apple WiFi Aware Framework Documentation](https://developer.apple.com/documentation/WiFiAware)
