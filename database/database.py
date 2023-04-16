from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from database.postgres_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Construct the path to the database
project_dir = os.getcwd()  # get the current working directory
db_path = os.path.join(project_dir, 'postgres_stock_db')

# # Create the engine
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')  # enable logging

Session = sessionmaker(bind=engine)

