# Android WiFi Aware App - Setup Guide

## Prerequisites

### Hardware Requirements

- Android device with WiFi Aware support (Android 8.0+, API level 26+)
- Not all Android devices support WiFi Aware - check device compatibility
- Common devices with support: Google Pixel 2+, Samsung Galaxy S9+, etc.

### Software Requirements

- Android Studio (latest stable version)
- JDK 11 or higher
- Android SDK with API level 26+
- Gradle 7.0+

## Checking Device Compatibility

Before proceeding, verify your device supports WiFi Aware:

```kotlin
val wifiAwareManager = context.getSystemService(Context.WIFI_AWARE_SERVICE) as WifiAwareManager?
val isAvailable = wifiAwareManager?.isAvailable ?: false
```

You can also check via ADB:

```bash
adb shell pm list features | grep wifi.aware
```

Should return: `feature:android.hardware.wifi.aware`

## Project Setup

### 1. Clone and Open Project

```bash
cd wifi_aware_investigation/android
```

Open the `android/` directory in Android Studio.

### 2. Required Permissions

The app requires the following permissions in `AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.NEARBY_WIFI_DEVICES" />

<!-- WiFi Aware requires these hardware features -->
<uses-feature android:name="android.hardware.wifi.aware" android:required="true" />
```

### 3. Gradle Dependencies

In `app/build.gradle.kts`:

```kotlin
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")

    // Jetpack Compose
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.activity:activity-compose:1.8.2")

    // Lifecycle
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}
```

## Building the App

### Build from Android Studio

1. Open the project in Android Studio
2. Sync Gradle files
3. Select your device or emulator
4. Click Run (Shift + F10)

### Build from Command Line

```bash
cd android
./gradlew assembleDebug
```

Install to connected device:

```bash
./gradlew installDebug
```

## Running the App

### Grant Required Permissions

On first launch, the app will request:

- Location permission (required for WiFi scanning)
- Nearby devices permission (Android 12+)

### Enable WiFi and Location

- WiFi must be enabled
- Location services must be enabled
- WiFi Aware is automatically managed by the system

## App Architecture

### Key Components

```plaintext
app/
├── ui/
│   ├── MainActivity.kt           # Entry point
│   ├── screens/
│   │   ├── DiscoveryScreen.kt   # WiFi Aware discovery UI
│   │   └── MessageScreen.kt     # Message exchange UI
│   └── viewmodels/
│       └── WifiAwareViewModel.kt # State management
├── wifiaware/
│   ├── WifiAwareManager.kt      # WiFi Aware wrapper
│   ├── DiscoverySession.kt      # Discovery logic
│   └── DataPath.kt              # Data exchange
└── models/
    ├── Message.kt
    └── DeviceInfo.kt
```

## WiFi Aware Implementation

### Initialize WiFi Aware

```kotlin
class WifiAwareManager(private val context: Context) {
    private val wifiAwareManager = context.getSystemService(Context.WIFI_AWARE_SERVICE) as WifiAwareManager

    fun attachSession(callback: AttachCallback) {
        wifiAwareManager.attach(callback, null)
    }
}
```

### Subscribe to Service

```kotlin
val config = SubscribeConfig.Builder()
    .setServiceName("rpi_control_service")
    .build()

discoverySession.subscribe(config, object : DiscoverySessionCallback() {
    override fun onSubscribeStarted(session: SubscribeDiscoverySession) {
        // Successfully subscribed
    }

    override fun onServiceDiscovered(peerHandle: PeerHandle, serviceSpecificInfo: ByteArray, matchFilter: List<ByteArray>) {
        // Discovered RPi service
    }
})
```

### Establish Data Path

```kotlin
val config = WifiAwareNetworkSpecifier.Builder(discoverySession, peerHandle)
    .build()

val request = NetworkRequest.Builder()
    .addTransportType(NetworkCapabilities.TRANSPORT_WIFI_AWARE)
    .setNetworkSpecifier(config)
    .build()

connectivityManager.requestNetwork(request, networkCallback)
```

## Testing

### Unit Tests

```bash
./gradlew test
```

### Instrumentation Tests

```bash
./gradlew connectedAndroidTest
```

### Manual Testing Checklist

- [ ] App launches without crashes
- [ ] Permissions are requested and granted
- [ ] WiFi Aware session attaches successfully
- [ ] Service discovery works
- [ ] Connection to RPi establishes
- [ ] Messages send/receive correctly
- [ ] UI updates reflect connection state
- [ ] App handles disconnections gracefully

## Debugging

### Enable Verbose Logging

```kotlin
Log.d("WifiAware", "Message: $details")
```

### ADB Logcat Filtering

```bash
adb logcat -s WifiAware:D
```

### Common Issues

**Issue**: `WifiAwareManager is null`
**Solution**: Device doesn't support WiFi Aware

**Issue**: `WIFI_AWARE_DATA_PATH_ROLE_RESPONDER failed`
**Solution**: Check that both devices are on compatible WiFi channels

**Issue**: Service not discovered
**Solution**: Ensure RPi is publishing the service and both devices are in range (~30m)

## Performance Optimization

- Use coroutines for async WiFi Aware operations
- Implement proper lifecycle management
- Clean up sessions when app goes to background
- Handle rapid connection/disconnection scenarios

## Resources

- [Android WiFi Aware Guide](https://developer.android.com/develop/connectivity/wifi/wifi-aware)
- [WiFi Aware Sample Code](https://github.com/android/connectivity-samples)
- [WiFi Aware API Reference](https://developer.android.com/reference/android/net/wifi/aware/package-summary)

## Troubleshooting

For issues specific to the Android implementation, check:

1. Device compatibility list
2. Android version (8.0+ required)
3. Location and WiFi permissions
4. WiFi Aware feature flag in manifest

For general architecture questions, see [architecture.md](architecture.md).
