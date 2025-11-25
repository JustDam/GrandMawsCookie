# Grand Maws Cookie Recipe Adjuster - APK Build Guide

## Files Included

- **GrandMawsCookie_APK.py** - Main Kivy application (mobile UI)
- **GrandMawsCookie_Console_Working.py** - Console version (reference)
- **buildozer.spec** - Build configuration for Android APK
- **requirements.txt** - Python dependencies

## Setup & Build Instructions

### Prerequisites
1. Install Python 3.9+ on your development machine
2. Install Java Development Kit (JDK) 11 or higher
3. Install Android SDK

### Step 1: Install Dependencies
```bash
pip install kivy==2.2.1
pip install buildozer==1.5.0
pip install cython
```

### Step 2: Configure buildozer.spec
Edit `buildozer.spec` and update:
- `package.domain` - Your organization domain
- `android.permissions` - Add permissions if needed
- `android.minapi` - Minimum Android API level

### Step 3: Build APK (Linux/Mac recommended)
```bash
buildozer android debug
```

For release builds:
```bash
buildozer android release
```

### Step 4: Install on Device
```bash
adb install -r bin/grandmawscookie-1.0.0-debug.apk
```

## Android Studio Integration

If using Android Studio:

1. Open Android Studio
2. Create new project → Empty Activity
3. Replace `MainActivity.java` with Kivy launcher
4. Add Kivy gradle dependencies
5. Build APK through Android Studio

## Mobile-Optimized Features

✓ Responsive UI that scales to phone screen sizes
✓ Portrait orientation for recipe display
✓ Touch-friendly input fields (numeric keyboard)
✓ Scrollable results for long recipes
✓ Error popups for invalid input
✓ Clean, readable typography for cooking

## Screen Specifications

- **Min Screen Width:** 320dp (small phones)
- **Max Screen Width:** 600dp (tablets)
- **Orientation:** Portrait (fixed)
- **API Level:** 21 (Android 5.0+) to 33 (Android 13)

## Testing on Emulator

1. Launch Android Emulator in Android Studio
2. Run: `adb install -r bin/grandmawscookie-1.0.0-debug.apk`
3. Open app from device home screen

## Troubleshooting

**Issue:** "buildozer: command not found"
- Solution: Install globally or use `python -m buildozer`

**Issue:** Kivy not found in build
- Solution: Ensure `kivy` is in `requirements` in buildozer.spec

**Issue:** Numeric input not restricting numbers
- Solution: Use `TextInput` with `input_filter='int'`

## Notes for Development

- Console version (`GrandMawsCookie_Console_Working.py`) useful for testing logic
- All calculation functions are unchanged and portable
- Assertions included for validation (disable with `-O` flag if needed)
