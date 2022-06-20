import datetime
from beanie import Document, Indexed, Replace, after_event
from pydantic import Field

from . import Price, ProductStatus

class Product(Document):
    #code_name: Indexed(str, unique=True) = Field(..., title="")
    name: str = Field(..., title="Name", description="Product name")
    detail: str = Field(..., title="Details", description="Product general details")
    price: Price = Field(..., title="Price", description="Product price data")
    vat: int = Field(19, title="VAT", description="Product national vat")
    stock: int = Field(..., title="Stock", description="Product disponibility")
    images: list[str] = Field([], title="Images", description="Product images")
    status: ProductStatus = Field(..., title="Status", description="Product status")
    is_available: bool = Field(..., title="Available", description="Product available")
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="Product creation date")
    updated_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Updated AT", description="Product last updated")

    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()

    class Collection:
        name = "products"
    
    class Settings:
        use_state_management = True
        validate_on_save = True
        use_state_management = True