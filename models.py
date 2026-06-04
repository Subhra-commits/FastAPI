from pydantic import BaseModel, Field
from typing import Annotated

class Products(BaseModel):
    id: Annotated[int, Field(..., description="Product ID", examples={1})]
    name: Annotated[str, Field(..., max_lenth = 30, description = "Product name")]
    description: Annotated[str, Field(..., description = 'Product description')]
    price: Annotated[float, Field(..., gt = 0, description = 'Product price')]
    quantity: Annotated[int, Field(..., gt = 0, description = 'Product quantity')]

    
