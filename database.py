from sqlmodel import Session, create_engine
from sqlmodel import SQLModel


DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

# Dependency function to get the database session
def get_session() -> Session:
    with Session(engine) as session:
        yield session
