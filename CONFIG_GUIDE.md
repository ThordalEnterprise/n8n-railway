# Quick Config Setup Guide

This project uses a simple `config.py` file for all API keys and settings - perfect for private use!

## Setup (3 steps)

### 1. Copy config template

```bash
cp config.example.py config.py
```

### 2. Edit config.py with your API keys

```bash
nano config.py  # or use any editor
```

### 3. Fill in your keys

```python
# Minimum required:
OPENAI_API_KEY = "sk-proj-YOUR-ACTUAL-KEY"
REDDIT_CLIENT_ID = "your_actual_id"
REDDIT_CLIENT_SECRET = "your_actual_secret"

# Choose TTS provider:
ELEVENLABS_API_KEY = "your_actual_key"  # Best quality
# OR
USE_OPENAI_TTS = True  # Cheaper option

# Choose video provider:
REPLICATE_API_TOKEN = "r8_YOUR-ACTUAL-TOKEN"  # Easiest
# OR
USE_RUNPOD = True
RUNPOD_API_KEY = "your_actual_key"
```

## Test Config

```bash
python config.py
```

Should show:
```
✅ Configuration validated successfully!
📊 Active providers:
  TTS: elevenlabs
  Video: replicate
  Upload: s3
```

## Update Service URLs

After deploying to Railway, update these:

```python
STORY_SERVICE_URL = "https://story-service.up.railway.app"
VOICE_SERVICE_URL = "https://voice-service.up.railway.app"
VIDEO_SERVICE_URL = "https://video-service.up.railway.app"
ASSEMBLY_SERVICE_URL = "https://assembly-service.up.railway.app"
```

## Settings You Can Change

### Story Style
```python
STORY_CONFIG = {
    "style": "dark absurd small town",  # Your preferred style
    "universe": "snowy small town",      # Setting
    "twist_level": "high",               # low/medium/high
    "subreddits": ["ShortStories", "creepypasta"],  # Reddit sources
    "gpt_model": "gpt-4",                # or "gpt-3.5-turbo" (cheaper)
}
```

### Video Settings
```python
VIDEO_CONFIG = {
    "num_clips": 5,           # Number of video clips
    "clip_duration": 5,       # Seconds per clip
    "add_subtitles": True,    # Auto-generate subtitles
}
```

### Schedule
```python
SCHEDULE_CONFIG = {
    "times": ["10:00", "18:00"],  # Post times
    "timezone": "Europe/Copenhagen"
}
```

### TikTok Hashtags
```python
TIKTOK_CONFIG = {
    "hashtags": ["#story", "#mystical", "#darkstory"],
    "privacy_level": "public",  # or "private"
}
```

## Security Note

⚠️ **config.py is in .gitignore** - it won't be committed to GitHub

But since this is a private repo, you can safely:
- Hardcode all keys
- No need for environment variables
- Just edit config.py directly

## Where to Get API Keys

Quick links (see CREDENTIALS.md for details):

- **OpenAI**: https://platform.openai.com/api-keys
- **Reddit**: https://www.reddit.com/prefs/apps
- **ElevenLabs**: https://elevenlabs.io (Profile → API Keys)
- **Replicate**: https://replicate.com/account/api-tokens
- **RunPod**: https://runpod.io/console/user/settings

## Cost Estimate

With default settings (2 videos/day):

- OpenAI GPT-4: ~$1.80/month
- OpenAI TTS: ~$0.24/month
- Replicate video: ~$30/month
- **Total: ~$32/month**

Cheaper option (GPT-3.5 + OpenAI TTS):
- ~$6/month for 60 videos

## Next Steps

1. ✅ Copy config.example.py → config.py
2. ✅ Add your API keys
3. ✅ Test with `python config.py`
4. ✅ Deploy services to Railway
5. ✅ Update service URLs in config.py
6. ✅ Import workflow to n8n
7. ✅ Activate and enjoy! 🎉

---

**Need help?** Check [CREDENTIALS.md](CREDENTIALS.md) for detailed API key instructions.
