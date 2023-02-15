from db.mysql_db import pool

from setting import ITEMS_PER_PAGE


class NewsDao:
    # search pending news list by page number
    def search_pending_news_list(self, page) -> list:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT n.id, n.title, t.type, u.username " \
                  "FROM t_news n JOIN t_type t ON n.type_id=t.id " \
                  "JOIN t_user u ON n.editor_id=u.id " \
                  "WHERE n.state=%s " \
                  "ORDER BY n.create_time DESC " \
                  "LIMIT %s,%s"
            cursor.execute(sql, ("pending", (page-1)*ITEMS_PER_PAGE, ITEMS_PER_PAGE))
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search pending news pages count
    def search_pending_news_pages(self):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT CEIL(COUNT(*)/%s) FROM t_news WHERE state=%s"
            cursor.execute(sql, (ITEMS_PER_PAGE, "pending"))
            res = cursor.fetchone()[0]
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # update status of new from pending to approved
    def approve_pending_news(self, news_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "UPDATE t_news SET state=%s WHERE id=%s"
            cursor.execute(sql, ("approved", news_id))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search news list by page number
    def search_news_list(self, page) -> list:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT n.id, n.title, t.type, u.username " \
                  "FROM t_news n JOIN t_type t ON n.type_id=t.id " \
                  "JOIN t_user u ON n.editor_id=u.id " \
                  "ORDER BY n.create_time DESC " \
                  "LIMIT %s,%s"
            cursor.execute(sql, ((page-1)*ITEMS_PER_PAGE, ITEMS_PER_PAGE))
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search news pages count
    def search_news_pages(self):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT CEIL(COUNT(*)/%s) FROM t_news"
            cursor.execute(sql, (ITEMS_PER_PAGE, ))
            res = cursor.fetchone()[0]
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # delete news by id
    def delete_news(self, news_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "DELETE FROM t_news WHERE id=%s"
            cursor.execute(sql, (news_id, ))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    #  insert new news
    def insert_news(self, title, editor_id, type_id, content_id, is_top):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "INSERT INTO t_news(title, editor_id, type_id, content_id, is_top, state) " \
                  "VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (title, editor_id, type_id, content_id, is_top, "pending"))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search news info by news_id
    def search_news(self, news_id) -> list:
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT n.title, u.username, t.type, n.content_id, n.is_top, n.create_time " \
                  "FROM t_news n JOIN t_type t ON n.type_id=t.id " \
                  "JOIN t_user u ON n.editor_id=u.id " \
                  "WHERE n.id=%s "
            cursor.execute(sql, (news_id, ))
            res = cursor.fetchone()
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # update news info by news_id
    def update_news(self, news_id, title, type_id, content_id, is_top):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "UPDATE t_news SET title=%s, type_id=%s, content_id=%s, is_top=%s, state=%s, update_time=NOW() " \
                  "WHERE id=%s"
            cursor.execute(sql, (title, type_id, content_id, is_top, "pending", news_id))
            con.commit()
        except Exception as e:
            if "con" in dir():
                con.rollback()
            print(e)
        finally:
            if "con" in dir():
                con.close()

    # search news content_id by news_id
    def search_news_content_id(self, news_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT content_id FROM t_news WHERE id=%s"
            cursor.execute(sql, (news_id, ))
            res = cursor.fetchone()[0]
            return res
        except Exception as e:
            print(e)
        finally:
            if "con" in dir():
                con.close()
