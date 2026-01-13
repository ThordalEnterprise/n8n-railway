# API Credentials Setup Guide

This guide covers all API keys and credentials needed for the TikTok Auto Story workflow.

## Required API Keys & Credentials

### 1. OpenAI API Key

**Used for:** Story generation using GPT-4

**How to get:**
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up / Log in
3. Go to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the key (starts with `sk-...`)

**Environment variable:**
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Cost:** ~$0.03 per story (GPT-4), ~$0.002 per story (GPT-3.5-turbo)

---

### 2. Reddit API Credentials

**Used for:** Scraping story seeds from subreddits

**How to get:**
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Scroll to bottom, click **"Create App"** or **"Create Another App"**
3. Fill in:
   - **Name:** TikTok Story Generator
   - **Type:** Select **"script"**
   - **Description:** Story seed scraper
   - **About URL:** (leave blank)
   - **Redirect URI:** `http://localhost:8080`
4. Click **"Create app"**
5. Note down:
   - **Client ID** (under app name, 14 characters)
   - **Client Secret** (next to "secret")

**Environment variables:**
```bash
REDDIT_CLIENT_ID=your_14_char_id
REDDIT_CLIENT_SECRET=your_secret_key
REDDIT_USER_AGENT=TikTokStoryBot/1.0
```

**Cost:** FREE (up to 60 requests per minute)

---

### 3. TikTok API Credentials

**Used for:** Uploading videos to TikTok

**⚠️ Note:** TikTok API is restricted and requires approval.

#### Option A: Official TikTok Developer Platform (Recommended)

**How to get:**
1. Go to [TikTok Developers](https://developers.tiktok.com)
2. Sign up as a developer
3. Create a new app
4. Apply for **"Content Posting API"** access
5. Wait for approval (can take 2-4 weeks)
6. Get your:
   - Client Key
   - Client Secret
   - Access Token

**Environment variables:**
```bash
TIKTOK_CLIENT_KEY=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret
TIKTOK_ACCESS_TOKEN=your_access_token
```

**Cost:** FREE (subject to rate limits)

#### Option B: Alternative - Upload to Cloud Storage

Instead of TikTok API, upload to S3/Cloud and download manually:

**Environment variables:**
```bash
# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=tiktok-videos
AWS_REGION=eu-west-1

# Or Cloudflare R2 (cheaper)
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=tiktok-videos
R2_ACCOUNT_ID=your_account_id
```

---

### 4. Text-to-Speech (TTS) API

#### Option A: ElevenLabs (Best Quality)

**How to get:**
1. Go to [ElevenLabs](https://elevenlabs.io)
2. Sign up
3. Go to **Profile → API Keys**
4. Copy your API key

**Environment variables:**
```bash
ELEVENLABS_API_KEY=your_api_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Default voice
```

**Cost:** 
- Free: 10,000 characters/month (~6-8 videos)
- Starter: $5/month - 30,000 characters
- Creator: $22/month - 100,000 characters

#### Option B: OpenAI TTS (Cheaper)

Uses same OpenAI key as story generation.

**Environment variable:**
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

**Cost:** $0.015 per 1,000 characters (~$0.004 per video)

#### Option C: Coqui TTS (FREE, Self-hosted)

No API key needed, runs locally with GPU.

**Requirements:**
- GPU with 4GB+ VRAM
- Python + Coqui TTS installed

---

### 5. Video Generation (AnimateDiff + SDXL)

**Runs on:** Self-hosted GPU or RunPod/Replicate

#### Option A: Self-hosted (FREE if you have GPU)

**Requirements:**
- NVIDIA GPU with 12GB+ VRAM (RTX 3060 Ti or better)
- ComfyUI with AnimateDiff + SDXL models
- No API key needed

#### Option B: RunPod (Pay per use)

**How to get:**
1. Go to [RunPod.io](https://runpod.io)
2. Sign up
3. Go to **Settings → API Keys**
4. Create new API key

**Environment variables:**
```bash
RUNPOD_API_KEY=your_api_key
RUNPOD_ENDPOINT_ID=your_endpoint_id
```

**Cost:** ~$0.15-0.50 per video (depending on GPU)

#### Option C: Replicate (Easiest)

**How to get:**
1. Go to [Replicate.com](https://replicate.com)
2. Sign up
3. Go to **Account → API Tokens**
4. Copy token

**Environment variables:**
```bash
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxx
```

**Cost:** ~$0.50-1.00 per video

---

## Environment Variables Summary

### Core Story Generation
```bash
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# Reddit
REDDIT_CLIENT_ID=your_14_char_id
REDDIT_CLIENT_SECRET=your_secret_key
REDDIT_USER_AGENT=TikTokStoryBot/1.0
```

### Voice Generation (Choose one)
```bash
# Option A: ElevenLabs (best quality)
ELEVENLABS_API_KEY=your_api_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Option B: OpenAI TTS (already have key above)
# No additional key needed

# Option C: Coqui TTS (self-hosted)
# No API key needed
```

### Video Generation (Choose one)
```bash
# Option A: Self-hosted ComfyUI
# No API key needed

# Option B: RunPod
RUNPOD_API_KEY=your_api_key
RUNPOD_ENDPOINT_ID=your_endpoint_id

# Option C: Replicate
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxxx
```

### TikTok Upload (Choose one)
```bash
# Option A: TikTok API (requires approval)
TIKTOK_CLIENT_KEY=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret
TIKTOK_ACCESS_TOKEN=your_access_token

# Option B: S3/R2 Upload
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=tiktok-videos
AWS_REGION=eu-west-1
```

---

## Setting Credentials in n8n

### Method 1: n8n Credentials Manager (Recommended)

1. Log in to n8n
2. Go to **Settings → Credentials**
3. Click **"Add Credential"**
4. Select credential type (e.g., "OpenAI API", "HTTP Header Auth")
5. Enter your API key
6. Save with a descriptive name

In your workflow, reference credentials by name instead of hardcoding.

### Method 2: Environment Variables in Railway

1. Go to your Railway service
2. Click **"Variables"** tab
3. Add each key-value pair
4. Railway automatically restarts service

Example:
```
OPENAI_API_KEY = sk-proj-xxxxx
REDDIT_CLIENT_ID = xxxxx
ELEVENLABS_API_KEY = xxxxx
```

### Method 3: .env File (Local Development Only)

**⚠️ NEVER commit .env to GitHub!**

Create `.env` file:
```bash
# Copy from env.example
cp env.example .env

# Edit with your keys
nano .env
```

---

## Cost Estimation (Per Video)

### Minimal Setup (Budget-friendly)
- OpenAI GPT-3.5-turbo: $0.002
- OpenAI TTS: $0.004
- Self-hosted video (own GPU): $0.00
- Manual TikTok upload: $0.00
- **Total: ~$0.006 per video**

### Balanced Setup (Recommended)
- OpenAI GPT-4: $0.03
- ElevenLabs TTS: $0.02
- Replicate video: $0.50
- TikTok API (free): $0.00
- **Total: ~$0.55 per video**

### Premium Setup (Best Quality)
- OpenAI GPT-4: $0.03
- ElevenLabs TTS (Creator plan): $0.02
- RunPod GPU (RTX 4090): $0.30
- TikTok API (free): $0.00
- **Total: ~$0.35 per video**

### Monthly Cost (2 videos/day = 60 videos/month)
- Minimal: ~$0.36/month
- Balanced: ~$33/month
- Premium: ~$21/month

---

## Security Best Practices

### ✅ DO:
- Store API keys in Railway environment variables
- Use n8n credentials manager for sensitive data
- Rotate API keys every 3-6 months
- Use separate keys for dev/staging/production
- Enable 2FA on all accounts

### ❌ DON'T:
- Hardcode API keys in workflow JSON
- Commit .env files to GitHub
- Share API keys in chat/email
- Use production keys for testing
- Leave unused API keys active

---

## Troubleshooting

### OpenAI API Errors
- **401 Unauthorized:** Check API key is correct
- **429 Rate limit:** Upgrade plan or reduce frequency
- **Insufficient credits:** Add payment method in OpenAI dashboard

### Reddit API Errors
- **401 Unauthorized:** Check client ID/secret
- **429 Too many requests:** Wait 1 minute, reduce scraping frequency
- **403 Forbidden:** Check user agent is set

### TikTok Upload Errors
- **API access denied:** Apply for Content Posting API approval
- **Invalid token:** Refresh access token
- **Video format error:** Ensure MP4, H.264, 9:16 aspect ratio

### Voice/Video Generation Errors
- **CUDA out of memory:** Reduce batch size or use smaller model
- **Timeout errors:** Increase timeout in HTTP Request nodes
- **Model not found:** Download required models to GPU server

---

## Next Steps

1. ✅ Get OpenAI + Reddit API keys (required for basic functionality)
2. ✅ Choose TTS provider (ElevenLabs recommended)
3. ✅ Choose video generation method (Replicate easiest to start)
4. ✅ Add all keys to Railway environment variables
5. ✅ Test each service individually before running full workflow
6. ✅ Set up TikTok API or use S3 upload as fallback

---

**Need help?** Check the main [README.md](README.md) or join the [n8n Community Forum](https://community.n8n.io).
