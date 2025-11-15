# LG WebOS TV Remote Control

A simple Python application to control your LG WebOS TV from the command line.

## Features

- 🎮 **Volume Control**: Adjust volume, mute/unmute
- 📺 **Channel Control**: Change channels up/down
- ⬆️ **Navigation**: Arrow keys, OK, Back, Home
- ▶️ **Media Control**: Play/Pause
- 📱 **App Launcher**: Launch popular apps (Netflix, YouTube, Disney+, etc.)
- 💬 **Notifications**: Send notifications to TV screen
- 🔍 **Auto Discovery**: Automatically finds TVs on your network

## Requirements

- Python 3.6+
- LG WebOS TV (connected to the same network)
- `pywebostv` library

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install pywebostv
```

## Usage

1. Make sure your TV is turned on and connected to the same network
2. Run the application:
```bash
python main.py
```

3. On first run, you'll see a pairing prompt on your TV screen - select "YES" to allow the connection
4. Once connected, you can use the following commands:

### Available Commands

**Volume:**
- `vol+` - Increase volume
- `vol-` - Decrease volume
- `mute` - Mute/unmute
- `vol:50` - Set volume to specific level (0-100)

**Navigation:**
- `up`, `down`, `left`, `right` - Arrow keys
- `ok` - OK/Select button
- `back` - Back button
- `home` - Home button

**Media:**
- `play` - Play
- `pause` - Pause

**Channels:**
- `ch+` - Channel up
- `ch-` - Channel down

**Apps:**
- `app:netflix` - Launch Netflix
- `app:youtube` - Launch YouTube
- `app:disney` - Launch Disney+
- `app:prime` - Launch Amazon Prime
- `app:spotify` - Launch Spotify

**Notifications:**
- `notify:Your Message` - Send notification to TV

**Exit:**
- `exit`, `quit`, or `q` - Exit the application

## Project Structure

- `main.py` - Main application entry point
- `tv_remote.py` - TVRemote class with all control methods
- `find_devices.py` - TV discovery functionality
- `tv_pairing.json` - Stores pairing information (created automatically)

## Notes

- The pairing information is saved in `tv_pairing.json` - you only need to pair once
- Make sure your TV and computer are on the same Wi-Fi network
- The TV must be powered on for the connection to work

