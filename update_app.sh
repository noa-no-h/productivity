#!/bin/bash

# Navigate to your project directory
cd /NoasPythonProjects/productivity

# Pull the latest changes from GitHub
git pull

# Activate the virtual environment
source env/bin/activate

# Install updated dependencies
pip install -r requirements.txt

# Rebuild your application with PyInstaller
pyinstaller --onefile main.py

# Create .app bundle structure
mkdir -p Productivity.app/Contents/MacOS

# Move PyInstaller executable into MacOS directory
mv dist/productivity Productivity.app/Contents/MacOS/Productivity

# Create Info.plist file inside Productivity.app/Contents
cat << EOF > Productivity.app/Contents/Info.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Productivity</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.yourdomain.productivity</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <string>1</string>
</dict>
</plist>
EOF

