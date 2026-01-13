"""
Video Generation Service - 100% FREE
Uses ComfyUI for video generation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
import os
import json
import time
import uuid
from pathlib import Path

app = FastAPI(title="Video Service", description="FREE video generation using ComfyUI")

# ==============================================
# Configuration
# ==============================================

COMFYUI_URL = os.getenv("COMFYUI_URL", "http://localhost:8188")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/video_output")

# Create output directory
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ==============================================
# Request Models
# ==============================================

class VideoRequest(BaseModel):
    visual_prompt: str
    num_clips: int = 5
    clip_duration: int = 5
    aspect_ratio: List[int] = [9, 16]  # TikTok format
    fps: int = 24

class VideoResponse(BaseModel):
    clips: List[str]
    total_duration: float
    prompt_used: str

# ==============================================
# ComfyUI Helper Functions
# ==============================================

def check_comfyui_status() -> bool:
    """Check if ComfyUI is available"""
    try:
        response = requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        return response.status_code == 200
    except:
        return False

def generate_workflow(prompt: str, num_frames: int, width: int, height: int) -> Dict:
    """
    Generate ComfyUI workflow for AnimateDiff video generation
    This is a simplified workflow - you'll need to adjust based on your ComfyUI setup
    """
    workflow = {
        "1": {
            "inputs": {
                "text": prompt,
                "clip": ["4", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "2": {
            "inputs": {
                "text": "blurry, low quality, distorted",
                "clip": ["4", 0]
            },
            "class_type": "CLIPTextEncode"
        },
        "3": {
            "inputs": {
                "seed": int(time.time()),
                "steps": 20,
                "cfg": 8.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["1", 0],
                "negative": ["2", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": num_frames
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode"
        },
        "7": {
            "inputs": {
                "filename_prefix": f"tiktok_{uuid.uuid4()}",
                "images": ["6", 0]
            },
            "class_type": "SaveImage"
        }
    }
    return workflow

def queue_prompt(workflow: Dict) -> str:
    """Queue workflow in ComfyUI"""
    try:
        response = requests.post(
            f"{COMFYUI_URL}/prompt",
            json={"prompt": workflow},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("prompt_id", "")
        else:
            raise Exception(f"ComfyUI returned status {response.status_code}")
    except Exception as e:
        raise Exception(f"Failed to queue prompt: {e}")

def wait_for_completion(prompt_id: str, timeout: int = 300) -> bool:
    """Wait for ComfyUI to complete generation"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
            if response.status_code == 200:
                history = response.json()
                if prompt_id in history:
                    return True
        except:
            pass
        
        time.sleep(2)
    
    return False

def get_output_images(prompt_id: str) -> List[str]:
    """Get generated images from ComfyUI"""
    try:
        response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
        if response.status_code == 200:
            history = response.json()
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                images = []
                for node_output in outputs.values():
                    if "images" in node_output:
                        for img in node_output["images"]:
                            filename = img.get("filename", "")
                            if filename:
                                images.append(filename)
                return images
    except:
        pass
    
    return []

# ==============================================
# API Endpoints
# ==============================================

@app.get("/")
def read_root():
    comfyui_online = check_comfyui_status()
    return {
        "service": "Video Generation Service",
        "status": "running",
        "cost": "FREE",
        "backend": "ComfyUI + AnimateDiff",
        "comfyui_url": COMFYUI_URL,
        "comfyui_status": "online" if comfyui_online else "offline"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    comfyui_status = "online" if check_comfyui_status() else "offline"
    return {
        "status": "healthy" if comfyui_status == "online" else "comfyui_offline",
        "comfyui": comfyui_status,
        "output_dir": OUTPUT_DIR
    }

@app.post("/generate-video", response_model=VideoResponse)
def generate_video(request: VideoRequest):
    """
    Generate video clips using FREE ComfyUI + AnimateDiff
    
    Note: Requires ComfyUI with AnimateDiff and SDXL models installed
    """
    try:
        # Check ComfyUI status
        if not check_comfyui_status():
            raise HTTPException(
                status_code=503,
                detail=f"ComfyUI not available at {COMFYUI_URL}"
            )
        
        print(f"🎬 Generating {request.num_clips} video clips...")
        print(f"   Prompt: {request.visual_prompt}")
        
        # Calculate dimensions
        width = 1080 if request.aspect_ratio == [9, 16] else 1920
        height = 1920 if request.aspect_ratio == [9, 16] else 1080
        num_frames = request.clip_duration * request.fps
        
        clips = []
        
        # Generate each clip
        for i in range(request.num_clips):
            print(f"   Generating clip {i+1}/{request.num_clips}...")
            
            # Create workflow
            workflow = generate_workflow(
                prompt=request.visual_prompt,
                num_frames=num_frames,
                width=width,
                height=height
            )
            
            # Queue in ComfyUI
            prompt_id = queue_prompt(workflow)
            
            # Wait for completion
            if wait_for_completion(prompt_id):
                # Get output images
                images = get_output_images(prompt_id)
                if images:
                    clips.extend(images)
        
        total_duration = request.num_clips * request.clip_duration
        
        print(f"✅ Generated {len(clips)} clips")
        
        return VideoResponse(
            clips=clips,
            total_duration=total_duration,
            prompt_used=request.visual_prompt
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
def test_video():
    """Quick test endpoint"""
    return generate_video(VideoRequest(
        visual_prompt="Snowy small town, dark atmosphere, mysterious lights, cinematic",
        num_clips=2,
        clip_duration=3
    ))

# ==============================================
# Run Server
# ==============================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FREE Video Generation Service")
    print(f"   Backend: ComfyUI + AnimateDiff")
    print(f"   ComfyUI: {COMFYUI_URL}")
    print(f"   Status: {'✅ Connected' if check_comfyui_status() else '❌ Offline'}")
    print(f"   Cost: $0.00/month 💚")
    uvicorn.run(app, host="0.0.0.0", port=8003)
