from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):

    limit: Optional[int] = Field(
        None,
        description="Limit the number of pages to scrape. Default is None, meaning no limit."
    )
    proxy: Optional[str] = Field(
        None,
        description="Proxy string to use for scraping. Default is None, meaning no proxy."
    )

    class Config:
        json_schema_extra  = {
            "example": {
                "limit": 5,
                "proxy": "http://myproxy:port"
            }
        }
