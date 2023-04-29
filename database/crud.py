# from sqlalchemy.orm import Session
from database.models import Exchange, Stock, Algorithm, HistoricalData, Prediction
from datetime import datetime
from database.database import Session


class ExchangeCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_exchange(self, name: str) -> Exchange:
        exchange = Exchange(name=name)
        self.session.add(exchange)
        self.session.commit()
        return exchange

    def read_exchange(self, exchange_id: int) -> Exchange:
        exchange = self.session.query(Exchange).filter(Exchange.id == exchange_id).one()
        return exchange

    def update_exchange(self, exchange_id: int, name: str) -> Exchange:
        exchange = self.session.query(Exchange).filter(Exchange.id == exchange_id).one()
        exchange.name = name
        self.session.commit()
        return exchange

    def delete_exchange(self, exchange_id: int):
        self.session.query(Exchange).filter(Exchange.id == exchange_id).delete()
        self.session.commit()

class StockCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_stock(self, name: str, symbol: str, description: str) -> Stock:
        stock = Stock(name=name, symbol=symbol, description=description)
        self.session.add(stock)
        self.session.commit()
        return stock

    def read_stock(self, stock_id: str) -> Stock:
        stock = self.session.query(Stock).filter(Stock.id == stock_id).one()
        return stock

    def update_stock(self, stock_id: str, name: str, symbol: str, description: str) -> Stock:
        stock = self.session.query(Stock).filter(Stock.id == stock_id).one()
        stock.name = name
        stock.symbol = symbol
        stock.description = description
        self.session.commit()
        return stock

    def delete_stock(self, stock_id: str):
        self.session.query(Stock).filter(Stock.id == stock_id).delete()
        self.session.commit()



class AlgorithmCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_algorithm(self, name: str, description: str, parameters: str) -> Algorithm:
        algorithm = Algorithm(name=name, description=description, parameters=parameters)
        self.session.add(algorithm)
        self.session.commit()
        return algorithm

    def read_algorithm(self, algorithm_id: int) -> Algorithm:
        algorithm = self.session.query(Algorithm).filter(Algorithm.id == algorithm_id).one()
        return algorithm

    def update_algorithm(self, algorithm_id: int, name: str, description: str, parameters: str) -> Algorithm:
        algorithm = self.session.query(Algorithm).filter(Algorithm.id == algorithm_id).one()
        algorithm.name = name
        algorithm.description = description
        algorithm.parameters = parameters
        self.session.commit()
        return algorithm

    def delete_algorithm(self, algorithm_id: int):
        self.session.query(Algorithm).filter(Algorithm.id == algorithm_id).delete()
        self.session.commit()

class HistoricalDataCRUD:
    def __init__(self):
        self.session = Session()

    def read_historical_data(self, symbol: str = None):
        if symbol:
            historical_data = self.session.query(HistoricalData).join(Stock).filter(Stock.symbol == symbol).all()
        else:
            historical_data = self.session.query(HistoricalData).all()
        return historical_data

    def update_historical_data(self, historical_data_id: int, timestamp: datetime = None, stock_id: int = None,
                               open_price: float = None, high_price: float = None, low_price: float = None,
                               close_price: float = None, volume: float = None) -> HistoricalData:
        historical_data = self.session.query(HistoricalData).filter(HistoricalData.id == historical_data_id).first()

        if timestamp is not None:
            historical_data.timestamp = timestamp

        if stock_id is not None:
            historical_data.stock_id = stock_id

        if open_price is not None:
            historical_data.open_price = open_price

        if high_price is not None:
            historical_data.high_price = high_price

        if low_price is not None:
            historical_data.low_price = low_price

        if close_price is not None:
            historical_data.close_price = close_price

        if volume is not None:
            historical_data.volume = volume

        self.session.commit()
        return historical_data

    def delete_historical_data(self, historical_data_id: int) -> None:
        historical_data = self.session.query(HistoricalData).filter(HistoricalData.id == historical_data_id).first()
        self.session.delete(historical_data)
        self.session.commit()
