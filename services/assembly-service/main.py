"""
Video Assembly Service - 100% FREE
Uses FFmpeg for video assembly, subtitles, and audio
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import os
import uuid
from pathlib import Path

app = FastAPI(title="Assembly Service", description="FREE video assembly using FFmpeg")

# ==============================================
# Configuration
# ==============================================

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/tmp/assembly_output")
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/assembly_temp")

# Create directories
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)

# ==============================================
# Request Models
# ==============================================

class AssemblyRequest(BaseModel):
    video_clips: List[str]  # Paths to video clips
    audio_path: str  # Path to audio file
    hook: Optional[str] = None  # Optional hook text for caption
    add_subtitles: bool = True
    subtitle_text: Optional[str] = None

class AssemblyResponse(BaseModel):
    final_video: str
    duration: float
    file_size: int

# ==============================================
# FFmpeg Helper Functions
# ==============================================

def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False

def concatenate_clips(clips: List[str], output_path: str) -> bool:
    """Concatenate video clips using FFmpeg"""
    try:
        # Create concat file
        concat_file = os.path.join(TEMP_DIR, f"concat_{uuid.uuid4()}.txt")
        with open(concat_file, 'w') as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")
        
        # Concatenate using FFmpeg
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Cleanup
        os.remove(concat_file)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error concatenating clips: {e}")
        return False

def add_audio_to_video(video_path: str, audio_path: str, output_path: str) -> bool:
    """Add audio to video using FFmpeg"""
    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error adding audio: {e}")
        return False

def create_subtitle_file(text: str, duration: float) -> str:
    """Create SRT subtitle file"""
    srt_path = os.path.join(TEMP_DIR, f"subtitles_{uuid.uuid4()}.srt")
    
    # Split text into chunks (roughly 10 words per subtitle)
    words = text.split()
    chunk_size = 10
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    # Calculate timing
    chunk_duration = duration / len(chunks)
    
    with open(srt_path, 'w') as f:
        for i, chunk in enumerate(chunks):
            start_time = i * chunk_duration
            end_time = (i + 1) * chunk_duration
            
            f.write(f"{i+1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{chunk}\n\n")
    
    return srt_path

def format_time(seconds: float) -> str:
    """Format seconds to SRT time format (00:00:00,000)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def add_subtitles_to_video(video_path: str, subtitle_text: str, duration: float, output_path: str) -> bool:
    """Add subtitles to video using FFmpeg"""
    try:
        # Create subtitle file
        srt_path = create_subtitle_file(subtitle_text, duration)
        
        # Add subtitles using FFmpeg
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}:force_style='Fontsize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,Alignment=2'",
            "-c:a", "copy",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Cleanup
        os.remove(srt_path)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error adding subtitles: {e}")
        return False

def get_video_duration(video_path: str) -> float:
    """Get video duration using FFmpeg"""
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    
    return 0.0

# ==============================================
# API Endpoints
# ==============================================

@app.get("/")
def read_root():
    ffmpeg_installed = check_ffmpeg()
    return {
        "service": "Video Assembly Service",
        "status": "running",
        "cost": "FREE",
        "backend": "FFmpeg",
        "ffmpeg_installed": ffmpeg_installed
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    ffmpeg_status = "installed" if check_ffmpeg() else "not_found"
    return {
        "status": "healthy" if ffmpeg_status == "installed" else "ffmpeg_missing",
        "ffmpeg": ffmpeg_status,
        "output_dir": OUTPUT_DIR
    }

@app.post("/assemble-video", response_model=AssemblyResponse)
def assemble_video(request: AssemblyRequest):
    """
    Assemble final video using FREE FFmpeg:
    1. Concatenate video clips
    2. Add audio
    3. Add subtitles (optional)
    """
    try:
        if not check_ffmpeg():
            raise HTTPException(
                status_code=503,
                detail="FFmpeg not installed. Install with: apt-get install ffmpeg"
            )
        
        if not request.video_clips:
            raise HTTPException(status_code=400, detail="No video clips provided")
        
        if not request.audio_path:
            raise HTTPException(status_code=400, detail="No audio path provided")
        
        print(f"🎬 Assembling video from {len(request.video_clips)} clips...")
        
        # Generate unique filename
        video_id = uuid.uuid4()
        temp_concat = os.path.join(TEMP_DIR, f"concat_{video_id}.mp4")
        temp_audio = os.path.join(TEMP_DIR, f"audio_{video_id}.mp4")
        final_output = os.path.join(OUTPUT_DIR, f"final_{video_id}.mp4")
        
        # Step 1: Concatenate clips
        print("   Step 1: Concatenating clips...")
        if not concatenate_clips(request.video_clips, temp_concat):
            raise Exception("Failed to concatenate clips")
        
        # Step 2: Add audio
        print("   Step 2: Adding audio...")
        if not add_audio_to_video(temp_concat, request.audio_path, temp_audio):
            raise Exception("Failed to add audio")
        
        # Step 3: Add subtitles (if requested)
        if request.add_subtitles and request.subtitle_text:
            print("   Step 3: Adding subtitles...")
            duration = get_video_duration(temp_audio)
            if not add_subtitles_to_video(temp_audio, request.subtitle_text, duration, final_output):
                # If subtitles fail, use video without subtitles
                print("   Warning: Subtitles failed, using video without subtitles")
                os.rename(temp_audio, final_output)
        else:
            os.rename(temp_audio, final_output)
        
        # Get video info
        duration = get_video_duration(final_output)
        file_size = os.path.getsize(final_output)
        
        # Cleanup temp files
        try:
            if os.path.exists(temp_concat):
                os.remove(temp_concat)
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
        except:
            pass
        
        print(f"✅ Video assembled: {duration:.2f}s, {file_size/1024/1024:.2f}MB")
        
        return AssemblyResponse(
            final_video=final_output,
            duration=duration,
            file_size=file_size
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{video_id}")
def download_video(video_id: str):
    """Download assembled video"""
    filepath = os.path.join(OUTPUT_DIR, f"final_{video_id}.mp4")
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        filepath,
        media_type="video/mp4",
        filename=f"tiktok_{video_id}.mp4"
    )

@app.delete("/cleanup")
def cleanup_old_files():
    """Clean up old files"""
    try:
        import time
        deleted = 0
        current_time = time.time()
        
        for directory in [OUTPUT_DIR, TEMP_DIR]:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
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
    print("🚀 Starting FREE Video Assembly Service")
    print(f"   Backend: FFmpeg")
    print(f"   Status: {'✅ Ready' if check_ffmpeg() else '❌ FFmpeg not found'}")
    print(f"   Cost: $0.00/month 💚")
    uvicorn.run(app, host="0.0.0.0", port=8004)
