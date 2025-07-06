from sqlalchemy.orm import Session
from models import Product

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def add_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, db_product: Product, data: dict):
    for key, value in data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()
