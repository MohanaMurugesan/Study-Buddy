from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


database_url = "postgresql://postgres:Mohana@localhost/StudyBuddy"

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False,bind=engine)

Base = declarative_base()