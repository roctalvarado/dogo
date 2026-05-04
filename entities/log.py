from datetime import datetime

import pymysql
from entities.user import User
from enums.log_type import LogType
from persistence.db import get_connection


class Log:
    def __init__(self, id: int, date: datetime, user: User,
                 description: str, type: LogType):
        self.id = id
        self.date = date
        self.user = user
        self.description = description
        self.type = type

    def saveLog(user: User, description: str, type: LogType):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = "INSERT INTO log (id_user, description, type, date) VALUES (%s, %s, %s, %s)"

            cursor.execute(sql, (user.id, description, type.value, datetime.now()))

            connection.commit()

            cursor.close()
            connection.close()

            return True
        except Exception as e:
            print(f"Error guardando log: {e}")
            return False
        
    @staticmethod
    def get_all():
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            # Traemos los logs junto con el nombre del usuario que hizo la acción
            sql = """
                SELECT l.id, l.date, l.description, l.type, 
                       u.id as user_id, u.name as user_name, u.email as user_email
                FROM log l
                JOIN user u ON l.id_user = u.id
                ORDER BY l.date DESC
            """
            cursor.execute(sql)
            rs = cursor.fetchall()
            
            logs = []
            for r in rs:
                # Reconstruimos un usuario parcial para asociarlo al log
                user = User(r["user_id"], r["user_name"], r["user_email"], "", None, [], True)
                logs.append(Log(r["id"], r["date"], user, r["description"], LogType(r["type"])))
                
            return logs
        except Exception as e:
            print(f"Error obteniendo logs: {e}")
            return []
        finally:
            cursor.close()
            connection.close()