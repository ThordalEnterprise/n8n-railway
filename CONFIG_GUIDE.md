# 100% FREE Configuration Guide

This project uses **ONLY free and open source tools** - zero monthly costs!

## Quick Setup (2 steps)

### 1. Copy config template

```bash
cp config.example.py config.py
```

### 2. Add Reddit API credentials (FREE)

```bash
nano config.py  # or use any editor
```

Fill in:
```python
REDDIT_CLIENT_ID = "your_14_char_id"      # Get from reddit.com/prefs/apps
REDDIT_CLIENT_SECRET = "your_secret"       # 100% FREE
REDDIT_USER_AGENT = "TikTokStoryBot/1.0"
```

**That's it! Everything else is already configured for FREE tools.**

---

## 💚 The FREE Stack (Default Configuration)

| Component | Tool | Cost |
|-----------|------|------|
| Stories | **Ollama (Llama2)** | FREE |
| Voice | **Coqui TTS** | FREE |
| Video | **ComfyUI** | FREE |
| Storage | **Local** | FREE |
| API | **Reddit** | FREE |

**Monthly Cost: $0.00** ✅

---

## Installation

### 1. Reddit API (Required - FREE)

```bash
# Go to: https://www.reddit.com/prefs/apps
# Click "Create App"
# Select "script"
# Copy Client ID and Secret
```

### 2. Ollama (Stories - FREE)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download Llama2 model
ollama pull llama2

# Start Ollama
ollama serve
```

### 3. Coqui TTS (Voice - FREE)

```bash
# Install Coqui TTS
pip install TTS

# List available voices
tts --list_models

# Test it
tts --text "Hello world" --out_path test.wav
```

### 4. ComfyUI (Video - FREE)

```bash
# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI

# Install dependencies
pip install -r requirements.txt

# Start ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

### 5. Download FREE Models

```bash
# SDXL 1.0 (FREE from HuggingFace)
# → https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0

# AnimateDiff (FREE)
# → https://huggingface.co/guoyww/animatediff

# Place in: ComfyUI/models/
```

---

## Test Configuration

```bash
python config.py
```

Expected output:
```
✅ Configuration validated successfully!

💚 100% FREE Open Source Stack:
   ✓ LLM: ollama
   ✓ TTS: coqui
   ✓ Video: comfyui
   ✓ Storage: Local
   ✓ Reddit: FREE API

💰 Monthly Cost: $0.00
🎉 You can generate unlimited videos for FREE!
```

---

## Customize Settings

All settings in `config.py`:

### Story Style
```python
STORY_CONFIG = {
    "style": "dark absurd small town",
    "universe": "snowy small town",
    "twist_level": "high",
    "subreddits": ["ShortStories", "creepypasta", "AskReddit"],
}
```

### Video Format
```python
VIDEO_CONFIG = {
    "num_clips": 5,
    "clip_duration": 5,
    "add_subtitles": True,
    "subtitle_style": "modern",
}
```

### Schedule
```python
SCHEDULE_CONFIG = {
    "times": ["10:00", "18:00"],
    "timezone": "Europe/Copenhagen"
}
```

### Hashtags
```python
TIKTOK_CONFIG = {
    "hashtags": ["#story", "#mystical", "#darkstory"],
}
```

---

## Alternative FREE Tools

### LLM (Stories)
```python
# Option A: Ollama (Recommended)
USE_OLLAMA = True
OLLAMA_MODEL = "llama2"  # or "mistral", "llama3"

# Option B: LM Studio
USE_LM_STUDIO = True
LM_STUDIO_URL = "http://localhost:1234"

# Option C: GPT4All
USE_GPT4ALL = True
```

### TTS (Voice)
```python
# Option A: Coqui TTS (Recommended - best quality)
USE_COQUI_TTS = True

# Option B: pyttsx3 (Built-in voices, no GPU)
USE_PYTTSX3 = True

# Option C: eSpeak (Lightweight)
USE_ESPEAK = True
```

### Video
```python
# Option A: ComfyUI (Recommended - best quality)
USE_COMFYUI = True

# Option B: Stable Diffusion WebUI
USE_SDWEBUI = True

# Option C: Text2Video-Zero (Lighter on GPU)
USE_TEXT2VIDEO = True
```

---

## GPU Requirements

### Minimum (RTX 3060 12GB)
- Generate videos slower (~5-10 min/video)
- Works fine for 2-4 videos/day

### Recommended (RTX 3090/4090)
- Fast generation (~2-3 min/video)
- Can handle 10+ videos/day

### No GPU?
- Use pyttsx3 for voice (no GPU needed)
- Rent GPU on-demand from Vast.ai (~$0.10-0.20/hour)

---

## Performance

With FREE tools on RTX 3090:

- **Story generation:** 30-60 seconds (Ollama Llama2)
- **Voice generation:** 10-30 seconds (Coqui TTS)
- **Video generation:** 2-5 minutes (ComfyUI)
- **Total:** ~3-7 minutes per video

**You can generate 200+ videos/month for FREE!**

---

## Update Service URLs

After deploying to Railway:

```python
STORY_SERVICE_URL = "https://story-service.up.railway.app"
VOICE_SERVICE_URL = "https://voice-service.up.railway.app"
VIDEO_SERVICE_URL = "https://video-service.up.railway.app"
ASSEMBLY_SERVICE_URL = "https://assembly-service.up.railway.app"
```

---

## Troubleshooting

### Ollama not starting
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

### Coqui TTS errors
```bash
# Reinstall
pip uninstall TTS
pip install TTS --no-cache-dir

# Test specific model
tts --model_name "tts_models/en/ljspeech/tacotron2-DDC" \
    --text "Test" --out_path test.wav
```

### ComfyUI CUDA errors
```bash
# Check GPU
nvidia-smi

# Reduce batch size in ComfyUI
# Or use smaller models
```

---

## Security

✅ **config.py is in .gitignore** - won't be committed

Since everything is FREE and open source:
- No API keys to protect (except Reddit, which is free)
- All models run locally
- Complete control over your data

---

## Next Steps

1. ✅ Get Reddit API credentials (FREE - 2 minutes)
2. ✅ Install Ollama (FREE - 5 minutes)
3. ✅ Install Coqui TTS (FREE - 2 minutes)
4. ✅ Install ComfyUI (FREE - 10 minutes)
5. ✅ Download models (FREE - 30 minutes)
6. ✅ Run `python config.py` to test
7. ✅ Deploy to Railway and enjoy! 🎉

**Total setup time: ~1 hour**  
**Monthly cost: $0.00**  
**Unlimited videos: ✅**

---

Need help? Check [FREE_SETUP.md](FREE_SETUP.md) for detailed guides.
