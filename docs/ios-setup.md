# iOS WiFi Aware App - Setup Guide

## Prerequisites

### Hardware Requirements

- iPhone or iPad with WiFi Aware support
- iOS 18.0 or later (WiFi Aware framework introduced in iOS 18)
- Physical device required (WiFi Aware does not work on simulator)

### Software Requirements

- macOS Ventura or later
- Xcode 16.0 or later
- Swift 5.9+
- CocoaPods or Swift Package Manager (optional, for dependencies)

## Checking Device Compatibility

WiFi Aware is available on:

- iPhone 15 Pro and later
- iPad models with M1 chip or later
- Requires iOS 18.0+

Verify availability in code:

```swift
import WiFiAware

let session = WiFiAwareSession()
if session.isAvailable {
    print("WiFi Aware is available")
} else {
    print("WiFi Aware is not available on this device")
}
```

## Project Setup

### 1. Open Xcode Project

```bash
cd wifi_aware_investigation/ios
open WiFiAwareApp.xcodeproj
```

Or if using CocoaPods:

```bash
cd ios
pod install
open WiFiAwareApp.xcworkspace
```

### 2. Required Capabilities

Add the following to your `Info.plist`:

```xml
<key>NSLocalNetworkUsageDescription</key>
<string>This app uses WiFi Aware to discover and communicate with nearby devices.</string>

<key>NSBonjourServices</key>
<array>
    <string>_wifiaware._tcp</string>
</array>
```

Enable WiFi capability in Xcode:

1. Select your project in the navigator
2. Select your target
3. Go to "Signing & Capabilities"
4. Click "+ Capability"
5. Add "Access WiFi Information"

### 3. Entitlements

Ensure your app has the WiFi Aware entitlement. In your `.entitlements` file:

```xml
<key>com.apple.developer.networking.wifi-aware</key>
<true/>
```

You may need to request this entitlement from Apple Developer Support.

### 4. Project Structure

```plaintext
WiFiAwareApp/
├── App/
│   ├── WiFiAwareAppApp.swift       # App entry point
│   └── ContentView.swift           # Main view
├── Views/
│   ├── DiscoveryView.swift         # Service discovery UI
│   ├── MessageView.swift           # Message exchange UI
│   └── Components/
│       ├── StatusIndicator.swift
│       └── MessageBubble.swift
├── ViewModels/
│   ├── WiFiAwareViewModel.swift    # State management
│   └── MessageViewModel.swift
├── Services/
│   ├── WiFiAwareManager.swift      # WiFi Aware wrapper
│   ├── DiscoveryService.swift      # Discovery logic
│   └── DataPathService.swift       # Data exchange
├── Models/
│   ├── Message.swift
│   ├── DeviceInfo.swift
│   └── ConnectionState.swift
└── Utils/
    ├── Logger.swift
    └── Constants.swift
```

## Building the App

### Build from Xcode

1. Select your development team in Signing & Capabilities
2. Connect your iOS device (WiFi Aware doesn't work in simulator)
3. Select your device as the target
4. Click Run (⌘ + R)

### Build from Command Line

```bash
xcodebuild -project WiFiAwareApp.xcodeproj \
    -scheme WiFiAwareApp \
    -destination 'platform=iOS,name=Your iPhone' \
    build
```

## WiFi Aware Implementation

### Import Framework

```swift
import WiFiAware
import Network
```

### Initialize WiFi Aware Session

```swift
class WiFiAwareManager: ObservableObject {
    private var session: WiFiAwareSession?

    func startSession() {
        session = WiFiAwareSession()

        guard session?.isAvailable == true else {
            print("WiFi Aware not available")
            return
        }

        // Session is ready
    }
}
```

### Subscribe to Service

```swift
func subscribeToService(serviceName: String) {
    guard let session = session else { return }

    let discoveryConfig = WiFiAwareDiscoveryConfiguration(
        serviceName: serviceName,
        serviceSpecificInfo: nil
    )

    let subscriber = WiFiAwareSubscriber(
        configuration: discoveryConfig,
        delegate: self
    )

    session.start(subscriber)
}

// MARK: - WiFiAwareSubscriberDelegate

extension WiFiAwareManager: WiFiAwareSubscriberDelegate {
    func subscriber(_ subscriber: WiFiAwareSubscriber,
                   didDiscoverPublisher publisher: WiFiAwarePublisher) {
        print("Discovered publisher: \(publisher)")
        // Establish data path
        establishDataPath(with: publisher)
    }

    func subscriber(_ subscriber: WiFiAwareSubscriber,
                   didLosePublisher publisher: WiFiAwarePublisher) {
        print("Lost publisher: \(publisher)")
    }
}
```

### Establish Data Path

```swift
func establishDataPath(with publisher: WiFiAwarePublisher) {
    let dataPathConfig = WiFiAwareDataPathConfiguration(
        peerDiscoveryInfo: publisher.discoveryInfo
    )

    let dataPath = WiFiAwareDataPath(
        configuration: dataPathConfig,
        delegate: self
    )

    session?.start(dataPath)
}

// MARK: - WiFiAwareDataPathDelegate

extension WiFiAwareManager: WiFiAwareDataPathDelegate {
    func dataPath(_ dataPath: WiFiAwareDataPath,
                 didEstablishConnection connection: NWConnection) {
        print("Data path established")
        self.connection = connection
        startReceiving()
    }

    func dataPath(_ dataPath: WiFiAwareDataPath,
                 didFailWithError error: Error) {
        print("Data path failed: \(error)")
    }
}
```

### Send and Receive Messages

```swift
func sendMessage(_ text: String) {
    guard let connection = connection else { return }

    let data = text.data(using: .utf8)!
    connection.send(content: data, completion: .contentProcessed { error in
        if let error = error {
            print("Send error: \(error)")
        } else {
            print("Message sent successfully")
        }
    })
}

func startReceiving() {
    connection?.receive(minimumIncompleteLength: 1,
                       maximumLength: 65536) { [weak self] data, context, isComplete, error in
        if let data = data, !data.isEmpty {
            let message = String(data: data, encoding: .utf8) ?? ""
            print("Received: \(message)")
        }

        if let error = error {
            print("Receive error: \(error)")
        } else {
            // Continue receiving
            self?.startReceiving()
        }
    }
}
```

## SwiftUI Integration

### View Model Example

```swift
@MainActor
class WiFiAwareViewModel: ObservableObject {
    @Published var isConnected = false
    @Published var messages: [Message] = []
    @Published var discoveredDevices: [DeviceInfo] = []

    private let manager = WiFiAwareManager()

    func startDiscovery() {
        manager.subscribeToService(serviceName: "rpi_control_service")
    }

    func sendMessage(_ text: String) {
        manager.sendMessage(text)
    }
}
```

### View Example

```swift
struct DiscoveryView: View {
    @StateObject private var viewModel = WiFiAwareViewModel()

    var body: some View {
        VStack {
            if viewModel.isConnected {
                Text("Connected to RPi")
                    .foregroundColor(.green)
            } else {
                Text("Searching...")
                    .foregroundColor(.orange)
            }

            Button("Start Discovery") {
                viewModel.startDiscovery()
            }

            List(viewModel.messages) { message in
                MessageBubble(message: message)
            }
        }
    }
}
```

## Testing

### Run Unit Tests

```bash
xcodebuild test -project WiFiAwareApp.xcodeproj -scheme WiFiAwareApp -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

### Manual Testing Checklist

- [ ] App builds successfully
- [ ] Runs on physical device (iOS 18+)
- [ ] WiFi Aware availability check works
- [ ] Service discovery initiates
- [ ] RPi service is discovered
- [ ] Data path establishes successfully
- [ ] Messages send correctly
- [ ] Messages receive correctly
- [ ] Connection state updates in UI
- [ ] App handles disconnections

## Debugging

### Enable Logging

```swift
import os.log

let logger = Logger(subsystem: "com.yourcompany.wifiaware", category: "discovery")

logger.info("Starting WiFi Aware discovery")
logger.error("Failed to establish data path: \(error.localizedDescription)")
```

### Console Filtering

In Xcode Console:

```plaintext
subsystem:com.yourcompany.wifiaware
```

### Common Issues

**Issue**: "WiFi Aware not available"
**Solution**: Verify device is iOS 18+ and has hardware support

**Issue**: Entitlement error
**Solution**: Request `com.apple.developer.networking.wifi-aware` entitlement from Apple

**Issue**: Discovery not working
**Solution**: Ensure WiFi is enabled, check service name matches RPi publisher

**Issue**: Cannot build to device
**Solution**: Check provisioning profile includes WiFi Aware capability

## Performance Considerations

- Use async/await for network operations
- Implement proper error handling for network failures
- Clean up sessions when app enters background
- Monitor battery usage during active WiFi Aware sessions

## Privacy & Security

- WiFi Aware data is transmitted over local network only
- Implement encryption for sensitive data
- Request minimal permissions
- Clearly explain WiFi Aware usage to users

## App Store Submission

Before submitting to App Store:

1. Ensure you have WiFi Aware entitlement approval
2. Provide clear privacy policy
3. Document WiFi Aware usage in App Store description
4. Include required device capabilities in Info.plist
5. Test on multiple device models (if available)

## Resources

- [Apple WiFi Aware Framework](https://developer.apple.com/documentation/WiFiAware)
- [WWDC Session on WiFi Aware](https://developer.apple.com/videos/play/wwdc2024/)
- [Network Framework Guide](https://developer.apple.com/documentation/network)
- [WiFi Alliance - Wi-Fi Aware](https://www.wi-fi.org/discover-wi-fi/wi-fi-aware)

## Troubleshooting

For issues specific to iOS implementation:

1. Verify iOS version (18.0+ required)
2. Check device compatibility
3. Confirm entitlement is properly configured
4. Review console logs for specific errors
5. Test on physical device (not simulator)

For general architecture questions, see [architecture.md](architecture.md).
