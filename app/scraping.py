from bs4 import BeautifulSoup as soup
from settings import TARGET_URL, REDIS_HOST, REDIS_PORT, REDIS_DB
from utils import CleanData, make_get_request_with_retries, check_missing_elements, check_missing_elements_after_conversion, ProductCacheManager
import redis, logging
from models.product import Product
from models.settings import Settings
from storage.storage import StorageClass


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scrapping:
    def __init__(self,settings:Settings,storageType:StorageClass):
        
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.baseURL = TARGET_URL
        self.settings = settings
        self.storage = storageType


    def scrapData(self, ):

        page = 1
        lis = []
        product_skipped = 0
        products = [  ]

        while self.settings.limit and page <= self.settings.limit:

            url = f"{self.baseURL}page/{page}/"
            responseData = make_get_request_with_retries(url=url)
            
            if not responseData:
                break

            soup_data = soup(responseData.text, 'html.parser')
            response_data = soup_data.select("li.product")
            if not response_data:
                logger.info(f"No product elements found on page {page}.")
                break

            for product in response_data:
                productName = product.select_one(".woo-loop-product__title a")
                productPrice = product.select_one(".price .woocommerce-Price-amount bdi")
                imageURL = product.select_one(".mf-product-thumbnail img")

                if check_missing_elements(page=page, productName=productName, productPrice=productPrice, imageURL=imageURL):
                    product_skipped+=1
                    continue

                productPrice = CleanData().price(productPrice)   #CleanData class can be used to clean the respective responseData 
                productName = CleanData().name(productName)   #CleanData class can be used to clean the respective responseData 
                imageURL = CleanData().image_url(imageURL)   #CleanData class can be used to clean the respective responseData 

                if check_missing_elements_after_conversion(page=page, productName=productName, productPrice=productPrice, imageURL=imageURL):
                    product_skipped+=1
                    continue

                product_model_obj = Product(
                    product_name = productName,
                    product_price = productPrice,
                    image_url = imageURL
                    )
                products.append(product_model_obj)
                # self.cache_product(product_obj)

                dic = {"price": productPrice,"name":productName,"image": imageURL}
                lis.append(dic)
            page+=1
        cache = ProductCacheManager(products=products,storage=self.storage, redis_client=self.redis_client)
        cache.cache_and_store_results()
        response = {"product_skipped": product_skipped,"count": len(products), "products":products }

        return response
