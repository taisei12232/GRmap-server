from typing import List, Optional

from pydantic import BaseModel


class HelloWorldModel(BaseModel):
    Hello: str


class Shop(BaseModel):
    fid: str
    name: str
    url: Optional[str]
    position: List[float]


class Fest(BaseModel):
    name: str
    logo: str
    position_ul: List[float]
    position_br: List[float]


class Review(BaseModel):
    fid: str
    text: str
    sid: str
    position: List[float]
    haspicture: bool


class ReviewImage(BaseModel):
    fid: str
    rid: str
    url: str
