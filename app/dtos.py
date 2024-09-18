from pydantic import BaseModel


class HLSDownload(BaseModel):
    uuid: str
    url: str
    pic_url: str


class HLSConvert(HLSDownload):
    pass


class Response(BaseModel):
    status: int = 200
    message: str
