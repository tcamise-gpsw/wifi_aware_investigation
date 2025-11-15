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
- Xcode 16.0 or later (with iOS SDK 18.0+)
- Active Apple Developer account

⚠️ **Framework Availability Note**: As of November 2025, the WiFiAware framework is not yet available in the standard Xcode SDK (tested with iOS SDK 18.5). The project currently uses stub implementations to allow compilation. Once Apple releases the framework (likely requiring entitlement approval), the stubs can be replaced with `import WiFiAware`.

## Device Compatibility

⚠️ **Hardware Requirements Under Investigation**

WiFi Aware is a new framework introduced in [iOS 18.0](https://developer.apple.com/documentation/wifiaware) with specific hardware requirements. Apple has not published an official list of compatible devices.

**Likely compatible devices (unverified):**

- iPhone 15 Pro and later (WiFi 6E chipset)
- iPad models with M1 chip or later (WiFi 6E support)

**Confirmed requirements:**

- iOS 18.0+ (see [WiFi Aware Framework Documentation](https://developer.apple.com/documentation/wifiaware))
- WiFi Aware entitlement from Apple Developer Support
- Physical device with WiFi 6E hardware (802.11ax with NAN support)

### Runtime Capability Check

The app includes early runtime capability checking that executes at app launch. Use the provided utility to check WiFi Aware support:

```swift
// Capability check runs automatically at app launch via AppState
let capability = WIFIAwareCapabilityCheck()
let result = capability.checkSupport()

switch result {
case .supported:
    print("✓ WiFi Aware is available")
case .notSupported(let reason):
    print("✗ Not available: \(reason)")
}
```

See [`WiFiAwareApp/WIFIAwareCapabilityCheck.swift`](WiFiAwareApp/WiFiAwareApp/WIFIAwareCapabilityCheck.swift) for the implementation. When the real framework is available, it will use Apple's official `WIFIAwarePublisher.isSupported` and `WIFIAwareSubscriber.isSupported` properties.

**Current Implementation**: Uses stub types that return `false` until the real framework is released. The app displays an alert and disables WiFi Aware features when not supported.

**References:**

- [WiFi Aware Framework Documentation](https://developer.apple.com/documentation/wifiaware)
- [WIFIAwarePublisher.isSupported](https://developer.apple.com/documentation/wifiaware/wifiawarepublisher/issupported)
- [WIFIAwareSubscriber.isSupported](https://developer.apple.com/documentation/wifiaware/wifiawaresubscriber/issupported)

**Note:** The specific device compatibility list above is based on WiFi 6E hardware availability and has not been officially confirmed by Apple. The runtime check is the authoritative way to determine support.

## Building the App

### Initial Setup (First Time Only)

The project structure is already set up. If starting fresh:

1. The Xcode project is located at `WiFiAwareApp/WiFiAwareApp.xcodeproj`
2. All source files are in `WiFiAwareApp/WiFiAwareApp/`
3. No external dependencies (CocoaPods/SPM) required

### Open in Xcode

```bash
cd wifi_aware_investigation/ios
open WiFiAwareApp/WiFiAwareApp.xcodeproj
```

### Configure Signing

1. Open project in Xcode
2. Select the WiFiAwareApp target
3. Go to "Signing & Capabilities"
4. Select your development team
5. Xcode will automatically manage signing

### Build and Run

**Simulator (for UI testing only):**

1. Select any iOS Simulator as target
2. Click Run (⌘R)
3. Note: WiFi Aware will show as "Not Supported" (expected behavior)

**Physical Device (required for WiFi Aware):**

1. Connect your iOS 18+ device via USB
2. Select your device as the target
3. Click Run (⌘R)
4. App will install and launch on your device

### Command Line Build

```bash
cd wifi_aware_investigation/ios
# For simulator
xcodebuild -project WiFiAwareApp/WiFiAwareApp.xcodeproj \
    -scheme WiFiAwareApp \
    -sdk iphonesimulator \
    build

# For device (requires provisioning)
xcodebuild -project WiFiAwareApp/WiFiAwareApp.xcodeproj \
    -scheme WiFiAwareApp \
    -sdk iphoneos \
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
├── WiFiAwareApp.xcodeproj/         # Xcode project file
├── WiFiAwareApp/                    # Main app target
│   ├── WiFiAwareAppApp.swift       # App entry point with early capability check
│   ├── ContentView.swift           # Main view with support status display
│   ├── WIFIAwareCapabilityCheck.swift  # Runtime capability check utility
│   ├── WiFiAwareApp.entitlements   # Includes WiFi Aware entitlement (when available)
│   └── Assets.xcassets/            # App assets
├── WiFiAwareAppTests/              # Unit tests (empty)
└── WiFiAwareAppUITests/            # UI tests (empty)
```

## Current State

✅ **Project builds successfully**

**Implemented:**

- Xcode project structure with all source files
- SwiftUI app with early WiFi Aware capability checking at launch
- `AppState` manager that checks support immediately when app starts
- UI displays support status with visual indicators
- Alert shown if WiFi Aware is not supported with detailed reason
- Discovery button disabled when WiFi Aware unavailable
- WiFi Aware entitlement configured in entitlements file
- Stub WiFiAware framework types (until real framework is released)

**Pending:**

- Replace stubs with real `import WiFiAware` when framework becomes available
- Request WiFi Aware entitlement from Apple Developer Support
- Service discovery implementation using `WIFIAwareSubscriber`
- Data path establishment using `WIFIAwareDataSession`
- Message protocol handling (JSON exchange per `../docs/architecture.md`)
- SwiftUI views for discovery details and messaging

**Build Status**: ✅ Compiles and runs on simulator and device (shows "Not Supported" until real framework available)

**Important:** WiFi Aware functionality requires:

1. Real WiFiAware framework from Apple (not yet available in SDK)
2. Special entitlement approval from Apple Developer Support
3. Physical iOS 18+ device with WiFi 6E hardware for testing

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

- [Apple WiFi Aware Framework Documentation](https://developer.apple.com/documentation/wifiaware)
- [Network Framework Guide](https://developer.apple.com/documentation/network)
- [WiFi Alliance - WiFi Aware Overview](https://www.wi-fi.org/discover-wi-fi/wi-fi-aware)
- [IEEE 802.11 NAN Specification](https://standards.ieee.org/ieee/802.11/7028/)
- [Architecture Documentation](../docs/architecture.md)
