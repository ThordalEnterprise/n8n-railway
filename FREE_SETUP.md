# 100% FREE Open Source TikTok Automation

This guide shows you how to run the entire TikTok automation pipeline using **ONLY free and open source tools**.

## 💚 The FREE Stack

| Component | Tool | Cost | GPU Needed |
|-----------|------|------|------------|
| Story Generation | OpenAI GPT-3.5 or **Ollama (Local)** | $0.12/month or **FREE** | No / Optional |
| Voice (TTS) | **Coqui TTS** | **FREE** | Optional (faster with GPU) |
| Video | **ComfyUI + AnimateDiff** | **FREE** | Yes (12GB+ VRAM) |
| Storage | **Local n8n Volume** | **FREE** | No |
| Orchestration | **n8n (Self-hosted)** | **FREE** | No |
| Database | **PostgreSQL (Railway)** | **FREE** | No |

**Total Monthly Cost: $0.12 (just OpenAI for stories) or $0 with local LLM!**

---

## 🚀 Quick Setup (3 Options)

### Option 1: Minimal Cost (~$0.12/month)

Use OpenAI for stories only, everything else is free:

```python
# config.py
OPENAI_API_KEY = "sk-proj-YOUR-KEY"  # Only cost: $0.002/story
REDDIT_CLIENT_ID = "your_id"  # FREE
USE_COQUI_TTS = True  # FREE
USE_COMFYUI = True  # FREE (needs GPU)
USE_LOCAL_STORAGE = True  # FREE
```

**Monthly cost for 60 videos: ~$0.12**

### Option 2: 100% FREE (Zero Cost)

Use local LLM for everything:

```python
# config.py
USE_LOCAL_LLM = True  # FREE
LOCAL_LLM_URL = "http://localhost:11434"  # Ollama
REDDIT_CLIENT_ID = "your_id"  # FREE
USE_COQUI_TTS = True  # FREE
USE_COMFYUI = True  # FREE (needs GPU)
USE_LOCAL_STORAGE = True  # FREE
```

**Monthly cost: $0.00**

### Option 3: Budget GPU-less Setup

No GPU? Use pyttsx3 for voice and pre-generated images:

```python
# config.py
OPENAI_API_KEY = "sk-proj-YOUR-KEY"  # $0.002/story
REDDIT_CLIENT_ID = "your_id"  # FREE
USE_PYTTSX3 = True  # FREE (offline, no GPU)
USE_LOCAL_STORAGE = True  # FREE
```

**Monthly cost for 60 videos: ~$0.12**

---

## 📦 Installation Guide

### 1. Install Free Tools

#### A. Coqui TTS (Free Voice Generation)

```bash
# Install Coqui TTS
pip install TTS

# Test it
tts --text "Hello world" --out_path output.wav

# List available voices
tts --list_models
```

**Best voices for storytelling:**
- `tts_models/en/ljspeech/tacotron2-DDC`
- `tts_models/en/vctk/vits` (multiple voices)

#### B. ComfyUI (Free Video Generation)

```bash
# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI

# Install dependencies
pip install -r requirements.txt

# Download models (AnimateDiff + SDXL)
# Place in: ComfyUI/models/

# Start ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

**Required models (all FREE):**
- SDXL 1.0: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
- AnimateDiff: https://huggingface.co/guoyww/animatediff

#### C. Ollama (Optional - Free Local LLM)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download a model
ollama pull llama2  # or mistral, codellama

# Start Ollama
ollama serve
```

#### D. Reddit API (Free)

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Select "script"
4. Get Client ID and Secret (100% FREE)

---

## 🎬 Deploy to Railway (Free Tier)

### What's FREE on Railway:

- $5 credit/month (enough for n8n + PostgreSQL)
- PostgreSQL database
- n8n instance
- Volume storage (1GB free)

### GPU Server Options:

ComfyUI needs GPU. Run it on:

**Option A: Your own PC/Mac with GPU**
- Free if you already have NVIDIA GPU (12GB+ VRAM)
- Expose via ngrok or CloudFlare Tunnel

**Option B: Vast.ai (Cheapest GPU rental)**
- ~$0.10-0.20/hour for RTX 3090
- Only run when generating videos
- ~$15/month if running 24/7

**Option C: RunPod (Good balance)**
- ~$0.30/hour for RTX 4090
- Spot instances even cheaper

### Setup:

1. **Deploy n8n to Railway** (covered in README.md)
2. **Run ComfyUI on GPU server** (local or Vast.ai)
3. **Update config.py:**

```python
COMFYUI_URL = "https://your-comfyui-url.ngrok.io"
# or
COMFYUI_URL = "http://your-vastai-instance:8188"
```

---

## 💰 Cost Breakdown

### 100% Free Setup (GPU at home):

```
Reddit API: FREE
Ollama (Local LLM): FREE
Coqui TTS: FREE
ComfyUI (Your GPU): FREE
n8n (Railway): FREE ($5 credit covers it)
PostgreSQL: FREE
Storage: FREE (1GB Railway volume)

Total: $0/month ✅
```

### Minimal Cost Setup (OpenAI + Home GPU):

```
Reddit API: FREE
OpenAI GPT-3.5: $0.12/month (60 stories)
Coqui TTS: FREE
ComfyUI (Your GPU): FREE
n8n (Railway): FREE
PostgreSQL: FREE
Storage: FREE

Total: $0.12/month ✅
```

### With Rented GPU (Vast.ai):

```
Reddit API: FREE
OpenAI GPT-3.5: $0.12/month
Coqui TTS: FREE
ComfyUI (Vast.ai RTX 3090): $15/month (24/7) or ~$5/month (on-demand)
n8n (Railway): FREE
PostgreSQL: FREE
Storage: FREE

Total: $5-15/month ✅
```

---

## 🔧 Configuration

Edit `config.py` for 100% free setup:

```python
# ==============================================
# 100% FREE CONFIGURATION
# ==============================================

# Story Generation (Choose one)
USE_LOCAL_LLM = True  # FREE
LOCAL_LLM_URL = "http://localhost:11434"
LOCAL_LLM_MODEL = "llama2"
# OR
OPENAI_API_KEY = "sk-proj-xxx"  # $0.002/story (GPT-3.5)

# Reddit (Always FREE)
REDDIT_CLIENT_ID = "your_id"
REDDIT_CLIENT_SECRET = "your_secret"

# Voice (100% FREE)
USE_COQUI_TTS = True
# Available voices:
# - tts_models/en/ljspeech/tacotron2-DDC (neutral)
# - tts_models/en/vctk/vits (multiple speakers)

# Video (100% FREE with GPU)
USE_COMFYUI = True
COMFYUI_URL = "http://localhost:8188"

# Storage (100% FREE)
USE_LOCAL_STORAGE = True
LOCAL_OUTPUT_DIR = "/home/node/.n8n/videos"
```

---

## 🎯 Quality Comparison

### Story Generation:

| Tool | Quality | Speed | Cost/Story |
|------|---------|-------|------------|
| GPT-4 | ⭐⭐⭐⭐⭐ | Fast | $0.03 |
| GPT-3.5 | ⭐⭐⭐⭐ | Fast | $0.002 |
| Llama2 (70B) | ⭐⭐⭐⭐ | Medium | FREE |
| Mistral (7B) | ⭐⭐⭐ | Fast | FREE |

### Voice (TTS):

| Tool | Quality | Speed | Cost/Video |
|------|---------|-------|------------|
| ElevenLabs | ⭐⭐⭐⭐⭐ | Fast | $0.02 |
| OpenAI TTS | ⭐⭐⭐⭐ | Fast | $0.004 |
| Coqui TTS | ⭐⭐⭐⭐ | Medium | FREE |
| pyttsx3 | ⭐⭐ | Fast | FREE |

### Video Generation:

| Tool | Quality | Speed | Cost/Video |
|------|---------|-------|------------|
| Replicate | ⭐⭐⭐⭐ | Fast | $0.50 |
| ComfyUI (RTX 4090) | ⭐⭐⭐⭐ | Fast | FREE |
| ComfyUI (RTX 3060) | ⭐⭐⭐⭐ | Slow | FREE |

---

## 🚀 Recommended Free Setup

**Best balance of quality and cost:**

```python
# config.py
OPENAI_API_KEY = "sk-proj-xxx"  # GPT-3.5 for stories ($0.002 each)
REDDIT_CLIENT_ID = "your_id"    # FREE
USE_COQUI_TTS = True             # FREE (good quality)
USE_COMFYUI = True               # FREE (excellent quality)
COMFYUI_URL = "http://localhost:8188"  # Your GPU or Vast.ai
USE_LOCAL_STORAGE = True         # FREE

STORY_CONFIG = {
    "gpt_model": "gpt-3.5-turbo",  # Cheap and good enough
}
```

**Result:**
- 60 videos/month
- High quality output
- Total cost: $0.12/month (or $0 with Ollama)

---

## 🛠️ Troubleshooting

### Coqui TTS Issues:

```bash
# If installation fails
pip install TTS --no-deps
pip install torch torchaudio

# List available models
tts --list_models

# Test voice generation
tts --model_name "tts_models/en/ljspeech/tacotron2-DDC" \
    --text "This is a test" \
    --out_path test.wav
```

### ComfyUI Issues:

```bash
# CUDA out of memory
# Solution: Use smaller models or reduce batch size

# Models not found
# Solution: Check models are in correct folders:
# - ComfyUI/models/checkpoints/ (SDXL)
# - ComfyUI/models/animatediff/ (AnimateDiff)
```

### Ollama Issues:

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Pull a model
ollama pull llama2

# Test generation
ollama run llama2 "Write a short horror story"
```

---

## 📊 Performance Expectations

With free tools:

- **Story generation:** 5-10 seconds (GPT-3.5) or 30-60s (Ollama)
- **Voice generation:** 10-30 seconds (Coqui TTS)
- **Video generation:** 2-5 minutes (ComfyUI with RTX 3090)
- **Total per video:** 3-7 minutes

**You can generate 200+ videos/month for FREE!**

---

## ✅ Next Steps

1. ✅ Get Reddit API credentials (FREE)
2. ✅ Install Coqui TTS (FREE)
3. ✅ Set up ComfyUI with GPU (FREE if you have GPU)
4. ✅ Optional: Install Ollama for 100% free stories
5. ✅ Update `config.py` with free tools
6. ✅ Deploy n8n to Railway (FREE tier)
7. ✅ Run the workflow and enjoy FREE content! 🎉

---

**Questions?** Check the main [README.md](README.md) or [CREDENTIALS.md](CREDENTIALS.md)
