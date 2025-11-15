# iOS WiFi Aware App

iOS application demonstrating WiFi Aware functionality for the WiFi Aware investigation project.

## Overview

This iOS app discovers and connects to the Raspberry Pi WiFi Aware service, enabling peer-to-peer communication without requiring internet or a traditional WiFi access point.

## Prerequisites

### Hardware

- iPhone 15 Pro or later, OR iPad with M1 chip or later
- iOS 18.0+ required
- **Physical device required** - WiFi Aware does not work on simulator

### Software

- macOS Ventura or later
- Xcode 16.0 or later
- Active Apple Developer account

## Device Compatibility

WiFi Aware is a new framework introduced in iOS 18.0 with specific hardware requirements:

**Compatible devices:**

- iPhone 15 Pro and later
- iPad models with M1 chip or later

**Requires:**

- iOS 18.0+
- WiFi Aware entitlement from Apple Developer Support

## Building the App

### Open in Xcode

```bash
cd wifi_aware_investigation/ios
open WiFiAwareApp.xcodeproj
```

### Configure Signing

1. Open project in Xcode
2. Select the WiFiAwareApp target
3. Go to "Signing & Capabilities"
4. Select your development team
5. Ensure "Access WiFi Information" capability is added

### Build and Run

1. Connect your iOS 18+ device via USB
2. Select your device as the target (not simulator)
3. Click Run (⌘R)
4. App will install and launch on your device

### Command Line Build

```bash
xcodebuild -project WiFiAwareApp.xcodeproj \
    -scheme WiFiAwareApp \
    -destination 'platform=iOS,name=Your iPhone' \
    build
```

## Running the App

### WiFi Aware Entitlement

⚠️ **Important**: WiFi Aware requires a special entitlement that must be requested from Apple Developer Support:

```xml
<key>com.apple.developer.networking.wifi-aware</key>
<true/>
```

Without this entitlement, WiFi Aware APIs will not function.

### First Launch

The app uses local network and WiFi, configured in `Info.plist`:

```xml
<key>NSLocalNetworkUsageDescription</key>
<string>This app uses WiFi Aware to discover and communicate with nearby devices.</string>
```

### What It Does

The app automatically:

- Checks for WiFi Aware availability on device
- Subscribes to the "rpi_control_service"
- Establishes data path when RPi is discovered
- Exchanges JSON messages per the protocol in `../docs/architecture.md`

## Project Structure

```plaintext
WiFiAwareApp/
├── App/
│   ├── WiFiAwareAppApp.swift       # App entry point
│   └── ContentView.swift           # Main view
├── Info.plist
└── WiFiAwareApp.entitlements       # Includes WiFi Aware entitlement
```

## Current State

🚧 **Basic skeleton implemented**

**Implemented:**

- Xcode project structure
- Basic SwiftUI app entry point
- WiFi Aware entitlement configured
- Info.plist with required descriptions

**Pending:**

- WiFi Aware framework integration
- Service discovery implementation
- Data path establishment
- Message protocol handling
- SwiftUI views for discovery and messaging

**Important:** Must test on physical iOS 18+ device. Simulator will not work.

## Testing

Run unit tests (when implemented):

```bash
xcodebuild test -project WiFiAwareApp.xcodeproj \
    -scheme WiFiAwareApp \
    -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

Manual testing checklist:

1. Ensure RPi service is running
2. Launch app on iOS device
3. Verify WiFi Aware availability check
4. Monitor discovery and connection status
5. Test message exchange

## Debugging

View logs in Xcode Console with filter:

```plaintext
subsystem:com.gopro.wifiaware
```

Common issues:

- **"WiFi Aware not available"**: Verify iOS 18+ and compatible hardware
- **Entitlement error**: Request WiFi Aware entitlement from Apple
- **Cannot build to device**: Check provisioning profile and signing

## Technology Stack

- Swift 5.9+
- SwiftUI
- WiFi Aware framework
- Network framework
- MVVM architecture

WiFi Aware does not work in the iOS Simulator. You must test on a physical device with iOS 18.0+ that supports WiFi Aware.

## Resources

- [Apple WiFi Aware Framework Documentation](https://developer.apple.com/documentation/WiFiAware)
- [Network Framework Guide](https://developer.apple.com/documentation/network)
- [Architecture Documentation](../docs/architecture.md)
