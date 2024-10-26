from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Books with id {id} not found!")

    return book


@app.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    book_db = db.query(models.Book).filter(models.Book.name == book.name).first()

    if book_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Books with name {book.name} already exists!")
    
    book_db = models.Book(**book.model_dump())

    db.add(book_db)
    db.commit()
    db.refresh(book_db)

    return {"id", book_db.id}


@app.delete("/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id)

    if not book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Books with id {id} not found!")
    
    book.delete()
    db.commit()