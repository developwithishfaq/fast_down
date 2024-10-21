from fastapi import APIRouter,Query,HTTPException
from fastapi.responses import StreamingResponse
import requests
import re
from utils import extensions,hls_parser
from models import request_models,response_models
from typing import Dict,List
import core
import subprocess
import json
import io

router = APIRouter()


@router.get("/extract/{link:path}")
async def getVideoInfo(link: str):
    return get_video_info(link)


def get_video_info(url):
    # Run ffprobe to extract video information
    command = [
        'ffprobe', '-v', 'error', '-show_format', '-show_streams',
        '-print_format', 'json', url
    ]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Parse the result as JSON
    video_info = json.loads(result.stdout)
    return video_info
