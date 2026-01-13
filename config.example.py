"""
TikTok Auto Story Pipeline - Configuration Template
Copy this file to config.py and fill in your API keys
"""

# ==============================================
# CORE API KEYS
# ==============================================

# OpenAI API (Required for story generation)
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"

# Reddit API (Required for story seeds)
REDDIT_CLIENT_ID = "your_14_char_id"
REDDIT_CLIENT_SECRET = "your_secret_key"
REDDIT_USER_AGENT = "TikTokStoryBot/1.0"

# ==============================================
# TEXT-TO-SPEECH (Choose one)
# ==============================================

# Option A: ElevenLabs (Best quality)
ELEVENLABS_API_KEY = "your_elevenlabs_key"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Default neutral voice

# Option B: OpenAI TTS (uses OPENAI_API_KEY above)
USE_OPENAI_TTS = False  # Set to True to use OpenAI TTS instead

# Option C: Coqui TTS (Self-hosted, no key needed)
USE_COQUI_TTS = False

# ==============================================
# VIDEO GENERATION (Choose one)
# ==============================================

# Option A: RunPod
RUNPOD_API_KEY = "your_runpod_key"
RUNPOD_ENDPOINT_ID = "your_endpoint_id"
USE_RUNPOD = False

# Option B: Replicate (Easiest to start)
REPLICATE_API_TOKEN = "r8_xxxxxxxxxxxxxxxxxxxxx"
USE_REPLICATE = True  # Default

# Option C: Self-hosted ComfyUI
COMFYUI_URL = "http://localhost:8188"
USE_COMFYUI = False

# ==============================================
# TIKTOK UPLOAD (Choose one)
# ==============================================

# Option A: TikTok API (Requires approval)
TIKTOK_CLIENT_KEY = "your_client_key"
TIKTOK_CLIENT_SECRET = "your_client_secret"
TIKTOK_ACCESS_TOKEN = "your_access_token"
USE_TIKTOK_API = False

# Option B: AWS S3 (For manual download)
AWS_ACCESS_KEY_ID = "your_access_key"
AWS_SECRET_ACCESS_KEY = "your_secret_key"
AWS_S3_BUCKET = "tiktok-videos"
AWS_REGION = "eu-west-1"
USE_S3_UPLOAD = True  # Default - manual upload

# Option C: Cloudflare R2 (Cheaper than S3)
R2_ACCESS_KEY_ID = "your_access_key"
R2_SECRET_ACCESS_KEY = "your_secret_key"
R2_BUCKET_NAME = "tiktok-videos"
R2_ACCOUNT_ID = "your_account_id"
USE_R2_UPLOAD = False

# ==============================================
# RAILWAY SERVICE URLS
# ==============================================
# Update these after deploying services to Railway

STORY_SERVICE_URL = "http://localhost:8001"  # Change to Railway URL
VOICE_SERVICE_URL = "http://localhost:8002"  # Change to Railway URL
VIDEO_SERVICE_URL = "http://localhost:8003"  # Change to Railway URL
ASSEMBLY_SERVICE_URL = "http://localhost:8004"  # Change to Railway URL
TIKTOK_UPLOAD_SERVICE_URL = "http://localhost:8005"  # Change to Railway URL

# ==============================================
# STORY GENERATION SETTINGS
# ==============================================

STORY_CONFIG = {
    "length_seconds": 25,
    "style": "dark absurd small town",
    "universe": "snowy small town",
    "twist_level": "high",
    "subreddits": ["ShortStories", "creepypasta", "AskReddit", "nosleep"],
    "gpt_model": "gpt-4",  # or "gpt-3.5-turbo" for cheaper
    "temperature": 0.8
}

# ==============================================
# VIDEO SETTINGS
# ==============================================

VIDEO_CONFIG = {
    "num_clips": 5,
    "clip_duration": 5,
    "aspect_ratio": [9, 16],  # TikTok format
    "fps": 24,
    "resolution": [1080, 1920],  # 1080x1920 for TikTok
    "add_subtitles": True,
    "subtitle_style": "modern"
}

# ==============================================
# VOICE SETTINGS
# ==============================================

VOICE_CONFIG = {
    "voice": "neutral_us",  # or specific ElevenLabs voice ID
    "speed": 1.0,
    "pitch": 1.0,
    "add_background_music": False,
    "background_music_volume": 0.2
}

# ==============================================
# TIKTOK POST SETTINGS
# ==============================================

TIKTOK_CONFIG = {
    "privacy_level": "public",  # or "private", "friends"
    "hashtags": ["#story", "#shorts", "#mystical", "#darkstory", "#storytelling"],
    "add_hook_as_caption": True,
    "allow_comments": True,
    "allow_duet": True,
    "allow_stitch": True
}

# ==============================================
# SCHEDULE SETTINGS
# ==============================================

SCHEDULE_CONFIG = {
    "enabled": True,
    "times": ["10:00", "18:00"],  # Post at 10 AM and 6 PM
    "timezone": "Europe/Copenhagen"
}

# ==============================================
# HELPER FUNCTIONS
# ==============================================

def get_active_tts_provider():
    """Returns the active TTS provider"""
    if USE_OPENAI_TTS:
        return "openai"
    elif USE_COQUI_TTS:
        return "coqui"
    else:
        return "elevenlabs"

def get_active_video_provider():
    """Returns the active video generation provider"""
    if USE_RUNPOD:
        return "runpod"
    elif USE_COMFYUI:
        return "comfyui"
    else:
        return "replicate"

def get_active_upload_provider():
    """Returns the active upload provider"""
    if USE_TIKTOK_API:
        return "tiktok"
    elif USE_R2_UPLOAD:
        return "r2"
    else:
        return "s3"

def get_all_config():
    """Returns all config as a dictionary"""
    return {
        "openai_key": OPENAI_API_KEY,
        "reddit": {
            "client_id": REDDIT_CLIENT_ID,
            "client_secret": REDDIT_CLIENT_SECRET,
            "user_agent": REDDIT_USER_AGENT
        },
        "tts_provider": get_active_tts_provider(),
        "video_provider": get_active_video_provider(),
        "upload_provider": get_active_upload_provider(),
        "story": STORY_CONFIG,
        "video": VIDEO_CONFIG,
        "voice": VOICE_CONFIG,
        "tiktok": TIKTOK_CONFIG,
        "schedule": SCHEDULE_CONFIG,
        "services": {
            "story": STORY_SERVICE_URL,
            "voice": VOICE_SERVICE_URL,
            "video": VIDEO_SERVICE_URL,
            "assembly": ASSEMBLY_SERVICE_URL,
            "upload": TIKTOK_UPLOAD_SERVICE_URL
        }
    }

# ==============================================
# VALIDATION
# ==============================================

def validate_config():
    """Validates that required keys are set"""
    errors = []
    
    if OPENAI_API_KEY == "sk-proj-xxxxxxxxxxxxxxxxxxxxx":
        errors.append("⚠️  OpenAI API key not set")
    
    if REDDIT_CLIENT_ID == "your_14_char_id":
        errors.append("⚠️  Reddit client ID not set")
    
    if get_active_tts_provider() == "elevenlabs" and ELEVENLABS_API_KEY == "your_elevenlabs_key":
        errors.append("⚠️  ElevenLabs API key not set")
    
    if get_active_video_provider() == "replicate" and REPLICATE_API_TOKEN == "r8_xxxxxxxxxxxxxxxxxxxxx":
        errors.append("⚠️  Replicate API token not set")
    
    if errors:
        print("\n🔴 Configuration Errors:")
        for error in errors:
            print(error)
        print("\n👉 Edit config.py and add your API keys\n")
        return False
    
    print("✅ Configuration validated successfully!")
    return True

if __name__ == "__main__":
    # Test configuration
    print("🔧 TikTok Auto Story Pipeline - Configuration")
    print("=" * 50)
    validate_config()
    print("\n📊 Active providers:")
    print(f"  TTS: {get_active_tts_provider()}")
    print(f"  Video: {get_active_video_provider()}")
    print(f"  Upload: {get_active_upload_provider()}")
