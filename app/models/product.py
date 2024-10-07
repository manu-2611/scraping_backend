from pydantic import BaseModel, Field, HttpUrl

class Product(BaseModel):
    """Model representing a product with title, price, and image URL."""
    
    product_name: str       = Field(..., description="The name of the product.")
    product_price: float    = Field(..., gt=0, description="The price of the product. Must be greater than 0.")
    image_url: str      = Field(..., description="URL of the product image.")

    class Config:
        json_schema_extra  = {
            "example": {
                "product_title": "Sample Product",
                "product_price": 29.99,
                "path_to_image": "https://example.com/image.jpg"
            }
        }