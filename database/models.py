from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from database.database import engine, Session

# Create a base class to be inherited by all models
Base = declarative_base()

# Define the Exchange model
class Exchange(Base):
    __tablename__ = 'exchanges'

    id = Column(Integer, primary_key=True)
    name = Column(String)

# Define the Stock model
class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    symbol = Column(String)
    description = Column(String)

# Define the Algorithm model
class Algorithm(Base):
    __tablename__ = 'algorithms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    parameters = Column(String)

# Define the Historical Data model
class HistoricalData(Base):
    __tablename__ = 'historical_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    stock = relationship("Stock", backref="historical_data")

# Define the Prediction model
class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'))
    predicted_price = Column(Float)
    direction = Column(String)
    stock = relationship("Stock", backref="predictions")
    algorithm = relationship("Algorithm", backref="predictions")

# Create the tables
Base.metadata.create_all(engine)
