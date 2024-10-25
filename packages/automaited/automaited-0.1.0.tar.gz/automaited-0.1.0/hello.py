from datetime import date
from pydantic import Field, BaseModel
from automaited import DocExtClient

class Article(BaseModel):
    article_number: str = Field(..., description="Typically alphabetical or alphanumerical.")
    description: str = Field(..., description="Description of the item.")
    quantity: float = Field(..., description="Number of pieces.")

class PurchaseOrder(BaseModel):
    customer_name: str = Field(..., description="Examples: Kaladent Inc., Henkel GmbH")
    order_number: str = Field(..., description="The purchase order number.")
    order_date: date = Field(..., description="The purchase order date.")
    items: list[Article] = Field(default_factory=list, description="List of all ordered articles.")

# print(PurchaseOrder.schema_json())

client = DocExtClient(API_KEY="TEST_BETA:you@company.com", base_url="http://localhost:8197/api/external_devs") # Use this for now, prod API keys coming soon
result: PurchaseOrder = client.extract_model(PurchaseOrder, "./po.pdf") # automaited.dev/samples
print(result)
