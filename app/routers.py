from fastapi import APIRouter
from requests import HTTPError
from starlette import status

from app.dtos import Response, HLSDownload, HLSConvert
from app.services import HLSService

service = HLSService()
router = APIRouter()


@router.get("/")
async def health_check():
    return Response(message="Hello!", status_code=200)


@router.post("/hls")
async def hls_download(hls: HLSDownload):
    # try:
    await service.hls_content_download(hls=hls)
    # except HTTPError:
    #     return Response(message=f"Failed to download {hls.url}"), status.HTTP_500_INTERNAL_SERVER_ERROR
    # except Exception:
    #     return Response(message="Unknown error"), status.HTTP_500_INTERNAL_SERVER_ERROR
    #
    # return Response(message="OK"), status.HTTP_201_CREATED


@router.post("/video")
async def media_download(video: HLSConvert):
    # try:
    await service.video_download_to_hls(video=video)
    # except HTTPError:
    #     return Response(
    #         message=f"Failed to download {video.url}"
    #     ), status.HTTP_500_INTERNAL_SERVER_ERROR
    # except EOFError:
    #     return Response(
    #         message=f"Failed to convert hls {video.url}"
    #     ), status.HTTP_500_INTERNAL_SERVER_ERROR
    # except Exception:
    #     return Response(message="Unknown error"), status.HTTP_500_INTERNAL_SERVER_ERROR
    #
    # return Response(message="OK"), status.HTTP_201_CREATED
