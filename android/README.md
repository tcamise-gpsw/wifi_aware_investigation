# Android WiFi Aware App

Android application demonstrating WiFi Aware functionality for the WiFi Aware investigation project.

## Overview

This Android app discovers and connects to the Raspberry Pi WiFi Aware service, enabling peer-to-peer communication without requiring internet or a traditional WiFi access point.

## Prerequisites

### Hardware

- Android device with WiFi Aware support (Android 8.0+, API level 26+)
- Not all Android devices support WiFi Aware - verify before testing

### Software

- Android Studio (latest stable version)
- JDK 17+ (recommended)
- Android SDK with API level 26+

## Device Compatibility

Verify your device supports WiFi Aware:

```bash
adb shell pm list features | grep wifi.aware
```

Should return: `feature:android.hardware.wifi.aware`

Common compatible devices:

- Google Pixel 2 and newer
- Samsung Galaxy S9 and newer
- OnePlus 6 and newer

## Building the App

### Option 1: Android Studio

1. Open the `android/` directory in Android Studio
2. Wait for Gradle sync to complete
3. Connect your Android device via USB
4. Click Run (⌘R or Shift+F10)

### Option 2: Command Line

```bash
cd android

# Build debug APK
./gradlew assembleDebug

# Build and install to connected device
./gradlew installDebug

# Clean build artifacts
./gradlew clean
```

Build output: `app/build/outputs/apk/debug/app-debug.apk`


## Key Features

- WiFi Aware service discovery
- Peer-to-peer data path establishment
- Real-time message exchange
- Connection state monitoring
- Material Design 3 UI

## Running the App

### First Launch

The app will request the following permissions:

- **Location** (required for WiFi scanning, even though WiFi Aware is proximity-based)
- **Nearby devices** (Android 12+)

Ensure WiFi and Location services are enabled on your device.

### What It Does

The app automatically:

- Discovers the RPi service named "rpi_control_service"
- Establishes peer-to-peer data path when service is found
- Exchanges JSON messages per the protocol in `../docs/architecture.md`

### Required Permissions (already configured)

```xml
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.NEARBY_WIFI_DEVICES" />
<uses-feature android:name="android.hardware.wifi.aware" android:required="true" />
```

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

### View Logs

```bash
# Filter for WiFi Aware logs
adb logcat -s WifiAware:D

# View all app logs
adb logcat | grep com.yourpackage
```

### Common Issues

**Issue**: Device doesn't support WiFi Aware
**Solution**: Verify with `adb shell pm list features | grep wifi.aware`

**Issue**: Service not discovered
**Solution**: Ensure RPi is running and publishing, both devices within ~30m range

**Issue**: Permission denied errors
**Solution**: Grant location permissions in Settings > Apps > WiFi Aware App

## Resources

- [Android WiFi Aware Guide](https://developer.android.com/develop/connectivity/wifi/wifi-aware)
- [WiFi Aware API Reference](https://developer.android.com/reference/android/net/wifi/aware/package-summary)
- [Architecture Documentation](../docs/architecture.md)

## Documentation

For detailed setup, implementation, and troubleshooting:

- [Android Setup Guide](../docs/android-setup.md)
- [Architecture Documentation](../docs/architecture.md)

## Current State

🚧 **Basic skeleton implemented**

**Implemented:**

- Project structure with Gradle build system
- AndroidX and Jetpack Compose setup
- Basic Material Design 3 UI shell (`MainActivity.kt`)
- Required permissions declared in manifest
- WiFi Aware hardware feature requirement configured

**Pending:**

- WiFi Aware manager implementation
- Service discovery logic
- Data path establishment
- Message protocol handling
- Connection state management
- UI components for discovery and messaging

## Technology Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Android WiFi Aware API
- Coroutines & Flow
- Hilt (Dependency Injection)
