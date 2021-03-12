import datetime
from typing import Union

from pydantic import BaseModel


class WebsiteBase(BaseModel):
    url: str


class WebsiteCreate(WebsiteBase):
    pass


class Website(WebsiteBase):
    id: int
    started_at: datetime.datetime
    status: str
    completed_at: Union[datetime.datetime, None]
    text: Union[str, None]

    class Config:
        orm_mode = True
