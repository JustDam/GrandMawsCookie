# GrandMawsCookie APK Build Instructions

## Prerequisites (Required)

Your system is **missing these components** needed for Android APK build:
- ❌ **Java Development Kit (JDK) 11+** - Required for Gradle compilation
- ❌ **Android SDK** - Required for Android framework libraries
- ❌ **Android NDK** - Required for native code compilation
- ❌ **Gradle** - Required for APK assembly

**Note:** Building Android APKs on Windows is challenging. The recommended approach is:

### Option 1: Use Windows Subsystem for Linux (WSL) - RECOMMENDED

1. **Enable WSL2 on Windows:**
   ```powershell
   wsl --install
   wsl --set-default-version 2
   ```

2. **Install Ubuntu in WSL:**
   ```powershell
   wsl --install Ubuntu
   ```

3. **In WSL terminal, install build dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv git openjdk-11-jdk
   pip3 install buildozer cython
   ```

4. **Install Android SDK & NDK (automated via buildozer):**
   ```bash
   cd /mnt/c/Users/bruma/OneDrive/Documents/PYTHON\ FILES/GrandMawsCookie
   buildozer android debug
   ```
   First run will download ~1-2 GB of Android tools to `~/.buildozer/`

5. **APK output:**
   ```
   bin/grandmawscookie-1.0.0-debug.apk
   ```

---

### Option 2: Use Docker (Offline/Network-safe)

Create a Dockerfile:
```dockerfile
FROM ubuntu:22.04
RUN apt update && apt install -y python3 python3-pip openjdk-11-jdk
RUN pip3 install buildozer cython
WORKDIR /app
CMD ["buildozer", "android", "debug"]
```

Build and run:
```bash
docker build -t kivy-builder .
docker run -v C:\Users\bruma\OneDrive\Documents\PYTHON\ FILES\GrandMawsCookie:/app kivy-builder
```

---

### Option 3: Use Online Build Service

Services like **Buildozer Cloud** or **GitHub Actions** can build APKs without local Android tools.

---

## Manual Build (Advanced - For Reference)

If you have Android SDK/NDK installed in `C:\Android\sdk` and `C:\Android\ndk-r25b`:

```powershell
cd "C:\Users\bruma\OneDrive\Documents\PYTHON FILES\GrandMawsCookie"

$env:ANDROIDSDK = "C:\Android\sdk"
$env:ANDROIDNDK = "C:\Android\ndk-r25b"

buildozer android debug
```

---

## Verify Current buildozer.spec

✅ Configuration is ready:
```ini
[app]
title = Grand Maws Cookie Recipe Adjuster
package.name = grandmawscookie
package.domain = org.example
main.py = GrandMawsCookie_APK.py
version = 1.0.0
requirements = python3,kivy,android
orientation = portrait
android.minapi = 21
android.maxapi = 33
```

---

## After Build

Once APK is built, install on device/emulator:

```bash
adb install -r bin/grandmawscookie-1.0.0-debug.apk
```

Or open Android Studio emulator and drag-drop the APK.

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `"buildozer: command not found"` | `pip install buildozer` |
| `"Java not found"` | Install JDK 11: `choco install openjdk11` (Windows) or `sudo apt install openjdk-11-jdk` (Linux) |
| `"Android SDK not found"` | Let buildozer auto-download on first run (1-2 GB download) |
| `"gradlew permission denied"` | Use WSL/Linux instead of Windows |
| Build hangs during download | Check internet connection; buildozer downloads ~1.5 GB |

---

## Current Status

| Component | Status |
|-----------|--------|
| Python code | ✅ Ready |
| Kivy UI | ✅ Ready |
| buildozer.spec | ✅ Configured |
| Unit tests | ✅ Passing |
| Android tools | ❌ Not installed (normal on Windows) |

**Recommendation:** Use WSL2 for the smoothest build experience.
