from db.redis_db import pool
import redis


class RedisNewsDao:

    # insert news info into redis
    def insert(self, news_id, title, username, news_type, content, is_top, create_time):
        con = redis.Redis(
            connection_pool=pool
        )
        try:
            data = {
                "title": title,
                "author": username,
                "news_type": news_type,
                "content": content,
                "is_top": is_top,
                "create_time": create_time
            }
            con.hset(name=news_id, mapping=data)
            if is_top == 0:
                con.expire(news_id, 24*60*60)
        except Exception as e:
            print(e)
        finally:
            del con

    # delete news info in redis
    def delete(self, news_id):
        con = redis.Redis(
            connection_pool=pool
        )
        try:
            con.delete(news_id)
        except Exception as e:
            print(e)
        finally:
            del con

