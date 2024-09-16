import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Creating the DB engine based on connection string
DATABASE_URL = 'postgresql://{user}:{password}@{hostname}:{port}/{db}'.format(user = os.environ['POSTGRES_USER'],
                                                                              password = os.environ['POSTGRES_PASSWORD'],
                                                                              hostname = os.environ['POSTGRES_HOSTNAME'],
                                                                              port = os.environ['POSTGRES_PORT'],
                                                                              db = os.environ['POSTGRES_DB']
                                                                            )


engine = create_engine(DATABASE_URL)

# Creating important objects to be able to use the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()