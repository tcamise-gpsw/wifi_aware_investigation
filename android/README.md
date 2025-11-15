# Android WiFi Aware App

Android application demonstrating WiFi Aware functionality for the WiFi Aware investigation project.

## Overview

This Android app discovers and connects to the Raspberry Pi WiFi Aware service, enabling peer-to-peer communication without requiring internet or a traditional WiFi access point.

## Prerequisites

- Android device with WiFi Aware support (Android 8.0+, API level 26+)
- Android Studio (latest stable version)
- JDK 11 or higher
- See [docs/android-setup.md](../docs/android-setup.md) for complete setup instructions

## Device Compatibility

Not all Android devices support WiFi Aware. Check compatibility:

```bash
adb shell pm list features | grep wifi.aware
```

Common compatible devices:
- Google Pixel 2 and newer
- Samsung Galaxy S9 and newer
- OnePlus 6 and newer

## Quick Start

### Open in Android Studio

```bash
cd wifi_aware_investigation/android
# Open this directory in Android Studio
```

### Build and Run

1. Open project in Android Studio
2. Sync Gradle files
3. Connect your Android device
4. Click Run (Shift + F10)

### Command Line Build

```bash
./gradlew assembleDebug
./gradlew installDebug
```

## Project Structure

```plaintext
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/gopro/wifiaware/
│   │   │   │   ├── ui/
│   │   │   │   │   ├── MainActivity.kt
│   │   │   │   │   ├── screens/
│   │   │   │   │   └── viewmodels/
│   │   │   │   ├── wifiaware/
│   │   │   │   │   ├── WifiAwareManager.kt
│   │   │   │   │   ├── DiscoverySession.kt
│   │   │   │   │   └── DataPath.kt
│   │   │   │   └── models/
│   │   │   ├── AndroidManifest.xml
│   │   │   └── res/
│   │   └── test/
│   ├── build.gradle.kts
│   └── proguard-rules.pro
├── gradle/
├── build.gradle.kts
├── settings.gradle.kts
└── README.md
```

## Key Features

- WiFi Aware service discovery
- Peer-to-peer data path establishment
- Real-time message exchange
- Connection state monitoring
- Material Design 3 UI

## Required Permissions

The app requires these permissions:

```xml
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.NEARBY_WIFI_DEVICES" />
```

## Configuration

No configuration needed for basic usage. The app will automatically:
- Request necessary permissions on first launch
- Discover the RPi service named "rpi_control_service"
- Establish data path when service is found
- Begin message exchange

## Testing

### Run Unit Tests

```bash
./gradlew test
```

### Run Instrumentation Tests

```bash
./gradlew connectedAndroidTest
```

## Debugging

Enable verbose logging:

```bash
adb logcat -s WifiAware:D
```

## Documentation

For detailed setup, implementation, and troubleshooting:
- [Android Setup Guide](../docs/android-setup.md)
- [Architecture Documentation](../docs/architecture.md)

## Status

🚧 **Stub - Implementation pending**

This is a placeholder structure. Full Android app implementation will include:
- Complete WiFi Aware API integration
- Jetpack Compose UI
- ViewModel architecture
- Message protocol implementation
- Comprehensive testing
- Error handling and reconnection logic

## Technology Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Android WiFi Aware API
- Coroutines & Flow
- Hilt (Dependency Injection)
