from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from sqlalchemy.orm import Session


DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost/escoladb"

engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessão vinculada ao engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Retorna uma classe base para modelos declarativos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
