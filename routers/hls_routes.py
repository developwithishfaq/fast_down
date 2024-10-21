from fastapi import APIRouter,Query
import requests
import re
from utils import extensions,hls_parser
from models import request_models,response_models
from typing import Dict,List
import core

router = APIRouter()

videoLinkResponse : Dict[str,Dict] = {}

@router.get("/getVideoLinks")
async def getVideoLinks(link: str = Query()):
    if link in videoLinkResponse:
        return videoLinkResponse[link]
    response = requests.get(link).text
    parsedData = hls_parser.parseQualities(text=response,url=link)
    result=  core.returnData(True,"Fetched",{
        "link" : link,
        "response" : parsedData
    })
    videoLinkResponse[link] = result
    return result

@router.get("/getVideoLinksWithChunks")
async def getVideoLinks(link: str = Query()):
    parsedData = getVideoLinks(link=link)
    newResponse = []
    for item in parsedData:
        data = (await getVideoLinks(item["url"]))
        item["chunks"]= {
           "urls" : data["response"]
        }
        newResponse.append(item)
    return {
        "link" : link,
        "response" : newResponse
    }


@router.post("/getAllSize")
async def getVideosSize(urls: request_models.VideoURLs):
    return await extensions.fetchAllSizes(urls.urls)

chunksRresults : Dict[str,Dict]  = {}

@router.get("/getVideoChunks")
async def getVideoLinks(link: str = Query()):
    if link in chunksRresults:
        return chunksRresults[link]
    response = requests.get(link).text
    parsedData = hls_parser.get_media_files(response,extensions.get_base_url(link))
    urlsModel = request_models.VideoURLs(urls=parsedData)
    videosWithSizes = await getVideosSize(urls=urlsModel)
    totalSize = sum(item["size"] for item in videosWithSizes)
    result =  {
        "link" : link,
        "totalSize": totalSize,
        "response" : videosWithSizes
    }
    chunksRresults[link] = result
    return result