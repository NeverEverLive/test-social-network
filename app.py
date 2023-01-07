import urllib

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class EncodedUrlResponse(BaseModel):
    url: str
    message: str


@app.get("/", response_model=EncodedUrlResponse, status_code=200)
def encode_url(url: str):
    url = urllib.parse.quote(url)
    return EncodedUrlResponse(url=url, message="Url successfully encoded")