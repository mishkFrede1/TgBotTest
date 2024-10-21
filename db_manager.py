from psycopg2.pool import SimpleConnectionPool
from datetime import time
from datetime import date

class Manager():
    connection_pool = SimpleConnectionPool(
        1, 20, 
        user='postgres',
        password='1707',
        host='127.0.0.1',
        database='grim_team'
    )

    def get_connection_from_pool(self) -> any:
        """
        Return connection from the pool of DB.

        :return:
        """
        try:
            conn = self.connection_pool.getconn()
            return conn
        
        except Exception as _ex:
            print("[ERROR]", _ex)
            return None
        
    def put_connection_in_pool(self, conn):
        """
        Return connection back in the pool of DB.
        """
        try:
            self.connection_pool.putconn(conn)

        except Exception as _ex:
            print("[ERROR]", _ex)

    def release_db_connection(self, conn):
        try:
            self.connection_pool.putconn(conn)

        except Exception as _ex:
            print("[ERROR]:", _ex)

    def user_exists(self, user_id: int) -> bool:
        """
        Checks if the user is in the Database by his Telegram ID.

        :param user_id: User's Telegram ID.
        :return:
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);
                    """, 
                    (user_id,)
                )
                exists = cursor.fetchone()[0]
                return(exists)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def new_user(self, user_id: int, first_name: str, login: str, password: str):
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (user_id, first_name, login, password) VALUES (%s, %s, %s, %s)
                    """, 
                    (user_id, first_name, login, password,)
                )
                print("[INFO] Succesfully upload data:", user_id, first_name, login, password)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_login_password(self, user_id: int):
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE user_id = %s
                    """, 
                    (user_id,)
                )
                return cursor.fetchall()
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_grades_cards(self, user_id: int, grades_cards):
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET grades_cards = %s WHERE user_id = %s;
                    """, 
                    (grades_cards, user_id,)
                )
                print("[INFO] Succesfully upload data:", grades_cards, user_id)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_exams_cards(self, user_id: int, exams_cards):
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET exams_cards = %s WHERE user_id = %s;
                    """, 
                    (exams_cards, user_id,)
                )
                print("[INFO] Succesfully upload data:", exams_cards, user_id)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)
