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
├── docs/               # Detailed documentation
│   ├── architecture.md
│   ├── android-setup.md
│   ├── ios-setup.md
│   └── rpi-setup.md
├── rpi/               # Raspberry Pi control device
├── android/           # Android WiFi Aware app
├── ios/               # iOS WiFi Aware app
└── README.md
```

## Getting Started

Each platform has specific requirements and setup steps. Please refer to the documentation in the `docs/` folder:

1. **[Raspberry Pi Setup](docs/rpi-setup.md)** - Configure your RPi as the control device
2. **[Android Setup](docs/android-setup.md)** - Build and run the Android app
3. **[iOS Setup](docs/ios-setup.md)** - Build and run the iOS app

For an overview of the system architecture and how the components interact, see [Architecture Documentation](docs/architecture.md).

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

## License

See [LICENSE](LICENSE) for details.
POC Android and iOS WifiAware
