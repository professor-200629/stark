# STARK — AI Assistant / AI Operating System

> **S**elf-**T**hinking **A**utonomous **R**eal-time **K**nowledge system

STARK is a voice-first, real-time personal AI assistant and operating system designed to run locally on your machine — **no API keys required**. It watches your screen, understands your voice, monitors through your camera, manages your files, controls your browser, attends meetings with you, and learns your habits over time.

---

## Features

| Category | Capabilities |
|---|---|
| **Voice & Presence** | Greets you by time of day, detects mood from voice, health reminders (water, rest breaks) |
| **Camera Vision** | Live face detection, emotion recognition, object detection — fully automatic, no button presses |
| **Screen Monitor** | Real-time OCR screen reading; say "read the paragraph" and STARK reads it aloud |
| **Code Assistant** | Watches your code editor, detects errors, generates and edits code on demand |
| **Meeting Assistant** | Silently displays answers on screen during Zoom/online meetings so you can read without speaking |
| **Browser Control** | Opens YouTube, Spotify, Netflix, Prime Video, JioHotstar; controls playback, skips ads |
| **File Management** | Navigate, create, move, delete files and folders by voice |
| **Communication** | Sends WhatsApp messages and makes calls via voice command |
| **Memory** | Remembers your habits, preferences, schedule, and goals across sessions |
| **Health Reminders** | Reminds you to drink water, take breaks, and rest after long work sessions |
| **App Control** | Opens and closes applications on your system |

---

## Requirements

- Python 3.8 or higher
- Windows (recommended; some features like app paths are Windows-specific)
- Microphone (optional — keyboard fallback is available)
- Webcam (optional — camera features require `opencv-python`)
- Tesseract OCR (optional — required for screen reading)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/professor-200629/stark.git
cd stark
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Windows PyAudio fix:** If `pyaudio` fails to install, run:
> ```bash
> pip install pipwin && pipwin install pyaudio
> ```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
CONTACT_MUMMY=+91XXXXXXXXXX
CONTACT_DAD=+91XXXXXXXXXX
CONTACT_FRIEND=+91XXXXXXXXXX

# Optional — leave empty to use STARK's built-in brain
GEMINI_API_KEY=
OPENAI_API_KEY=
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 5. (Optional) Install Tesseract OCR

- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki and install to `C:\Program Files\Tesseract-OCR\`
- **Linux:** `sudo apt install tesseract-ocr`
- **macOS:** `brew install tesseract`

STARK auto-detects the `tesseract` binary using `shutil.which`.

---

## Usage

```bash
python main.py
```

STARK will greet you, start all subsystems, and begin listening. Speak naturally — you don't need a wake word.

### Example commands

| You say | STARK does |
|---|---|
| `"What time is it?"` | Tells you the current time |
| `"Play Animal trailer in Telugu on YouTube"` | Searches and plays on YouTube |
| `"Skip ad"` | Skips the current YouTube advertisement |
| `"Pause"` | Pauses video playback |
| `"Open Spotify"` | Opens Spotify |
| `"Message mummy hello"` | Sends a WhatsApp message to your mum's number |
| `"What do you see?"` | Describes what the camera sees |
| `"Read the screen"` | Reads on-screen text aloud |
| `"Check my code for errors"` | Analyses the code in your editor |
| `"Start meeting mode"` | Activates silent meeting answer display |
| `"Shutdown"` | Gracefully shuts STARK down |

---

## Architecture

```
stark/
├── main.py               # Entry point — STARK class, command dispatcher
├── config.py             # All configuration (loads from .env)
├── voice_engine.py       # Text-to-speech (pyttsx3)
├── listener.py           # Voice and keyboard input
├── own_brain.py          # Local AI reasoning engine
├── code_brain.py         # Code analysis and generation
├── camera_vision.py      # Live camera — face, emotion, object detection
├── screen_monitor.py     # Real-time screen OCR
├── browser_controller.py # Browser and media control
├── app_controller.py     # Application launcher
├── file_explorer.py      # File system management
├── code_editor.py        # Code editor integration
├── communication.py      # WhatsApp / messaging
├── meeting_assistant.py  # Silent on-screen meeting helper
├── memory_manager.py     # Persistent memory across sessions
├── knowledge_engine.py   # Knowledge base queries
├── utils.py              # Shared utilities
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── .gitignore
```

---

## Security Notes

- **Never hardcode phone numbers, API keys, or passwords** in source files.
- All secrets must be stored in `.env` (which is git-ignored).
- See `.env.example` for the required variable names.

---

## License

This project is personal software. All rights reserved by the author.
