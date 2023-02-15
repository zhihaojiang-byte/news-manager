from db.mysql_db import pool


class TypeDao:
    # search news type list
    def search_type_list(self) -> list:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT id, type FROM t_type ORDER BY id"
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

