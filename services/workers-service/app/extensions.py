from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os


POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@postgres:5432/alertora")


Base = declarative_base()
engine = create_engine(POSTGRES_URI)
SessionLocal = sessionmaker(bind=engine)
