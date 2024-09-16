from app.db import DATABASE_URL
from app.models.db import Base

from sqlalchemy import create_engine

import time


print("Starting engine to create all the tables in the database...")

# Waiting a few seconds to start connection with DB, it might not be ready yet
time.sleep(3)
engine = create_engine(DATABASE_URL)

# This line creates the tables in the database based on the ORM model definitions
Base.metadata.create_all(engine)