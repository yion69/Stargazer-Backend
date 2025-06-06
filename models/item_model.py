from pydantic import BaseModel, Field, conlist
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ItemModelBase(BaseModel):
    item_name: Optional[str] = Field(None, min_length=1, max_length=255)
    item_price: Optional[float] = Field(None, ge=0.0) # ge=0.0 means greater than or equal to 0
    item_brand: Optional[str] = Field(None, min_length=1, max_length=255)
    item_rating: Optional[float] = Field(None, ge=0.0, le=5.0) # Between 0.0 and 5.0
    item_sold: Optional[int] = Field(None, ge=0)
    item_images: Optional[List[str]] = Field(None)

class ItemCreateModel(ItemModelBase):
    pass

class ItemUpdateModel(ItemModelBase):
    pass

class ItemModelFull(ItemModelBase):
    item_id: UUID
    item_created_at: datetime