# WiFi Aware Investigation

A proof-of-concept repository demonstrating WiFi Aware functionality across Android and iOS platforms, using a Raspberry Pi as a control device.

## Overview

WiFi Aware (also known as Wi-Fi Neighbor Awareness Networking or NAN) is a technology that enables devices to discover services in their proximity without requiring an internet connection or traditional WiFi access point. This repository contains three interconnected projects to test and validate WiFi Aware capabilities:

- **Raspberry Pi**: Control device that coordinates WiFi Aware sessions
- **Android**: Native Android app implementing WiFi Aware APIs
- **iOS**: Native iOS app implementing WiFi Aware framework

## What is WiFi Aware?

WiFi Aware allows devices to:

- Discover other devices and services nearby
- Establish peer-to-peer connections without internet
- Communicate with ultra-low latency
- Conserve battery through efficient discovery mechanisms

### Key Resources

- [Android WiFi Aware Documentation](https://developer.android.com/develop/connectivity/wifi/wifi-aware)
- [Apple WiFi Aware Framework](https://developer.apple.com/documentation/WiFiAware)

## Repository Structure

```plaintext
wifi_aware_investigation/
├── docs/               # Cross-platform documentation
│   └── architecture.md # Message protocol and system architecture
├── rpi/               # Raspberry Pi control device
├── android/           # Android WiFi Aware app
├── ios/               # iOS WiFi Aware app
└── README.md
```

## Getting Started

Each platform has its own README with build and run instructions:

1. **[Raspberry Pi](rpi/README.md)** - Setup RPi as the WiFi Aware publisher
2. **[Android](android/README.md)** - Build and run the Android subscriber app
3. **[iOS](ios/README.md)** - Build and run the iOS subscriber app

For the cross-platform message protocol and architecture, see [Architecture Documentation](docs/architecture.md).

## Prerequisites

- Raspberry Pi (RPi 4 or newer recommended) with WiFi Aware capable hardware
- Android device running Android 8.0+ (API level 26+) with WiFi Aware support
- iOS device running iOS 18.0+ with WiFi Aware support
- Development environments:
  - Python 3.8+ (for RPi)
  - Android Studio (for Android)
  - Xcode 16.0+ (for iOS)

## Project Status

🚧 **This is a proof-of-concept repository under active development**

### POC Proof Plan

The following phased approach will validate WiFi Aware functionality across platforms:

#### Phase 1: RPi Discovery Validation

Prove the Raspberry Pi can be discovered using the existing [WiFi NAN Scan Android app](https://play.google.com/store/apps/details?id=com.google.android.apps.location.rtt.wifinanscan&hl=en_US) from the Google Play Store. This validates our RPi publisher implementation before investing in custom client development.

**Success criteria**: WiFi NAN Scan app successfully discovers the RPi's published service and displays connection information.

#### Phase 2: Custom Android Implementation

Implement our custom Android project to replace the WiFi NAN Scan app, proving our Android implementation can discover and communicate with the RPi.

**Success criteria**: Our Android app discovers the RPi service and exchanges JSON-formatted messages per the protocol defined in `docs/architecture.md`.

#### Phase 3: iOS Implementation

Implement our iOS project to replace the Android project in the test setup, proving our iOS implementation works independently.

**Success criteria**: Our iOS app discovers the RPi service and exchanges JSON-formatted messages per the protocol defined in `docs/architecture.md`.

#### Phase 4: Multi-Platform Integration

Test our Android and iOS projects together, both connecting to the RPi simultaneously to validate concurrent multi-platform communication.

**Success criteria**: Both Android and iOS apps can discover the RPi and communicate with it at the same time without interference, demonstrating full cross-platform WiFi Aware capability.

## License

See [LICENSE](LICENSE) for details.
POC Android and iOS WifiAware
