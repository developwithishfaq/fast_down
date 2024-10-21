from fastapi import APIRouter,Query
import requests
import re
from utils import extensions
from models import request_models,response_models
from typing import Dict,List

def get_media_files(playlist_content, base_url):
    media_files = []
    lines = playlist_content.splitlines()
    isDataLoaded = True
    firstLink = ""
    for line in lines:
        # Check if the line is a media file (not a comment or directive)
        if not line.startswith("#") and line.strip():
            firstLink = line
            if "m3u8" in line:
                isDataLoaded = False
                break
            newLine = ""
            # If the line starts with 'http', it's a complete URL
            if line.startswith("http"):
                newLine = line
                media_files.append(line)
            else:
                newLine = f"{base_url}{line}"
            media_files.append(newLine)
    if isDataLoaded:
        return media_files
    else:
        isDataLoaded = True
        response = requests.get(base_url+firstLink).text
        return get_media_files(response,extensions.get_base_url(base_url+firstLink))




def parseQualities(text: str,url:str):
    lines = text.splitlines()
    values = []
    links = []
    data =None
    for index,line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF:"):
            data = extensions.parse_ext_x_stream_inf(line=line)
        elif not data is None:
            if line.startswith("http"):
                data["url"] = line
            else:
                data["url"] = extensions.get_base_url(url) +line
            values.append(data)
    return values


