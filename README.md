# WhatsApp Automation Tool

An advanced WhatsApp automation tool that provides multiple features for enhancing your WhatsApp experience.

## Key Features

### 1. Messaging Features
- Send text messages to multiple contacts
- Text-to-speech conversion
- Schedule messages
- Translate messages to multiple languages
- Send audio messages

### 2. Location Features
- Share real-time live location
- Send mock locations
- Customize location sharing duration
- Support for both static and live locations

### 3. Status Monitoring
- Check contacts' online status
- Real-time status updates

### 4. Profile Features
- Convert videos to profile pictures
- Create animated profile pictures
- Automatic profile picture changing

## Installation

### For Linux (Ubuntu/Debian)

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-tk ffmpeg espeak git
```

2. Clone and set up:
```bash
git clone https://github.com/ishaq2321/WA_automation.git
cd whatsapp-automation-tool
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

3. Run the tool:
```bash
python3 wa.py
```

### For Windows

1. Install Python:
   - Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Check "Install pip"

2. Install FFmpeg:
   - Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract the zip file
   - Add FFmpeg's bin fwaer to System PATH:
     - Right-click Computer → Properties → Advanced System Settings
     - Environment Variables → System Variables → Path → Edit
     - Add the path to FFmpeg's bin fwaer
     - Click OK on all windows

3. Install eSpeak:
   - Download eSpeak from [sourceforge.net/projects/espeak](https://sourceforge.net/projects/espeak/)
   - Run the installer
   - During installation, select "Add to PATH"

4. Clone and setup:
   ```cmd
   # Open Command Prompt as Administrator
   git clone https://github.com/ishaq2321/WA_automation.git
   cd whatsapp-automation-tool
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Run the tool:
   ```cmd
   python wa.py
   ```

### Verifying Installation

1. Test Python:
```bash
python --version  # Should show Python 3.8+
pip --version     # Should show pip version
```

2. Test FFmpeg:
```bash
ffmpeg -version  # Should show FFmpeg version
```

3. Test eSpeak:
```bash
espeak "Hello World"  # Should speak the text
```

## Common Installation Issues

### Windows
1. "Python not found":
   - Make sure Python is added to PATH
   - Try using `py` instead of `python`

2. "FFmpeg not found":
   - Verify FFmpeg in PATH
   - Restart Command Prompt after PATH changes

3. "eSpeak not working":
   - Reinstall with "Add to PATH" option
   - Check Windows Sound settings

### Linux
1. Permission denied:
   ```bash
   sudo chown -R $USER:$USER .
   sudo chmod +x wa.py
   ```

2. pip installation fails:
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```

3. Missing build tools:
   ```bash
   sudo apt-get install python3-dev build-essential
   ```

## System Requirements

### Minimum Requirements
- Python 3.8 or higher
- 4GB RAM
- Chrome Browser
- Internet connection
- 500MB free disk space

### Recommended
- Python 3.9+
- 8GB RAM
- Chrome Browser (latest version)
- Stable Internet connection
- 1GB free disk space

## Post-Installation Setup

1. Chrome Browser:
   - Install latest version
   - Enable location services if needed
   - Allow notifications if needed

2. WhatsApp Web:
   - Have your phone ready for QR code scan
   - Enable location sharing in browser
   - Grant necessary permissions

## Running the Tool

1. Start the tool:
```bash
# Linux
python3 wa.py

# Windows
python wa.py
```

2. First-time setup:
   - Click "Start the tool"
   - Scan WhatsApp Web QR code
   - Click "I am now logged in"
   - Choose desired features from menu

## Feature Guide

### Sending Messages
1. Select "Send Message"
2. Enter contact name(s)
3. Type message
4. Optional: Enable audio/translation/scheduling
5. Click Send

### Location Sharing
1. Select "Share Mock Location"
2. Choose between mock or real location
3. For mock: Enter location name
4. For live: Select duration
5. Click Share

### Profile Picture Animation
1. Select "Video Profile Change"
2. Choose video file or existing frames
3. Follow on-screen instructions
4. Use responsibly to avoid restrictions

## Security Notes

- Never share WhatsApp session data
- Use scheduling features responsibly
- Protect location sharing information
- Follow WhatsApp's terms of service

## Troubleshooting

### Location Issues
- Enable browser location services
- Grant WhatsApp Web location permissions
- Check internet connection

### Audio Issues
- Verify ffmpeg installation
- Check file permissions
- Ensure audio device access

### Translation Issues
- Check internet connection
- Verify language codes
- Update googletrans package

## Dependencies

### Python Packages
- selenium: Web automation
- webdriver-manager: ChromeDriver management
- opencv-python: Video processing
- pygame: Audio playback
- pyttsx3: Text-to-speech
- schedule: Message scheduling
- googletrans: Translation services
- geopy: Location services
- And more in requirements.txt

### System Requirements
- Python 3.8+
- Chrome Browser
- FFmpeg
- espeak
- Internet Connection

## Contribution

Feel free to contribute to this project:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License


## Disclaimer

This tool is for educational purposes only. Users are responsible for how they use this tool and should comply with WhatsApp's terms of service.
