"""
Voice Generation Service - 100% FREE
Uses Coqui TTS (open source)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import tempfile
import uuid
from pathlib import Path

app = FastAPI(title="Voice Service", description="FREE TTS using Coqui TTS")

# ==============================================
# Configuration
# ==============================================

TTS_MODEL = os.getenv("TTS_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/tts_output")

# Create output directory
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ==============================================
# Initialize TTS
# ==============================================

try:
    from TTS.api import TTS
    print(f"🎙️  Loading Coqui TTS model: {TTS_MODEL}")
    tts = TTS(model_name=TTS_MODEL)
    print("✅ TTS model loaded successfully!")
except Exception as e:
    print(f"⚠️  Error loading TTS: {e}")
    print("   Install with: pip install TTS")
    tts = None

# ==============================================
# Request Models
# ==============================================

class VoiceRequest(BaseModel):
    text: str
    speed: float = 1.0
    output_format: str = "wav"

class VoiceResponse(BaseModel):
    audio_file: str
    duration: float
    text_length: int

# ==============================================
# Helper Functions
# ==============================================

def generate_voice(text: str, speed: float = 1.0) -> str:
    """Generate voice using FREE Coqui TTS"""
    if not tts:
        raise Exception("TTS not initialized. Install with: pip install TTS")
    
    # Generate unique filename
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        # Generate audio
        tts.tts_to_file(
            text=text,
            file_path=filepath,
            speed=speed
        )
        
        return filepath
        
    except Exception as e:
        raise Exception(f"TTS generation failed: {e}")

def get_audio_duration(filepath: str) -> float:
    """Get audio duration in seconds"""
    try:
        import wave
        with wave.open(filepath, 'r') as audio_file:
            frames = audio_file.getnframes()
            rate = audio_file.getframerate()
            duration = frames / float(rate)
            return duration
    except:
        return 0.0

# ==============================================
# API Endpoints
# ==============================================

@app.get("/")
def read_root():
    return {
        "service": "Voice Generation Service",
        "status": "running",
        "cost": "FREE",
        "tts": "Coqui TTS",
        "model": TTS_MODEL,
        "ready": tts is not None
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if tts else "tts_not_loaded",
        "model": TTS_MODEL,
        "output_dir": OUTPUT_DIR
    }

@app.post("/generate-voice", response_model=VoiceResponse)
def generate_voice_endpoint(request: VoiceRequest):
    """
    Generate voice audio using FREE Coqui TTS
    
    Returns: Audio file path and metadata
    """
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        print(f"🎙️  Generating voice for {len(request.text)} characters...")
        
        # Generate audio
        audio_path = generate_voice(request.text, request.speed)
        
        # Get duration
        duration = get_audio_duration(audio_path)
        
        print(f"✅ Voice generated: {duration:.2f}s")
        
        return VoiceResponse(
            audio_file=audio_path,
            duration=duration,
            text_length=len(request.text)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def download_audio(filename: str):
    """Download generated audio file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        filepath,
        media_type="audio/wav",
        filename=filename
    )

@app.get("/models")
def list_models():
    """List available TTS models"""
    try:
        from TTS.api import TTS
        models = TTS.list_models()
        return {"models": models}
    except:
        return {"models": []}

@app.post("/test")
def test_voice():
    """Quick test endpoint"""
    return generate_voice_endpoint(VoiceRequest(
        text="This is a test of the free voice generation service."
    ))

# ==============================================
# Cleanup
# ==============================================

@app.delete("/cleanup")
def cleanup_old_files():
    """Clean up old audio files"""
    try:
        import time
        deleted = 0
        current_time = time.time()
        
        for filename in os.listdir(OUTPUT_DIR):
            filepath = os.path.join(OUTPUT_DIR, filename)
            # Delete files older than 1 hour
            if os.path.getmtime(filepath) < current_time - 3600:
                os.remove(filepath)
                deleted += 1
        
        return {"deleted_files": deleted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================================
# Run Server
# ==============================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FREE Voice Generation Service")
    print(f"   TTS: Coqui TTS")
    print(f"   Model: {TTS_MODEL}")
    print(f"   Status: {'✅ Ready' if tts else '❌ Not loaded'}")
    print(f"   Cost: $0.00/month 💚")
    uvicorn.run(app, host="0.0.0.0", port=8002)
