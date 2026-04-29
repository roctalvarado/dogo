from enums.value_permission import ValuePermission
import pymysql
from persistence.db import get_connection

class Permission():
    def __init__(self, id: int, value: ValuePermission):
        self.id = id
        self.value = value

    def get_permissions_by_id(id_user: int):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, value FROM permission WHERE id_user = %s"

            cursor.execute(sql, (id_user,))

            rs = cursor.fetchall()

            cursor.close()
            connection.close()

            permissions = []
            for r in rs:
                permissions.append(
                    Permission(
                        r["id"], 
                        ValuePermission(r["value"])))
                
            return permissions
        except Exception as e:
            print(f"Error obteniendo permisos: {e}")
            return []