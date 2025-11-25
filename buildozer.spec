[app]
# Application metadata
title = Grand Maws Cookie Recipe Adjuster
package.name = grandmawscookie
package.domain = org.example

# Source code location
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Main entry point
main.py = GrandMawsCookie_APK.py

# Version
version = 1.0.0

# App requirements
requirements = python3,kivy

# Permissions needed for Android
android.permissions = INTERNET

# Features
android.features = android.hardware.screen.portrait

# Icons and graphics
android.presplash = 

# Gradle build settings
android.gradle_dependencies = 

# Min/Max API levels for Android
android.minapi = 21
android.maxapi = 31
android.ndk = 25b
android.sdk = 31

# Orientation - portrait mode for recipe display
orientation = portrait

# Window settings
fullscreen = 0

# Build settings
log_level = 2
warn_on_root = 1
