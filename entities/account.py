from datetime import datetime
from entities.user import User
from entities.transaction import Transaction
from persistence.db import get_connection
import pymysql

class Account():
    def __init__(self, id: int, number: str, creation_date: datetime, user: User, transactions: list):
        self.id = id
        self.number = number
        self.creation_date = creation_date
        self.user = user
        self.transactions = transactions

    def get_account_by_id(id_user: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, number, creation_date, id_user FROM account WHERE id_user = %s"

            cursor.execute(sql, (id_user,))

            rs = cursor.fetchone()

            user = User.get_by_id(rs["id_user"])

            transactions = Transaction.get_transactions_by_account(rs["id"])

            account = Account(
                rs["id"],
                rs["number"],
                rs["creation_date"],
                user,
                transactions
            )

            cursor.close()
            connection.close()

            return account
        except:
            pass
    
    """
    
    def get_balance(account_id):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT SUM(CASE WHEN type = 1 THEN amount ELSE -amount END) as balance FROM transaction WHERE id_account = %s"

        cursor.execute(sql, (account_id,))

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        
        # Si no hay transacciones
        if result['balance'] == None:
            return 0.0
        else:
            return result['balance']
        
    def get_transactions(account_id):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT id, description, date, amount, type FROM transaction WHERE id_account = %s ORDER BY date"

        cursor.execute(sql, (account_id,))

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        return transactions """