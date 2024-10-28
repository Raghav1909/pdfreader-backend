from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pdf2image import convert_from_path
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

STATIC_PDF_DIR = Path("static/pdf")
STATIC_IMG_DIR = Path("static/img")
STATIC_PDF_DIR.mkdir(parents=True, exist_ok=True)
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Books with id {id} not found!",
        )

    return book


@app.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    book_db = db.query(models.Book).filter(models.Book.name == book.name).first()

    if book_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Books with name {book.name} already exists!",
        )

    book_db = models.Book(**book.model_dump())

    db.add(book_db)
    db.commit()
    db.refresh(book_db)

    return {"id": book_db.id}


@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id)

    if not book.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Books with id {id} not found!",
        )

    book.delete()
    db.commit()


@app.get("/{id}/pdf", status_code=status.HTTP_200_OK)
def get_book_pdf(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found"
        )

    pdf_paths = []

    for i in range(1, book.no_of_pages + 1):
        pdf_paths.append(f"{STATIC_IMG_DIR}/{book.id}/page_{i}.jpg")

    return {"paths": pdf_paths}


@app.post("/{id}/pdf", status_code=status.HTTP_201_CREATED)
async def create_book_pdf(
    id: int, pdf_file: UploadFile = File(...), db: Session = Depends(get_db)
):
    book_db = db.query(models.Book).filter(models.Book.id == id).first()

    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {id} not found!",
        )

    pdf_file_path = (
        STATIC_PDF_DIR / f"{book_db.id}_{book_db.name.lower().replace(" ", "_")}.pdf"
    )
    with open(pdf_file_path, "wb") as file:
        content = await pdf_file.read()
        file.write(content)

    img_dir = STATIC_IMG_DIR / str(book_db.id)
    img_dir.mkdir(parents=True, exist_ok=True)

    try:
        images = convert_from_path(str(pdf_file_path).replace("\\", "/"))

        # Save each page as a separate JPG image in the img_dir
        for idx, image in enumerate(images):
            img_path = img_dir / f"page_{idx + 1}.jpg"
            image.save(img_path, "JPEG")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting PDF to images: {str(e)}",
        )

    book_db.pdf_path = str(pdf_file_path)
    db.commit()
    db.refresh(book_db)
