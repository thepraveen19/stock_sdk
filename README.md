STOCK_SDK tree:

<img width="318" alt="Screenshot 2023-12-23 at 02 22 59" src="https://github.com/thepraveen19/stock_sdk/assets/42544315/cb9984c4-0d1b-4d3b-b56c-f0896f4e71bb">



Stock Trading System

This is a stock trading system that uses an API to fetch data for various stocks, performs analysis on the data, 
and uses the results to buy and sell stocks. The system stores all the data in a database for future reference.

Project Structure

The project structure is organized as follows:

postgres_stock_db/ contains files related to a PostgreSQL database for storing stock data.

credentials.py: This file will store the login credentials like usernames, passwords, and other secrets.

config.py: This file will store the API endpoint URLs.

api/: contains code related to the project's API, including defining API endpoints and an API client for accessing external services.
__init__.py: This file is needed to treat api directory as a package.
endpoints.py: This file will contain the code to connect with the API, fetch data and return it to the main program.
api_client.py: This file will contain the code to make api calls

analysis/: contains code related to analyzing stock data, including various prediction algorithms.
__init__.py: This file is needed to treat analysis directory as a package.
analysis.py: This file will contain the code to analyze the data fetched from the API and create a new table with the analyzed
data.

predictions/: This folder will contain the code for different prediction algorithms.
__init__.py: This file is needed to treat predictions directory as a package.
algorithm1.py: This file will contain the code for the first prediction algorithm.
algorithm2.py: This file will contain the code for the second prediction algorithm.
algorithm3.py: This file will contain the code for the third prediction algorithm.
...: This folder can contain any number of prediction algorithm files.

trading/: contains code related to the project's trading logic.
__init__.py: This file is needed to treat trading directory as a package.
trading.py: This file will contain the code for buying and selling stocks using different strategies.

database/: contains code for interacting with the project's database, including defining models and CRUD (create, read, update, delete) operations.
__init__.py: This file is needed to treat database directory as a package.
models.py: This file will contain the SQLAlchemy model classes for the database tables.
database.py: This file will contain the code for connecting to the database, creating the tables, and inserting data into them.
crud.py: This file will contain the code for performing CRUD operations on the database, such as creating new records, retrieving existing records, updating records, and deleting records. This file will typically use the SQLAlchemy ORM (Object-Relational Mapping) to interact with the database. The CRUD operations implemented in this file will be used by other parts of the project to manage data in the database.

utils/: This folder will contain utility functions that can be used across the project.
__init__.py: This file is needed to treat utils directory as a package.
helpers.py: This file will contain the helper functions that can be used across the project.
main.py: This file will be the entry point of the program and will tie together all the different parts of the program.
logger.py: This logs everything in log.txt file. However, a seperate logger based on dates is created by fyers api by default.
README.md: This file will contain information about the project.
requirements.txt: This file will contain a list of all the required Python packages and their versions.



Installation

Clone the repository to your local machine.
Install the required packages using the following command:
pip install -r requirements.txt

Update credentials.py with your API credentials.
Usage
To run the system, simply execute the main.py script:
python main.py
The system will connect to the API, fetch data for various stocks, perform analysis on the data, and use the 
results to buy and sell stocks. All the data will be stored in the database for future reference.
