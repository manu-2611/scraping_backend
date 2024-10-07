from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.product import ProductResponse
from models.settings import Settings
from scraping import Scrapping
from settings import FILE_PATH, STATIC_TOKEN, STORAGE_TYPE
from storage.json import JsonStorage
from storage.sql import SQLStorage
from tasks.notification import NotificationStrategy

app = FastAPI()


# Dependency to check for the static token
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )

# Protected POST endpoint
@app.post("/products/", response_model=ProductResponse)
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
