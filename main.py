from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import shutil
import os
import uuid
import uvicorn
from database import SessionLocal, engine, Base
from models import Product
from crud import get_all_products, get_product, add_product, update_product, delete_product

# Ініціалізація бази (створення таблиць)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Папка для статичних файлів (картинки)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Залежність: отримання сесії БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Головна сторінка зі списком товарів
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    products = get_all_products(db)
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

# Форма додавання товару
@app.get("/add", response_class=HTMLResponse)
async def add_form(request: Request):
    categories = ['Штани', 'Худі', 'Шорти', 'Взуття', 'Аксесуари', 'Шапки', 'Рукавиці', 'Куртки / Жилетки', 'Футболки']
    return templates.TemplateResponse("add_product.html", {"request": request, "categories": categories})

# Обробка форми додавання товару
@app.post("/add")
async def add_product_post(
    request: Request,
    category: str = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid.uuid4().hex}_{photo.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    photo_url = f"/static/uploads/{filename}"

    product = Product(category=category, name=name, description=description, price=price, photo=photo_url)
    add_product(db, product)

    return RedirectResponse(url="/", status_code=303)

# Форма редагування товару
@app.get("/edit/{product_id}", response_class=HTMLResponse)
async def edit_form(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
    categories = ['Штани', 'Худі', 'Шорти', 'Взуття', 'Аксесуари', 'Шапки', 'Рукавиці', 'Куртки / Жилетки', 'Футболки']
    return templates.TemplateResponse("edit_product.html", {"request": request, "product": product, "categories": categories})

# Обробка редагування товару
@app.post("/edit/{product_id}")
async def edit_product_post(
    product_id: int,
    category: str = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    photo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")

    if photo and photo.filename != "":
        filename = f"{uuid.uuid4().hex}_{photo.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        photo_url = f"/static/uploads/{filename}"
    else:
        photo_url = product.photo

    update_product(db, product, {
        "category": category,
        "name": name,
        "description": description,
        "price": price,
        "photo": photo_url
    })

    return RedirectResponse(url="/", status_code=303)

# Видалення товару
@app.get("/delete/{product_id}")
async def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не знайдено")
    delete_product(db, product)
    return RedirectResponse(url="/", status_code=303)

@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не знайдено")
    return FileResponse(file_path)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
