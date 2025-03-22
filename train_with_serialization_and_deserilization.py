from pydantic import BaseModel
from enum import Enum

class ProdType(str, Enum):
    clothes = "Одежда"
    electronics = "Электроника"
    household_chemistry = "Бытовая химия"

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    product_type: ProdType

# Создаём объект
product = Product(name="Чайник", price=5000.7, in_stock="true", product_type="Электроника")

# Сериализация (Python → JSON)
json_data = product.model_dump_json()
print(json_data)


# Десериализация (JSON → Python)
new_product = Product.model_validate_json(json_data)
print(new_product.name)
