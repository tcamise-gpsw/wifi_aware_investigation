# WiFi Aware Investigation - Copilot Instructions

## Project Overview

This is a **proof-of-concept** multi-platform WiFi Aware (NAN - Neighbor Awareness Networking) demonstration. The architecture consists of three independent applications that communicate via peer-to-peer WiFi Aware:

- **Raspberry Pi** (`rpi/`): Control device that publishes WiFi Aware services (Python)
- **Android** (`android/`): Subscriber client app (Kotlin + Jetpack Compose)
- **iOS** (`ios/`): Subscriber client app (Swift + SwiftUI)

**Key principle**: Each platform operates independently but follows a common protocol for discovery and messaging (see `docs/architecture.md`).

## Architecture Patterns

### Platform Responsibilities

**RPi is the publisher/coordinator**: It initializes WiFi Aware sessions and advertises services. Android/iOS are subscribers that discover and connect.

**No internet required**: All communication happens over WiFi Aware peer-to-peer. No traditional WiFi AP or internet connection is involved.

**JSON-based protocol**: Devices exchange structured messages (discovery, data, status) defined in `docs/architecture.md` with `type`, `device_id`, `platform`, and `timestamp` fields.

### Critical Hardware Requirements

- **Android**: Requires API 26+ and `android.hardware.wifi.aware` feature. Not all devices support it (verify with `pm list features`).
- **iOS**: Requires iOS 18.0+ and specific hardware (iPhone 15 Pro+, M1+ iPads). **Simulator won't work**.
- **RPi**: Requires WiFi Aware capable hardware (BCM43455 on RPi 4) and wpa_supplicant 2.10+ with NAN support.

## Development Workflows

### Android (android/)

**Build system**: Gradle with Kotlin DSL

**Prerequisites**:
- Android SDK with API level 26+ (Android 8.0 Oreo or higher)
- Gradle 9.0+ (included via wrapper)
- JDK 17+ recommended

**Building from command line**:
```bash
cd android
./gradlew assembleDebug      # Build debug APK
./gradlew assembleRelease    # Build release APK (requires signing config)
./gradlew installDebug       # Build and install to connected device/emulator
./gradlew clean              # Clean build artifacts
```

**Build output**: APK is generated at `app/build/outputs/apk/debug/app-debug.apk`

**Key configuration files**:
- `gradle.properties`: Must include `android.useAndroidX=true` for AndroidX dependency support
- `app/build.gradle.kts`:
  - `minSdk=26` (WiFi Aware API level requirement)
  - Jetpack Compose enabled with BOM version 2024.02.00
  - Kotlin version aligned with Compose compiler
- `AndroidManifest.xml`:
  - Required permissions: `ACCESS_WIFI_STATE`, `CHANGE_WIFI_STATE`, `ACCESS_FINE_LOCATION`, `NEARBY_WIFI_DEVICES`
  - Required hardware feature: `android.hardware.wifi.aware` with `required="true"`

**Common build issues**:
1. **"android.useAndroidX property is not enabled"**: Create `gradle.properties` with `android.useAndroidX=true`
2. **Missing launcher icons**: Ensure `mipmap-anydpi-v26/` contains `ic_launcher.xml` and `ic_launcher_round.xml` adaptive icons, with corresponding `drawable/ic_launcher_background.xml` and `drawable/ic_launcher_foreground.xml` resources
3. **Gradle Daemon issues**: Run `./gradlew --stop` to stop all daemons, then retry build
4. **SDK/JDK version mismatch**: Check `JAVA_HOME` and ensure JDK 17+ is installed

**IDE setup**:
- Open `android/` directory in Android Studio
- Gradle sync will automatically download dependencies
- Use "Build > Make Project" or "Build > Build Bundle(s) / APK(s) > Build APK(s)"

**Current state**: Basic Compose UI skeleton exists (`MainActivity.kt`). WiFi Aware manager implementation is pending.

### iOS (ios/)

**Build system**: Xcode project (no CocoaPods/SPM yet)
```bash
cd ios
open WiFiAwareApp.xcodeproj
```

**Key files**:
- `WiFiAwareApp.entitlements`: Must include `com.apple.developer.networking.wifi-aware`
- `Info.plist`: Requires `NSLocalNetworkUsageDescription` and `NSBonjourServices` entries

**Current state**: Basic SwiftUI skeleton (`ContentView.swift`). WiFi Aware framework integration pending. **Must test on physical device only**.

### Raspberry Pi (rpi/)

**Runtime**: Python 3.8+ with virtual environment
```bash
cd rpi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo python3 main.py  # Requires root for WiFi operations
```

**Dependencies**: `pyroute2` (network management), `python-networkmanager` (NM integration), `PyYAML` (config parsing). See `requirements.txt`.

**Configuration**: `config/settings.yaml` defines service name, network interface (wlan0), and protocol settings.

**Current state**: Entry point (`main.py`) exists with logging and signal handling. Core WiFi Aware manager (`src/wifi_aware_manager.py`) not implemented yet.

## Project Conventions

### Commit Messages

Use conventional commits enforced by `commitlint.config.js`:
```
type(scope): subject

Types: feat, fix, docs, chore, refactor, test, ci, build
Scopes: rpi, android, ios, docs, config, deps, ci
```

Examples:
- `feat(android): implement WiFi Aware discovery manager`
- `fix(rpi): handle connection timeout in publisher`
- `docs(ios): update setup instructions for Xcode 16`

### File Organization

- **Documentation first**: All setup guides live in `docs/` (platform-specific: `android-setup.md`, `ios-setup.md`, `rpi-setup.md`)
- **Platform isolation**: Each platform directory is self-contained with its own build system and README
- **Shared protocol**: Message formats defined in `docs/architecture.md` are the contract between platforms

### Testing Strategy

- **Device compatibility checks**: Always verify WiFi Aware availability before attempting operations
- **Physical device required**: WiFi Aware doesn't work on emulators/simulators
- **Multi-device scenarios**: Test with RPi publisher + at least one subscriber (Android or iOS) running simultaneously

## Common Pitfalls

1. **Permissions**: WiFi Aware requires location permissions on Android (even though it's proximity-based, not GPS).
2. **Root access**: RPi service needs `sudo` to manage WiFi interfaces.
3. **wpa_supplicant version**: RPi must have version 2.10+ with NAN support compiled in.
4. **iOS entitlements**: The WiFi Aware entitlement may require explicit approval from Apple Developer Support.
5. **Service names**: Must be consistent across platforms for discovery (currently "rpi_control_service" in config).

## Integration Points

- **Discovery phase**: RPi publishes service → Android/iOS scan and match by service name → Exchange discovery messages
- **Data path**: After discovery, establish direct peer-to-peer connection using WiFi Aware data paths (not implemented yet)
- **Message protocol**: JSON format with `type`, `sender`, `sequence`, `payload`, `timestamp` (see `docs/architecture.md`)

## When Adding Features

1. **Check device compatibility first**: Add runtime checks for WiFi Aware availability
2. **Update all three platforms**: Features should maintain protocol compatibility
3. **Document hardware requirements**: Update relevant setup docs if new capabilities require specific hardware
4. **Follow platform idioms**: Kotlin coroutines (Android), Swift async/await (iOS), Python asyncio (RPi)
5. **Log extensively**: This is a POC for investigating WiFi Aware behavior - capture connection states, latencies, errors
