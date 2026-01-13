# FREE TikTok Automation Services

All services use 100% FREE and open source tools - zero monthly costs!

## Services

### 1. Story Service (Port 8001)
**Technology:** Ollama + Reddit API  
**Cost:** FREE  

Generates unique stories from Reddit seeds using local LLM.

```bash
cd story-service
pip install -r requirements.txt
python main.py
```

**Endpoints:**
- `POST /generate-story` - Generate story
- `GET /health` - Health check
- `GET /test` - Quick test

### 2. Voice Service (Port 8002)
**Technology:** Coqui TTS  
**Cost:** FREE  

Converts story text to voice using open source TTS.

```bash
cd voice-service
pip install -r requirements.txt
python main.py
```

**Endpoints:**
- `POST /generate-voice` - Generate voice
- `GET /download/{filename}` - Download audio
- `GET /models` - List available voices
- `POST /test` - Quick test

### 3. Video Service (Port 8003)
**Technology:** ComfyUI + AnimateDiff  
**Cost:** FREE (needs GPU)  

Generates video clips from visual prompts.

```bash
cd video-service
pip install -r requirements.txt
python main.py
```

**Requirements:**
- ComfyUI running on port 8188
- SDXL + AnimateDiff models installed

**Endpoints:**
- `POST /generate-video` - Generate video clips
- `GET /health` - Health check
- `POST /test` - Quick test

### 4. Assembly Service (Port 8004)
**Technology:** FFmpeg  
**Cost:** FREE  

Assembles final video with audio and subtitles.

```bash
cd assembly-service
pip install -r requirements.txt
python main.py
```

**Endpoints:**
- `POST /assemble-video` - Assemble final video
- `GET /download/{video_id}` - Download video
- `DELETE /cleanup` - Clean up old files

---

## Quick Start (Local Development)

### 1. Install Prerequisites

```bash
# Ollama (for stories)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2
ollama serve

# Coqui TTS (for voice)
pip install TTS

# ComfyUI (for video)
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI && pip install -r requirements.txt
python main.py --listen 0.0.0.0 --port 8188

# FFmpeg (for assembly)
# macOS: brew install ffmpeg
# Ubuntu: apt-get install ffmpeg
```

### 2. Get Reddit API Credentials (FREE)

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Select "script"
4. Copy Client ID and Secret

### 3. Configure Services

```bash
# Set environment variables
export REDDIT_CLIENT_ID="your_id"
export REDDIT_CLIENT_SECRET="your_secret"
export OLLAMA_URL="http://localhost:11434"
export COMFYUI_URL="http://localhost:8188"
```

### 4. Start All Services

```bash
# Terminal 1: Story Service
cd story-service && python main.py

# Terminal 2: Voice Service
cd voice-service && python main.py

# Terminal 3: Video Service
cd video-service && python main.py

# Terminal 4: Assembly Service
cd assembly-service && python main.py
```

### 5. Test Services

```bash
# Test story generation
curl -X POST http://localhost:8001/generate-story \
  -H "Content-Type: application/json" \
  -d '{"subreddits": ["ShortStories"]}'

# Test voice generation
curl -X POST http://localhost:8002/generate-voice \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test"}'

# Test video generation
curl -X POST http://localhost:8003/generate-video \
  -H "Content-Type: application/json" \
  -d '{"visual_prompt": "Snowy town, dark, mysterious"}'
```

---

## Deploy to Railway

### Option 1: Story, Voice, and Assembly Services

These can run on Railway's free tier (no GPU needed):

1. Create new Railway service
2. Connect GitHub repo
3. Set root directory to `services/story-service`
4. Add environment variables:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `OLLAMA_URL` (point to your Ollama server)
5. Deploy

Repeat for `voice-service` and `assembly-service`.

### Option 2: Video Service (ComfyUI)

Needs GPU - run on your own hardware or Vast.ai:

**On your own GPU:**
```bash
# Start ComfyUI
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# Expose via ngrok or CloudFlare Tunnel
ngrok http 8188
```

**On Vast.ai:**
1. Rent RTX 3090 instance (~$0.10-0.20/hour)
2. Install ComfyUI
3. Set `COMFYUI_URL` to Vast.ai instance URL

---

## Docker Deployment

Each service has a Dockerfile for easy deployment:

```bash
# Build and run story service
cd story-service
docker build -t story-service .
docker run -p 8001:8001 \
  -e REDDIT_CLIENT_ID=your_id \
  -e REDDIT_CLIENT_SECRET=your_secret \
  -e OLLAMA_URL=http://host.docker.internal:11434 \
  story-service

# Build and run voice service
cd voice-service
docker build -t voice-service .
docker run -p 8002:8002 voice-service

# Build and run video service
cd video-service
docker build -t video-service .
docker run -p 8003:8003 \
  -e COMFYUI_URL=http://your-comfyui:8188 \
  video-service

# Build and run assembly service
cd assembly-service
docker build -t assembly-service .
docker run -p 8004:8004 assembly-service
```

---

## API Flow

```
1. Story Service → Generates story from Reddit + Ollama
   ↓
2. Voice Service → Converts story to audio with Coqui TTS
   ↓
3. Video Service → Creates video clips with ComfyUI
   ↓
4. Assembly Service → Combines everything with FFmpeg
   ↓
5. Final TikTok video (9:16, with audio, subtitles)
```

---

## Cost Breakdown

| Service | Tool | Cost |
|---------|------|------|
| Story | Ollama + Reddit | FREE |
| Voice | Coqui TTS | FREE |
| Video | ComfyUI | FREE* |
| Assembly | FFmpeg | FREE |
| **Total** | | **$0/month** |

\* Needs GPU - free if you own hardware, ~$5-15/month if renting

---

## Hardware Requirements

### Minimum (For 2-4 videos/day)
- CPU: Any modern processor
- RAM: 16GB
- GPU: RTX 3060 12GB
- Storage: 50GB

### Recommended (For 10+ videos/day)
- CPU: 8+ cores
- RAM: 32GB
- GPU: RTX 3090/4090 24GB
- Storage: 100GB

### No GPU?
- Use pyttsx3 for voice (no GPU)
- Rent GPU on-demand (~$0.10/hour)

---

## Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Coqui TTS Not Loading
```bash
# Reinstall
pip uninstall TTS
pip install TTS --no-cache-dir
```

### ComfyUI Offline
```bash
# Check if ComfyUI is running
curl http://localhost:8188/system_stats

# Start ComfyUI
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

### FFmpeg Not Found
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
apt-get install ffmpeg

# Verify
ffmpeg -version
```

---

## Next Steps

1. ✅ Get Reddit API credentials
2. ✅ Install free tools (Ollama, Coqui TTS, ComfyUI, FFmpeg)
3. ✅ Start all services locally
4. ✅ Test each service individually
5. ✅ Deploy to Railway (story, voice, assembly)
6. ✅ Connect to n8n workflow
7. ✅ Generate unlimited free videos! 🎉

---

**Questions?** Check the main [README.md](../README.md) or [FREE_SETUP.md](../FREE_SETUP.md)
