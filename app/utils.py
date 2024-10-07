import logging, time, requests
from typing import Optional
from bs4.element import Tag
from settings import RETRY_COUNT
from typing import List
from storage.json import JsonStorage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CleanData:
    # Class to clean and extract data from HTML elements.

    @staticmethod
    def price(price: Tag) -> float:
        # Extract and convert the price from a Tag.

        cleaned_price = float(price.text.replace("₹", "").replace(" ", ""))
        logger.debug("Extracted price: %s", cleaned_price)
        return cleaned_price

    @staticmethod
    def name(name: Tag) -> str:
        # Extract the name from a Tag

        cleaned_name = name.text.strip()
        logger.debug("Extracted name: %s", cleaned_name)
        return cleaned_name

    @staticmethod
    def image_url(image: Tag) -> Optional[str]:
        # Extract the image URL from a Tag

        image_url = str(image.get("data-lazy-src"))
        logger.debug("Extracted image URL: %s", image_url)
        return image_url

class ProductCacheManager:
    def __init__(self, redis_client, storage, products: List[dict]):
        self.redis_client = redis_client
        self.products = products
        self.storage = storage

    def cache_and_store_results(self) -> int:

        try:
            # Load current products from storage
            current_data = self.storage.get()

            names = {product["product_name"]: product for product in current_data}

            count = 0
            
            for product in self.products:
                cached_price = self.redis_client.get(product.product_name)

                # Check if price has not changed
                if cached_price and float(cached_price) == product.product_price:
                    logger.info(f"Skipping product '{product.product_name}' - price unchanged.")
                    continue

                # Update Redis cache
                self.redis_client.set(product.product_name, product.product_price)
                logger.info(f"Cached price for product '{product.product_name}': {product.product_price}")

                # Update local storage if the product price has changed or if it's a new product
                if product.product_name in names:
                    if names[product.product_name]["product_price"] != product.product_price:
                        names[product.product_name] = product.dict()
                        count += 1
                        logger.info(f"Updated product '{product.product_name}' with new price: {product.product_price}")
                else:
                    names[product.product_name] = product.dict()
                    count += 1
                    logger.info(f"Added new product '{product.product_name}' to storage.")

            logger.info(f"Saved {len(names)} products to storage.")
            self.storage.create(list(names.values()))

            return count

        except Exception as e:
            logger.error(f"An error occurred while caching and storing results: {e}")
            return 0




def make_get_request_with_retries(url: str, retries: int = RETRY_COUNT) -> Optional[requests.Response]:
    # Make an HTTP GET request with retries

    for attempt in range(retries):
        try:
            logger.info("Attempting to connect to %s (Attempt %d/%d)", url, attempt + 1, retries)
            response = requests.get(url)
            response.raise_for_status()
            logger.info("Successfully connected to %s", url)
            return response

        except requests.exceptions.RequestException as e:
            logger.warning(
                "Request to %s failed (attempt %d/%d): %s. Retrying in 5 seconds...",
                url, attempt + 1, retries, str(e)
            )
            time.sleep(5)

    logger.error("All attempts to connect to %s have failed.", url)

    return None

def check_missing_elements(page, productName, productPrice, imageURL):
    missing_elements = []
    if not productName:
        missing_elements.append("Title")
    if not productPrice:
        missing_elements.append("Price")
    if not imageURL:
        missing_elements.append("Image")
    if missing_elements:
        if len(missing_elements) == 3:  # If all elements are missing
            logger.warning("Skipping product on page %d due to all elements missing: %s", page, ", ".join(missing_elements))
        else:
            logger.warning("Skipping product on page %d due to missing elements: %s", page, ", ".join(missing_elements))
        return True
    return False


def check_missing_elements_after_conversion(page, productName, productPrice, imageURL):
    missing_elements = []
    if not productName:
        missing_elements.append("Title")
    if not productPrice:
        missing_elements.append("Price")
    if not imageURL:
        missing_elements.append("Image")
    if missing_elements:
        if len(missing_elements) == 3:  # If all elements are missing
            logger.warning("Skipping product on page %d due to data extraction and type conversion issues: All expected elements missing:%s", page, ", ".join(missing_elements))
        else:
            logger.warning("Skipping product on page %d due to data extraction and type conversion issues: Missing elements: %s", page, ", ".join(missing_elements))
        return True
    return False



