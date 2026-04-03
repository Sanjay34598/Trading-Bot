from pydantic import BaseModel, constr, confloat, validator
from typing import Optional

class OrderModel(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None

    @validator('symbol')
    def symbol_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError("Symbol must be alphanumeric (e.g., BTCUSDT).")
        return v.upper()

    @validator('side')
    def side_must_be_valid(cls, v):
        v = v.upper()
        if v not in ['BUY', 'SELL']:
            raise ValueError("Side must be BUY or SELL.")
        return v

    @validator('order_type')
    def type_must_be_valid(cls, v):
        v = v.upper()
        if v not in ['MARKET', 'LIMIT']:
            raise ValueError("Type must be MARKET or LIMIT.")
        return v

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return v

    @validator('price')
    def price_validation(cls, v, values):
        # Default price to None, but require if it's a LIMIT order
        order_type = values.get('order_type')
        if order_type == 'LIMIT':
            if v is None or v <= 0:
                raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")
        return v
