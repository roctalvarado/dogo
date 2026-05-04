from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from enums.profile import Profile
from entities.permission import Permission
from flask_login import UserMixin

class User (UserMixin):
    def __init__(self, id: int, name:str, email:str, password:str, profile: Profile, permissions: list, is_active: bool):
        self.id= id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.permissions = permissions
        self._is_active = is_active

    @property
    def is_active(self):
        return self._is_active
    
    def check_email_exists(email) -> bool:
        """
            Verifica si la cuenta de correo electrónico ya se encuentra registrada.

            Parameters:
                email (str): Correo electrónico a validar.

            Returns:
                bool: True si el correo ya se encunetra registrado; de lo contrario, False.
        """
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT email from user WHERE email = %s"
        cursor.execute(sql, (email,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row is not None
        
    def save(name: str, email:str, password:str) -> bool:
        """
            Guarda un registro de usuario en la base de datos

            Parameters:
                name (str): Nombre del usuario.
                email (str): Correo electrónico del usuario.
                password (str): Contraseña del usuario en texto plano.

            Returns:
                bool: True si la cuenta se guardó correctamente; de lo contrario, False.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor()
            hash_password = generate_password_hash(password)

            sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, hash_password, 2, True))
            connection.commit()

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving user:{ex}")
            return False
        
    def check_login(email, password):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, name, email, password, is_active, profile FROM user WHERE email = %s"
            cursor.execute(sql, (email,))

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user and check_password_hash(user["password"], password):
                permissions = Permission.get_permissions_by_id(user["id"])

                is_active = user["is_active"] == b'\x01' if user["is_active"] is not None else False

                return User(
                    user["id"],
                    user["name"],
                    user["email"],
                    "",
                    Profile(user["profile"]),
                    permissions,
                    is_active
                )

            return None
        except Exception as ex:
            print(f"Error logging in user:{ex}")
            return False
        
    def get_by_id(id):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, name, email, password, is_active, profile FROM user WHERE id = %s"
            cursor.execute(sql, (id,))

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                
                permissions = Permission.get_permissions_by_id(user["id"])
                is_active = user["is_active"] == b'\x01' if user["is_active"] is not None else False
                return User(
                    user["id"],
                    user["name"],
                    user["email"],
                    user["password"],
                    Profile(user["profile"]),
                    permissions,
                    is_active
                )

            return None
        except Exception as ex:
            print(f"Error:{ex}")
            return False
        
    @staticmethod
    def get_all():
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, name, email, is_active, profile FROM user"
            cursor.execute(sql)
            rs = cursor.fetchall()
            
            users = []
            for r in rs:
                is_active = r["is_active"] == b'\x01' if r["is_active"] is not None else False
                users.append(User(
                    r["id"],
                    r["name"],
                    r["email"],
                    "",
                    Profile(r["profile"]),
                    [], # Lista de permisos vacía para optimizar el listado general
                    is_active
                ))
            return users
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
            return []
        finally:
            cursor.close()
            connection.close()