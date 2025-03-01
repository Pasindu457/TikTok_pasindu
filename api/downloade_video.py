from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import re
from mangum import Mangum

# FastAPI app
app = FastAPI()

# Mock Data (In a real-world scenario, you'd fetch video metadata from TikTok)
MOCK_VIDEO_METADATA = {
    'title': 'Sample TikTok Video',
    'author': 'John Doe',
    'duration': 120,
    'quality': 'high',
    'size': 50000000,  # in bytes
    'url': 'https://download-tiktok.com/video.mp4'
}

# Function to validate TikTok URL
def validate_tiktok_url(url: str) -> bool:
    pattern = r"https:\/\/www\.tiktok\.com\/@[\w.-]+\/video\/\d+"
    return bool(re.match(pattern, url))

# Mock video download function
def download_video(url: str, quality: Optional[str], format: Optional[str], watermark: bool):
    # Simulate video download and processing
    video_data = MOCK_VIDEO_METADATA.copy()
    if quality:
        video_data['quality'] = quality
    if format:
        video_data['format'] = format
    if watermark:
        video_data['watermark_removed'] = True
    return video_data

# Pydantic models for request and response
class VideoRequest(BaseModel):
    url: str
    quality: Optional[str] = 'high'  # 'high', 'medium', 'low'
    format: Optional[str] = 'mp4'   # 'mp4', 'webm'
    remove_watermark: Optional[bool] = False

class VideoResponse(BaseModel):
    video_url: str
    title: str
    author: str
    duration: int
    size: int
    quality: str
    format: str
    watermark_removed: bool

# API Endpoint to download TikTok video
@app.post("/download_video", response_model=VideoResponse, status_code=200)
async def download_video_endpoint(req: VideoRequest, request: Request):
    # Validate URL format
    if not validate_tiktok_url(req.url):
        raise HTTPException(status_code=400, detail="Invalid TikTok URL format")
    
    # Simulate downloading the video
    try:
        video_data = download_video(req.url, req.quality, req.format, req.remove_watermark)
        return video_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")

# Adapter for AWS Lambda (Vercel uses AWS Lambda under the hood)
handler = Mangum(app)
