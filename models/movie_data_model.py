from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from enum import Enum

from models.user_data_model import FullNameUser


class Locations(str, Enum):
    MSK = "MSK"
    SPB = "SPB"

class CreatedAt(str, Enum):
    asc = "asc"
    desc = "desc"

class MovieFilters(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    pageSize: int = Field(default=10, gt=0)
    page: int = Field(default=1, gt=0)
    minPrice: Optional[int] = Field(default=None, gt=0)
    maxPrice: Optional[int] = Field(default=None, gt=0)
    locations: Optional[Union[list[Locations], Locations]] = None
    published: Optional[bool] = None
    genreId: Optional[int] = None
    createdAt: Optional[CreatedAt] = None

    @field_validator("locations", mode="before")
    def validate_locations(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = [value]
        if not all(item in Locations.__members__ for item in value):
            raise ValueError("Допустимые значения для locations: MSK, SPB")
        return [Locations(item) for item in value]

    @field_validator("maxPrice")
    def min_and_max_price_relationship(cls, value: int, info) -> int:
        if "minPrice" in info.data and info.data["minPrice"] is not None and value < info.data["minPrice"]:
            raise ValueError("Минимальная цена должна быть меньше максимальной")
        return value

class Genre(BaseModel):
    name: str

class Movie(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    genreId: int
    imageUrl: Optional[str] = None
    price: float
    rating: Optional[float] = None
    location: Locations
    published: bool
    createdAt: str
    genre: Genre

from typing import List

class MovieResponse(BaseModel):
    movies: List[Movie]
    count: int
    page: int
    pageSize: int
    pageCount: int

class OptionalMovie(Movie):
    # Явно переопределяем только обязательные поля
    id: Optional[int] = None
    name: Optional[str] = None
    genre: Optional[int] = None
    price: Optional[float] = None
    location: Optional[Union[list[Locations], Locations]] = None
    published: Optional[bool] = None
    createdAt: Optional[str] = None

class Reviews(BaseModel):
    userId: str
    text: str
    rating: int
    createdAt: str
    user: FullNameUser

class MovieForID(Movie):
    reviews: Optional[list[Reviews]] = []