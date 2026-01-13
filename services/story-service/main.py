"""
Story Generation Service - 100% FREE
Uses Ollama (local LLM) + Reddit API
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random
import praw
import requests
import os

app = FastAPI(title="Story Service", description="FREE story generation using Ollama + Reddit")

# ==============================================
# Configuration
# ==============================================

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "your_client_id")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "your_secret")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TikTokStoryBot/1.0")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# ==============================================
# Reddit Setup
# ==============================================

try:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
except Exception as e:
    print(f"⚠️  Reddit API not configured: {e}")
    reddit = None

# ==============================================
# Request Models
# ==============================================

class StoryRequest(BaseModel):
    length_seconds: int = 25
    style: str = "dark absurd small town"
    universe: str = "snowy small town"
    twist_level: str = "high"
    subreddits: List[str] = ["ShortStories", "creepypasta", "AskReddit", "nosleep"]
    temperature: float = 0.8

class StoryResponse(BaseModel):
    title: str
    story_text: str
    hook: str
    visual_prompt: str
    reddit_seeds: List[str]

# ==============================================
# Helper Functions
# ==============================================

def get_reddit_seeds(subreddits: List[str], limit: int = 5) -> List[str]:
    """Fetch story seeds from Reddit (FREE)"""
    if not reddit:
        # Fallback seeds if Reddit not configured
        return [
            "A small town where everyone disappears at midnight",
            "Strange lights appear in the woods every winter",
            "The old lighthouse keeper never ages",
            "Children in the town all share the same nightmare",
            "A blizzard that never ends"
        ]
    
    seeds = []
    try:
        for sub in subreddits:
            posts = list(reddit.subreddit(sub).hot(limit=50))
            for post in posts:
                if post.selftext and len(post.selftext) > 100:
                    seeds.append(f"{post.title}: {post.selftext[:300]}")
        
        return random.sample(seeds, k=min(limit, len(seeds)))
    except Exception as e:
        print(f"Error fetching Reddit seeds: {e}")
        return [
            "A small town where everyone disappears at midnight",
            "Strange lights appear in the woods every winter"
        ]

def generate_story_with_ollama(
    seeds: List[str],
    style: str,
    universe: str,
    twist_level: str,
    temperature: float
) -> Dict:
    """Generate story using FREE Ollama LLM"""
    
    seed_text = "\n".join([f"- {seed}" for seed in seeds])
    
    prompt = f"""You are a TikTok storyteller. Create a compelling 25-second story.

Style: {style}
Universe: {universe}
Twist level: {twist_level}

Reddit inspiration:
{seed_text}

Create a JSON response with:
1. "title" - catchy title (5 words max)
2. "story_text" - the story (150-200 words, dramatic, engaging)
3. "hook" - opening line that grabs attention (1 sentence)
4. "visual_prompt" - cinematic visual description for video generation (descriptive, atmospheric)

Make it dark, mysterious, and engaging for TikTok audience.

Return ONLY valid JSON, no other text."""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "")
            
            # Try to parse JSON from response
            import json
            try:
                # Find JSON in response
                start = generated_text.find("{")
                end = generated_text.rfind("}") + 1
                if start >= 0 and end > start:
                    json_text = generated_text[start:end]
                    story_data = json.loads(json_text)
                    return story_data
            except:
                pass
            
            # Fallback: create structured response from text
            lines = generated_text.split("\n")
            return {
                "title": "Dark Tale",
                "story_text": generated_text[:500],
                "hook": lines[0] if lines else "Something strange happened...",
                "visual_prompt": f"{universe}, dark atmospheric lighting, cinematic, mysterious"
            }
        else:
            raise Exception(f"Ollama returned status {response.status_code}")
            
    except Exception as e:
        print(f"Error generating with Ollama: {e}")
        # Fallback story
        return {
            "title": "The Frozen Town",
            "story_text": f"In {universe}, strange things happen. {seeds[0] if seeds else 'Something mysterious unfolds.'}",
            "hook": "You won't believe what happened next...",
            "visual_prompt": f"{universe}, {style}, mysterious atmosphere, cinematic lighting"
        }

# ==============================================
# API Endpoints
# ==============================================

@app.get("/")
def read_root():
    return {
        "service": "Story Generation Service",
        "status": "running",
        "cost": "FREE",
        "llm": OLLAMA_MODEL,
        "reddit_configured": reddit is not None
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    ollama_status = "unknown"
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_status = "connected" if r.status_code == 200 else "error"
    except:
        ollama_status = "offline"
    
    return {
        "status": "healthy",
        "ollama": ollama_status,
        "reddit": "connected" if reddit else "not configured"
    }

@app.post("/generate-story", response_model=StoryResponse)
def generate_story(request: StoryRequest):
    """
    Generate a story using FREE tools:
    - Reddit API for story seeds
    - Ollama for story generation
    """
    try:
        # Step 1: Get Reddit seeds (FREE)
        print(f"📖 Fetching seeds from Reddit: {request.subreddits}")
        seeds = get_reddit_seeds(request.subreddits, limit=5)
        
        # Step 2: Generate story with Ollama (FREE)
        print(f"🤖 Generating story with Ollama ({OLLAMA_MODEL})...")
        story_data = generate_story_with_ollama(
            seeds=seeds,
            style=request.style,
            universe=request.universe,
            twist_level=request.twist_level,
            temperature=request.temperature
        )
        
        # Step 3: Return response
        return StoryResponse(
            title=story_data.get("title", "Dark Tale"),
            story_text=story_data.get("story_text", ""),
            hook=story_data.get("hook", "Something strange happened..."),
            visual_prompt=story_data.get("visual_prompt", f"{request.universe}, cinematic"),
            reddit_seeds=seeds
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_story():
    """Quick test endpoint"""
    return generate_story(StoryRequest())

# ==============================================
# Run Server
# ==============================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FREE Story Generation Service")
    print(f"   LLM: {OLLAMA_MODEL} @ {OLLAMA_URL}")
    print(f"   Reddit: {'✅ Configured' if reddit else '❌ Not configured'}")
    print(f"   Cost: $0.00/month 💚")
    uvicorn.run(app, host="0.0.0.0", port=8001)
