//
//  WIFIAwareCapabilityCheck.swift
//  WiFiAwareApp
//
//  Provides runtime capability checking for WiFi Aware support.
//

import Foundation
import WiFiAware

/// Utility for checking WiFi Aware hardware and software support at runtime.
///
/// WiFi Aware requires specific hardware capabilities and iOS 18.0+. Not all devices
/// support WiFi Aware even if running iOS 18.0 or later.
///
/// ## References
/// - [WiFi Aware Framework Documentation](https://developer.apple.com/documentation/wifiaware)
/// - [WIFIAwarePublisher Documentation](https://developer.apple.com/documentation/wifiaware/wifiawarepublisher)
/// - [WIFIAwareSubscriber Documentation](https://developer.apple.com/documentation/wifiaware/wifiawaresubscriber)
///
/// ## Usage
/// ```swift
/// let capability = WIFIAwareCapabilityCheck()
/// let result = capability.checkSupport()
///
/// switch result {
/// case .supported:
///     print("WiFi Aware is available")
/// case .notSupported(let reason):
///     print("WiFi Aware not available: \(reason)")
/// }
/// ```
@available(iOS 18.0, *)
struct WIFIAwareCapabilityCheck {

    /// Result of WiFi Aware capability check
    enum SupportResult {
        /// WiFi Aware is fully supported on this device
        case supported

        /// WiFi Aware is not supported, with a reason
        case notSupported(reason: String)

        var isSupported: Bool {
            if case .supported = self {
                return true
            }
            return false
        }
    }

    /// Check if WiFi Aware is supported on the current device.
    ///
    /// This method checks both publisher and subscriber capabilities. WiFi Aware
    /// requires hardware support which is only available on certain devices.
    ///
    /// According to Apple's documentation, `WIFIAwarePublisher.isSupported` and
    /// `WIFIAwareSubscriber.isSupported` return `true` only if the device has
    /// the necessary hardware capabilities for WiFi Aware operations.
    ///
    /// - Returns: `SupportResult` indicating whether WiFi Aware is supported
    ///
    /// - Note: Must be called on iOS 18.0+ devices. For older iOS versions,
    ///         WiFi Aware framework is not available.
    func checkSupport() -> SupportResult {
        // Check publisher support
        let publisherSupported = WIFIAwarePublisher.isSupported

        // Check subscriber support
        let subscriberSupported = WIFIAwareSubscriber.isSupported

        // Both must be supported for full WiFi Aware functionality
        if publisherSupported && subscriberSupported {
            return .supported
        } else if !publisherSupported && !subscriberSupported {
            return .notSupported(reason: "Device hardware does not support WiFi Aware (neither publisher nor subscriber)")
        } else if !publisherSupported {
            return .notSupported(reason: "Device hardware does not support WiFi Aware publisher")
        } else {
            return .notSupported(reason: "Device hardware does not support WiFi Aware subscriber")
        }
    }

    /// Check only subscriber support (most common use case for this app).
    ///
    /// - Returns: `true` if the device supports WiFi Aware subscriber operations
    func checkSubscriberSupport() -> Bool {
        return WIFIAwareSubscriber.isSupported
    }

    /// Check only publisher support.
    ///
    /// - Returns: `true` if the device supports WiFi Aware publisher operations
    func checkPublisherSupport() -> Bool {
        return WIFIAwarePublisher.isSupported
    }

    /// Get a detailed support status message suitable for displaying to users.
    ///
    /// - Returns: Human-readable string describing WiFi Aware support status
    func getSupportStatusMessage() -> String {
        let result = checkSupport()

        switch result {
        case .supported:
            return "✓ WiFi Aware is supported on this device"
        case .notSupported(let reason):
            return "✗ WiFi Aware not available: \(reason)\n\nWiFi Aware requires iOS 18.0+ and specific hardware (iPhone 15 Pro or later, iPad with M1+ chip)"
        }
    }
}

// MARK: - Convenience Extensions

@available(iOS 18.0, *)
extension WIFIAwareCapabilityCheck {
    /// Quick check if WiFi Aware is available without detailed reason
    static var isAvailable: Bool {
        let check = WIFIAwareCapabilityCheck()
        return check.checkSupport().isSupported
    }
}
