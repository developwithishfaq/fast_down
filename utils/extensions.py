import re
from urllib.parse import urljoin
import requests
from pydantic import BaseModel
from typing import Dict,List
import aiohttp,asyncio


def get_base_url(url):
    # Extract base URL by removing the last part of the path
    base_url = url.rsplit('/', 1)[0] + '/'
    return base_url

def parse_ext_x_stream_inf(line):
    # Regular expression to match key=value pairs
    pattern = r'([A-Z\-]+)=("[^"]*"|[^,]*)'
    
    # Find all matches
    matches = re.findall(pattern, line)
    
    # Convert matches to a dictionary
    result = {key: value.strip('"') for key, value in matches}
    
    # Convert numeric values to integers (if possible)
    for key, value in result.items():
        if value.isdigit():
            result[key] = int(value)
    
    return result

def get_file_size(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200 and 'Content-Length' in response.headers:
            return int(response.headers['Content-Length'])
        else:
            return None
    except Exception as e:
        print(f"Error fetching size for {url}: {e}")
        return None
    
async def getFileSize(session,url):
    try:
        async with session.head(url) as response:
            if response.status == 200 and 'Content-Length' in response.headers:
                return {"link":url,"size":int(response.headers["Content-Length"])}
            else:
                return {"link":url,"size": -1}
    except Exception as e:
        return {
            "link":url,
            "size" :None
        }
    
async def fetchAllSizes(urls:List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [getFileSize(session,url) for url in urls]
        return await asyncio.gather(*tasks)