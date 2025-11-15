# iOS WiFi Aware App

iOS application demonstrating WiFi Aware functionality for the WiFi Aware investigation project.

## Overview

This iOS app discovers and connects to the Raspberry Pi WiFi Aware service, enabling peer-to-peer communication without requiring internet or a traditional WiFi access point.

## Prerequisites

- iPhone or iPad with WiFi Aware support (iOS 18.0+)
- Physical device required (WiFi Aware does not work on simulator)
- macOS Ventura or later
- Xcode 16.0 or later
- See [docs/ios-setup.md](../docs/ios-setup.md) for complete setup instructions

## Device Compatibility

WiFi Aware is available on:

- iPhone 15 Pro and later
- iPad models with M1 chip or later
- Requires iOS 18.0+

**Note**: This is a new framework introduced in iOS 18.

## Quick Start

### Open in Xcode

```bash
cd wifi_aware_investigation/ios
open WiFiAwareApp.xcodeproj
```

### Build and Run

1. Open project in Xcode
2. Select your development team in Signing & Capabilities
3. Connect your iOS device (simulator won't work)
4. Select your device as the target
5. Click Run (⌘ + R)

## Project Structure

```plaintext
ios/
├── WiFiAwareApp/
│   ├── App/
│   │   ├── WiFiAwareAppApp.swift
│   │   └── ContentView.swift
│   ├── Views/
│   │   ├── DiscoveryView.swift
│   │   ├── MessageView.swift
│   │   └── Components/
│   ├── ViewModels/
│   │   ├── WiFiAwareViewModel.swift
│   │   └── MessageViewModel.swift
│   ├── Services/
│   │   ├── WiFiAwareManager.swift
│   │   ├── DiscoveryService.swift
│   │   └── DataPathService.swift
│   ├── Models/
│   │   ├── Message.swift
│   │   ├── DeviceInfo.swift
│   │   └── ConnectionState.swift
│   └── Utils/
│       ├── Logger.swift
│       └── Constants.swift
├── WiFiAwareApp.xcodeproj
└── README.md
```

## Key Features

- WiFi Aware service discovery
- Peer-to-peer data path establishment
- Real-time message exchange
- Connection state monitoring
- SwiftUI interface

## Required Capabilities

The app requires:

- WiFi Aware entitlement (request from Apple Developer)
- Access WiFi Information capability
- Local Network usage description

## Configuration

Edit `Info.plist` to include:

```xml
<key>NSLocalNetworkUsageDescription</key>
<string>This app uses WiFi Aware to discover and communicate with nearby devices.</string>
```

## Current State

🚧 **Basic skeleton implemented**

**Implemented:**

- Xcode project structure
- Basic SwiftUI app entry point (`WiFiAwareAppApp.swift`)
- Placeholder UI view (`ContentView.swift`)
- WiFi Aware entitlement configured
- Info.plist with required descriptions

**Pending:**

- WiFi Aware framework integration
- Service discovery implementation
- Data path establishment
- Message protocol handling
- SwiftUI views for discovery and messaging
- View models and service layer
- Connection state management

**Important:** Must test on physical iOS 18+ device with WiFi Aware support (iPhone 15 Pro+ or M1+ iPad). Simulator will not work.

## Testing

### Build for Device

WiFi Aware only works on physical devices:

```bash
xcodebuild -project WiFiAwareApp.xcodeproj \
    -scheme WiFiAwareApp \
    -destination 'platform=iOS,name=Your iPhone' \
    build
```

### Manual Testing

1. Ensure RPi service is running
2. Launch app on iOS device
3. Tap "Start Discovery"
4. Monitor connection status
5. Test message exchange

## Debugging

View logs in Xcode Console:

```plaintext
subsystem:com.gopro.wifiaware
```

Or use Instruments for detailed profiling.

## Documentation

For detailed setup, implementation, and troubleshooting:

- [iOS Setup Guide](../docs/ios-setup.md)
- [Architecture Documentation](../docs/architecture.md)


## Technology Stack

- Swift 5.9+
- SwiftUI
- WiFi Aware framework
- Combine
- Network framework
- MVVM architecture

## Important Notes

### WiFi Aware Entitlement

The WiFi Aware framework requires a special entitlement from Apple:

```xml
<key>com.apple.developer.networking.wifi-aware</key>
<true/>
```

You must request this entitlement through Apple Developer Support before you can use WiFi Aware in your app.

### Simulator Limitation

WiFi Aware does not work in the iOS Simulator. You must test on a physical device with iOS 18.0+ that supports WiFi Aware.

## Resources

- [Apple WiFi Aware Framework Documentation](https://developer.apple.com/documentation/WiFiAware)
- [Network Framework Guide](https://developer.apple.com/documentation/network)
- [WWDC WiFi Aware Sessions](https://developer.apple.com/videos/)
