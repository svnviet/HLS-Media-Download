from pydantic import BaseModel


class HLSDownload(BaseModel):
    uuid: str
    url: str
    filename: str = 'mv.m3u8'


class HLSConvert(HLSDownload):
    pass


class Response(BaseModel):
    status: int = 200
    message: str
