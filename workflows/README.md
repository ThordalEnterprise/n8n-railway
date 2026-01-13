# n8n Workflows

This directory contains pre-built n8n workflows ready for import.

## Available Workflows

### 1. TikTok Auto Story + Video Pipeline

**File:** `tiktok-auto-story.json`

**Description:**  
Fully automated TikTok content creation pipeline that generates unique story videos from Reddit content.

**Features:**
- 🤖 Automated story generation from Reddit (ShortStories, creepypasta, AskReddit)
- 🎯 OpenAI-powered unique narratives with hooks
- 🎙️ Text-to-speech voice generation
- 🎬 AI video generation (AnimateDiff + SDXL)
- 📱 9:16 TikTok format with subtitles
- ⏰ Scheduled execution (10:00 and 18:00 daily)

**Workflow Nodes:**

1. **Cron Trigger** - Runs twice daily
2. **Generate Story** - Fetches Reddit seeds + OpenAI story generation
3. **Generate Voice** - Converts story text to audio (TTS)
4. **Generate Video** - Creates video clips from visual prompt
5. **Merge Data** - Combines voice and video data
6. **Assemble Video** - Final video assembly with subtitles
7. **Post to TikTok** - Uploads to TikTok with caption

**Requirements:**

External FastAPI services (deploy separately on Railway):

- **Story Service** (`/generate-story`)
  - Reddit API credentials (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
  - OpenAI API key
  
- **Voice Service** (`/generate-voice`)
  - TTS engine (ElevenLabs, Coqui TTS, or similar)
  
- **Video Service** (`/generate-video`)
  - GPU for AnimateDiff + SDXL
  - ComfyUI or similar backend
  
- **Assembly Service** (`/assemble-video`)
  - FFmpeg for video assembly
  - Subtitle generation
  
- **TikTok Upload Service** (`/upload`)
  - TikTok API credentials

**Setup Instructions:**

1. Import workflow in n8n:
   - Go to Workflows → Import from File
   - Select `tiktok-auto-story.json`

2. Update service URLs in each HTTP Request node:
   ```
   https://story-service.up.railway.app/generate-story
   https://voice-service.up.railway.app/generate-voice
   https://video-service.up.railway.app/generate-video
   https://assembly-service.up.railway.app/assemble-video
   https://tiktok-upload-service.up.railway.app/upload
   ```

3. Configure credentials (if using n8n credentials manager):
   - OpenAI API
   - Reddit API
   - TikTok API

4. Test workflow manually before enabling schedule

5. Activate workflow

**Customization:**

Edit the "Generate Story" node body to customize:

```json
{
  "length_seconds": 25,        // Story length
  "style": "dark absurd small town",  // Story style
  "universe": "snowy small town",      // Setting
  "twist_level": "high",              // Twist intensity
  "subreddits": [                     // Reddit sources
    "ShortStories",
    "creepypasta",
    "AskReddit"
  ]
}
```

**Output:**

Final TikTok video with:
- ✅ Unique AI-generated story
- ✅ Professional voice-over
- ✅ Cinematic video clips (9:16)
- ✅ Automated subtitles
- ✅ Catchy hook as caption
- ✅ Relevant hashtags

---

## How to Import Workflows

1. Log in to your n8n instance
2. Navigate to **Workflows** in the sidebar
3. Click **"Add Workflow"** → **"Import from File"**
4. Select the `.json` file from this directory
5. Update credentials and URLs as needed
6. Test and activate

## Contributing

Have a useful workflow? Submit a PR with:
- Workflow JSON file
- Documentation in this README
- Required services/credentials list

---

**Note:** All workflows are templates. Update service URLs and credentials before use.
