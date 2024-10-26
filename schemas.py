from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    author: str
    no_of_pages: int | None = None


class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int