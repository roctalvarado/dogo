from datetime import datetime
from enums.transaction_type import TransactionType
from entities.account import Account

class Transaction():
    def __init__(self, id: int, description: str, date: datetime, 
                 amount: float, type: TransactionType):
        self.id = id
        self.description = description
        self.date = date
        self.amount = amount
        self.type = type