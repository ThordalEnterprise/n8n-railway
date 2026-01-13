"""
TikTok Auto Story Pipeline - FREE Open Source Configuration
Uses ONLY free and open source tools - zero monthly costs!

Copy this file to config.py and configure your Reddit API credentials
"""

# ==============================================
# CORE API KEYS (FREE)
# ==============================================

# Reddit API (100% FREE - get from reddit.com/prefs/apps)
REDDIT_CLIENT_ID = "your_14_char_id"
REDDIT_CLIENT_SECRET = "your_secret_key"
REDDIT_USER_AGENT = "TikTokStoryBot/1.0"

# ==============================================
# STORY GENERATION (Choose one FREE option)
# ==============================================

# Option A: Ollama (100% FREE - Local LLM) ⭐ RECOMMENDED
USE_OLLAMA = True
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama2"  # or "mistral", "codellama", "llama3"

# Option B: LM Studio (100% FREE - Alternative local LLM)
USE_LM_STUDIO = False
LM_STUDIO_URL = "http://localhost:1234"

# Option C: GPT4All (100% FREE - Lightweight local models)
USE_GPT4ALL = False
GPT4ALL_MODEL_PATH = "/path/to/model.bin"

# ==============================================
# TEXT-TO-SPEECH (100% FREE)
# ==============================================

# Option A: Coqui TTS (100% FREE - Best quality) ⭐ RECOMMENDED
USE_COQUI_TTS = True
COQUI_MODEL = "tts_models/en/ljspeech/tacotron2-DDC"
# Other good models:
# - tts_models/en/vctk/vits (multiple voices)
# - tts_models/en/ljspeech/glow-tts

# Option B: pyttsx3 (100% FREE - Offline, built-in voices)
USE_PYTTSX3 = False
PYTTSX3_VOICE = "english"  # Uses system voices

# Option C: eSpeak (100% FREE - Lightweight)
USE_ESPEAK = False

# ==============================================
# VIDEO GENERATION (100% FREE)
# ==============================================

# Option A: ComfyUI (100% FREE - Best quality) ⭐ RECOMMENDED
USE_COMFYUI = True
COMFYUI_URL = "http://localhost:8188"
# Requires GPU (12GB+ VRAM recommended)
# Models needed (all FREE from HuggingFace):
# - SDXL 1.0
# - AnimateDiff

# Option B: Stable Diffusion WebUI (100% FREE)
USE_SDWEBUI = False
SDWEBUI_URL = "http://localhost:7860"

# Option C: Text2Video-Zero (100% FREE - Lighter on GPU)
USE_TEXT2VIDEO = False
TEXT2VIDEO_URL = "http://localhost:7861"

# ==============================================
# VIDEO OUTPUT (100% FREE)
# ==============================================

# Local File Storage (100% FREE) ⭐ RECOMMENDED
LOCAL_OUTPUT_DIR = "/home/node/.n8n/videos"
# Videos saved to n8n volume - download manually or via n8n

# ==============================================
# SERVICE URLS
# ==============================================
# Update these after deploying FREE services to Railway/your server

STORY_SERVICE_URL = "http://localhost:8001"
VOICE_SERVICE_URL = "http://localhost:8002"
VIDEO_SERVICE_URL = "http://localhost:8003"
ASSEMBLY_SERVICE_URL = "http://localhost:8004"

# ==============================================
# STORY GENERATION SETTINGS
# ==============================================

STORY_CONFIG = {
    "length_seconds": 25,
    "style": "dark absurd small town",
    "universe": "snowy small town",
    "twist_level": "high",
    "subreddits": ["ShortStories", "creepypasta", "AskReddit", "nosleep", "LetsNotMeet"],
    "temperature": 0.8,
    "max_tokens": 500
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
    "subtitle_style": "modern",
    "subtitle_font": "Arial",
    "subtitle_color": "white",
    "subtitle_outline": "black"
}

# ==============================================
# VOICE SETTINGS
# ==============================================

VOICE_CONFIG = {
    "speed": 1.0,
    "pitch": 1.0,
    "add_background_music": False,
    "background_music_volume": 0.2,
    "normalize_audio": True
}

# ==============================================
# TIKTOK POST SETTINGS
# ==============================================

TIKTOK_CONFIG = {
    "hashtags": ["#story", "#shorts", "#mystical", "#darkstory", "#storytelling", "#creepy"],
    "add_hook_as_caption": True,
    "max_caption_length": 150
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

def get_active_llm_provider():
    """Returns the active LLM provider"""
    if USE_OLLAMA:
        return "ollama"
    elif USE_LM_STUDIO:
        return "lm_studio"
    elif USE_GPT4ALL:
        return "gpt4all"
    else:
        return "ollama"  # Default

def get_active_tts_provider():
    """Returns the active TTS provider"""
    if USE_COQUI_TTS:
        return "coqui"
    elif USE_PYTTSX3:
        return "pyttsx3"
    elif USE_ESPEAK:
        return "espeak"
    else:
        return "coqui"  # Default

def get_active_video_provider():
    """Returns the active video generation provider"""
    if USE_COMFYUI:
        return "comfyui"
    elif USE_SDWEBUI:
        return "sdwebui"
    elif USE_TEXT2VIDEO:
        return "text2video"
    else:
        return "comfyui"  # Default

def get_all_config():
    """Returns all config as a dictionary"""
    return {
        "reddit": {
            "client_id": REDDIT_CLIENT_ID,
            "client_secret": REDDIT_CLIENT_SECRET,
            "user_agent": REDDIT_USER_AGENT
        },
        "llm_provider": get_active_llm_provider(),
        "tts_provider": get_active_tts_provider(),
        "video_provider": get_active_video_provider(),
        "story": STORY_CONFIG,
        "video": VIDEO_CONFIG,
        "voice": VOICE_CONFIG,
        "tiktok": TIKTOK_CONFIG,
        "schedule": SCHEDULE_CONFIG,
        "services": {
            "story": STORY_SERVICE_URL,
            "voice": VOICE_SERVICE_URL,
            "video": VIDEO_SERVICE_URL,
            "assembly": ASSEMBLY_SERVICE_URL
        },
        "output_dir": LOCAL_OUTPUT_DIR
    }

# ==============================================
# VALIDATION
# ==============================================

def validate_config():
    """Validates that required settings are configured"""
    errors = []
    warnings = []
    
    # Reddit is the only required external API (and it's FREE!)
    if REDDIT_CLIENT_ID == "your_14_char_id":
        errors.append("⚠️  Reddit client ID not set")
        errors.append("    Get it FREE from: https://www.reddit.com/prefs/apps")
    
    # Check if at least one provider is enabled for each component
    if not (USE_OLLAMA or USE_LM_STUDIO or USE_GPT4ALL):
        warnings.append("💡 No LLM provider enabled - defaulting to Ollama")
    
    if not (USE_COQUI_TTS or USE_PYTTSX3 or USE_ESPEAK):
        warnings.append("💡 No TTS provider enabled - defaulting to Coqui TTS")
    
    if not (USE_COMFYUI or USE_SDWEBUI or USE_TEXT2VIDEO):
        warnings.append("💡 No video provider enabled - defaulting to ComfyUI")
    
    if errors:
        print("\n🔴 Configuration Errors:")
        for error in errors:
            print(error)
        print("\n👉 Edit config.py and add your Reddit API credentials\n")
        return False
    
    if warnings:
        print("\n💡 Configuration Warnings:")
        for warning in warnings:
            print(warning)
        print()
    
    print("✅ Configuration validated successfully!")
    print("\n💚 100% FREE Open Source Stack:")
    print(f"   ✓ LLM: {get_active_llm_provider()}")
    print(f"   ✓ TTS: {get_active_tts_provider()}")
    print(f"   ✓ Video: {get_active_video_provider()}")
    print(f"   ✓ Storage: Local")
    print(f"   ✓ Reddit: FREE API")
    print("\n💰 Monthly Cost: $0.00")
    print("🎉 You can generate unlimited videos for FREE!\n")
    
    return True

# ==============================================
# INSTALLATION HELPERS
# ==============================================

def print_installation_guide():
    """Prints installation instructions for free tools"""
    print("\n📦 Installation Guide for FREE Tools")
    print("=" * 50)
    
    print("\n1️⃣  Reddit API (100% FREE):")
    print("   → https://www.reddit.com/prefs/apps")
    print("   → Create app, select 'script', get Client ID & Secret")
    
    print("\n2️⃣  Ollama (Local LLM - FREE):")
    print("   → curl -fsSL https://ollama.ai/install.sh | sh")
    print("   → ollama pull llama2")
    print("   → ollama serve")
    
    print("\n3️⃣  Coqui TTS (Voice - FREE):")
    print("   → pip install TTS")
    print("   → tts --list_models")
    
    print("\n4️⃣  ComfyUI (Video - FREE):")
    print("   → git clone https://github.com/comfyanonymous/ComfyUI")
    print("   → cd ComfyUI && pip install -r requirements.txt")
    print("   → python main.py --listen 0.0.0.0 --port 8188")
    
    print("\n5️⃣  Download FREE models:")
    print("   → SDXL: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0")
    print("   → AnimateDiff: https://huggingface.co/guoyww/animatediff")
    
    print("\n💡 All tools are 100% free and open source!")
    print("=" * 50)

if __name__ == "__main__":
    # Test configuration
    print("🔧 TikTok Auto Story Pipeline - FREE Configuration")
    print("=" * 50)
    
    if validate_config():
        print_installation_guide()
    
    print("\n📊 Active Configuration:")
    import json
    print(json.dumps(get_all_config(), indent=2))
