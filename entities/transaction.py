from datetime import datetime
from enums.transaction_type import TransactionType
from persistence.db import get_connection
import pymysql

class Transaction():
    def __init__(self, id: int, description: str, date: datetime, 
                 amount: float, type: TransactionType):
        self.id = id
        self.description = description
        self.date = date
        self.amount = amount
        self.type = type

    @classmethod
    def get_transactions_by_account(cls, account_id: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, description, date, amount, type FROM transaction WHERE id_account = %s ORDER BY date DESC"

            cursor.execute(sql, (account_id,))
            rows = cursor.fetchall()

            transactions = []
            
            for row in rows:
                transaction = cls(
                    id=row['id'],
                    description=row['description'],
                    date=row['date'],
                    amount=row['amount'],
                    type=TransactionType(row['type']) 
                )
                transactions.append(transaction)

            cursor.close()
            connection.close()

            return transactions
            
        except Exception as e:
            print(f"Error obteniendo transacciones: {e}")
            return []