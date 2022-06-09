from pydantic import BaseModel


class Item(BaseModel):
    """Model that defines a valid Item."""
    class Config:
        validate_assignment = True  # Validate new data used in updating existing items

    id: int
    name: str
