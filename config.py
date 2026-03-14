"""
STARK AI Assistant - Configuration
NO API KEYS NEEDED - STARK has its own brain
"""

import os

# ============================================
# USER PROFILE
# ============================================
USER_NAME = "Sir"
ASSISTANT_NAME = "STARK"

# ============================================
# CONTACTS
# ============================================
CONTACTS = {
    "mummy": "+918309351685",
    "mom": "+918309351685",
    "mother": "+918309351685",
    "whatsapp": "+918309351685",
    # Add more contacts here
    "dad": "+91XXXXXXXXXX",
    "father": "+91XXXXXXXXXX",
    "friend": "+91XXXXXXXXXX",
}

# ============================================
# PATHS
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "stark_memory.json")
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "knowledge_base.json")

# Tesseract OCR path (for screen reading)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ============================================
# BRAIN SETTINGS
# ============================================
# STARK works WITHOUT any API keys
# Uses local processing and intelligent responses
BRAIN_MODE = "local"  # "local" = no API needed

# ============================================
# VOICE SETTINGS
# ============================================
VOICE_RATE = 175
VOICE_VOLUME = 1.0
VOICE_INDEX = 0  # Change to select different voice

# ============================================
# CAMERA SETTINGS
# ============================================
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_ANALYSIS_INTERVAL = 3  # Seconds between auto-analysis

# ============================================
# SCREEN MONITOR SETTINGS
# ============================================
SCREEN_MONITOR_INTERVAL = 2  # Seconds between screen checks
SCREEN_LANGUAGE = "eng"  # OCR language

# ============================================
# BROWSER SETTINGS
# ============================================
CHROME_PROFILE_PATH = os.path.expanduser(
    r"~\AppData\Local\Google\Chrome\User Data"
)
CHROME_PROFILE_NAME = "Default"

# ============================================
# APP PATHS - Windows
# ============================================
APP_PATHS = {
    "whatsapp": "whatsapp://",
    "telegram": "telegram://",
    "spotify": "spotify://",
    "netflix": "https://www.netflix.com",
    "prime": "https://www.primevideo.com",
    "hotstar": "https://www.hotstar.com",
    "jiohotstar": "https://www.hotstar.com",
    "youtube": "https://www.youtube.com",
}

# ============================================
# MEETING ASSISTANT
# ============================================
MEETING_ANSWER_DISPLAY_TIME = 30  # Seconds to show answer on screen

# ============================================
# WORK HEALTH REMINDERS
# ============================================
WORK_REMINDER_INTERVAL = 2700  # 45 minutes in seconds
WATER_REMINDER_INTERVAL = 3600  # 60 minutes in seconds

# ============================================
# GEMINI API (OPTIONAL - Only if you want to use)
# ============================================
# Leave empty to use STARK's built-in brain
GEMINI_API_KEY = ""  # Put your Gemini API key here if you want to use Gemini AI
OPENAI_API_KEY = ""  # Put your OpenAI API key here if you want to use GPT