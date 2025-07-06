from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://dava_bayer:kIa41WLPqldniK2zKCwTbKP7sG4ud3KP@dpg-d1l431er433s73d86e70-a/dava_bayer"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
