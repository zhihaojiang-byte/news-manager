from db.mysql_db import pool
import time

from setting import MY_SQL_ENCRYPT_KEY
from setting import ITEMS_PER_PAGE


class UserDao:
    # Authenticate user by username and password
    def login(self, username, password) -> bool:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT COUNT(*) FROM t_user WHERE username=%s AND " \
                  "AES_DECRYPT(UNHEX(password), %s)=%s"
            cursor.execute(sql, (username, MY_SQL_ENCRYPT_KEY, password))
            count = cursor.fetchone()[0]
            return True if count == 1 else False
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # Query user role
    def search_user_role(self, username) -> str:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT r.role FROM t_user u JOIN t_role r ON u.role_id=r.id WHERE u.username=%s"
            cursor.execute(sql, (username, ))
            role = cursor.fetchone()[0]
            return role
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    #  insert new user
    def insert_user(self, username, password, email, role_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "INSERT INTO t_user(username, password, email, role_id) " \
                  "VALUES(%s, HEX(AES_ENCRYPT(%s, %s)), %s, %s)"
            cursor.execute(sql, (username, password, MY_SQL_ENCRYPT_KEY, email, role_id))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search user list by page number
    def search_user_list(self, page) -> list:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT u.id, u.username, u.email, r.role " \
                  "FROM t_user u JOIN t_role r ON u.role_id=r.id " \
                  "ORDER BY u.id " \
                  "LIMIT %s,%s"
            cursor.execute(sql, ((page-1)*ITEMS_PER_PAGE, ITEMS_PER_PAGE))
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search user pages count
    def search_user_pages(self):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT CEIL(COUNT(*)/%s) FROM t_user"
            cursor.execute(sql, (ITEMS_PER_PAGE, ))
            res = cursor.fetchone()[0]
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # update user info by id
    def update_user(self, user_id, username, password, email, role_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "UPDATE t_user SET username=%s, password=HEX(AES_ENCRYPT(%s, %s)), email=%s, role_id=%s WHERE id=%s"
            cursor.execute(sql, (username, password, MY_SQL_ENCRYPT_KEY, email, role_id, user_id))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # delete user by id
    def delete_user(self, user_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "DELETE FROM t_user WHERE id=%s"
            cursor.execute(sql, (user_id, ))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search user id by username
    def search_user_id(self, username) -> int:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT id FROM t_user WHERE username=%s"
            cursor.execute(sql, (username, ))
            res = cursor.fetchone()[0]
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

