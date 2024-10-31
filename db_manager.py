from psycopg2.pool import SimpleConnectionPool

class Manager():
    connection_pool = SimpleConnectionPool(
        1, 20, 
        user='postgres',
        password='1707',
        host='127.0.0.1',
        database='users_profiles'
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
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);
                    """, 
                    (user_id,)
                )
                return(cursor.fetchone()[0])
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def all_users(self):
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users;
                    """
                )
                return(cursor.fetchall())
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def all_rejected_users(self) -> bool:
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE rejected = TRUE;
                    """
                )
                return(cursor.fetchall())
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def all_accepted_users(self) -> bool:
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE accepted = TRUE;
                    """
                )
                return(cursor.fetchall())
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def user_accepted(self, user_id: int) -> bool:
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT accepted FROM users WHERE user_id = %s;
                    """, 
                    (user_id,)
                )
                return(cursor.fetchone()[0])
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def new_user(self, user_id: int, first_name: str, last_name: str, age: int, gender_female: bool, rejected=False):
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (user_id, first_name, last_name, age, gender_female, accepted, rejected) VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, 
                    (user_id, first_name, last_name, age, gender_female, False, rejected,)
                )
                print("[INFO] Succesfully upload data:", user_id, first_name, last_name, age, gender_female)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def get_user(self, user_id: int):
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE user_id = %s
                    """, 
                    (user_id,)
                )
                return cursor.fetchall()[0]
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def get_user_by_param(self, param_name: str, param_value):
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT * FROM users WHERE {param_name} = %s
                    """, 
                    (param_value,)
                )
                return cursor.fetchall()
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)

    def update_app_status(self, user_id: int, param_name: str, param_value: bool):
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE users SET {param_name} = %s WHERE user_id = %s;
                    """, 
                    (param_value, user_id,)
                )
                print("[INFO] Succesfully upload data:", param_name, param_value, user_id)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            self.release_db_connection(conn)
