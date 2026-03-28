from persistence.db import get_connection
import pymysql

class Account:
    def get_by_user_id(user_id):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT id, number, creation_date FROM account WHERE id_user = %s"

        cursor.execute(sql, (user_id,))

        account = cursor.fetchone()

        cursor.close()
        connection.close()

        return account
    
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
            return['balance']
        
    def get_transactions(account_id):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT id, description, date, amount, type FROM transaction WHERE id_account = %s ORDER BY date DESC"

        cursor.execute(sql, (account_id,))

        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        return transactions