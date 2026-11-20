
from .database import Database
from .connect import DatabaseConnection

database = Database()
db = DatabaseConnection(database)
