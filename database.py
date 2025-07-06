from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://dava_bayer:oRHlidY8IDrDAfx0MTaYgFqfa4QCCZdM@dpg-d1ldt5h5pdvs73bsf0pg-a/dava_bayer_87zd"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
