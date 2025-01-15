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

### Prerequisites
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-pip python3-tk ffmpeg espeak

# For MacOS
brew install python3 ffmpeg espeak

# For Windows
# Install Python 3.8+ from python.org
# Install ffmpeg from ffmpeg.org
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Start the tool:
```bash
python old.py
```

2. Follow the GUI prompts:
   - Click "Start the tool"
   - Scan QR code if needed
   - Click "I am now logged in"
   - Choose desired feature from menu

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

This project is licensed under the MIT License.

## Disclaimer

This tool is for educational purposes only. Users are responsible for how they use this tool and should comply with WhatsApp's terms of service.
