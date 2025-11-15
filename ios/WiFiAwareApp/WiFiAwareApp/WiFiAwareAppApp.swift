//
//  WiFiAwareAppApp.swift
//  WiFiAwareApp
//
//  Created by tcamise on 11/14/25.
//

import SwiftUI

@main
struct WiFiAwareAppApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .onAppear {
                    appState.checkWiFiAwareSupport()
                }
        }
    }
}

/// Application state manager that handles WiFi Aware capability checking
@MainActor
class AppState: ObservableObject {
    @Published var wifiAwareSupported: Bool = false
    @Published var supportMessage: String = "Checking WiFi Aware support..."
    @Published var showUnsupportedAlert: Bool = false

    /// Check WiFi Aware support early at app launch
    func checkWiFiAwareSupport() {
        if #available(iOS 18.0, *) {
            let checker = WIFIAwareCapabilityCheck()
            let result = checker.checkSupport()

            switch result {
            case .supported:
                wifiAwareSupported = true
                supportMessage = "✓ WiFi Aware is supported on this device"
            case .notSupported(let reason):
                wifiAwareSupported = false
                supportMessage = "✗ WiFi Aware not available: \(reason)\n\nWiFi Aware requires iOS 18.0+ and specific hardware (iPhone 15 Pro or later, iPad with M1+ chip)"
                showUnsupportedAlert = true
            }
        } else {
            wifiAwareSupported = false
            supportMessage = "✗ WiFi Aware requires iOS 18.0 or later. This device is running an older version."
            showUnsupportedAlert = true
        }
    }
}
