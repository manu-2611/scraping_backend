from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from settings import STATIC_TOKEN, FILE_PATH, STORAGE_TYPE
from models.settings import Settings
from tasks.notification import NotificationStrategy
from scraping import Scrapping
from storage.json import JsonStorage
from storage.sql import SQLStorage

app = FastAPI()


# Dependency to check for the static token
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

# Protected POST endpoint
@app.post("/products/")
async def product(settings: Settings, credentials: HTTPAuthorizationCredentials = Depends(verify_token)):  
    if STORAGE_TYPE == "JSON":
        storage = JsonStorage(FILE_PATH)
    if STORAGE_TYPE =="SQL":
        storage = SQLStorage()
    scraper = Scrapping(settings, storageType=storage)
    response = scraper.scrapData()

    if response:

        notification = NotificationStrategy()
        final_message = (
            "Scraping completed. "
            f"Total products scraped: {response.get("count")}, "
            f"Total products skipped: {response.get("total_skipped")}."
        )

        notification.console_notification(final_message)


        return response
    return {"error": "Something went wrong, check logs for more clarity"}

