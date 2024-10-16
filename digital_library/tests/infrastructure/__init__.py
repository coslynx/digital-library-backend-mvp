from infrastructure.database import initialize_database
from infrastructure.config import settings

def initialize_infrastructure():
    initialize_database()