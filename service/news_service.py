from db.news_dao import NewsDao
from db.redis_news_dao import RedisNewsDao
from db.mongo_news_dao import MongoNewsDao


class NewsService:
    __news_dao = NewsDao()
    __redis_news_dao = RedisNewsDao()
    __mongodb_news_dao = MongoNewsDao()

    # search pending news list by page number
    def search_pending_news_list(self, page) -> list:
        res = self.__news_dao.search_pending_news_list(page)
        return res

    # search pending news pages count
    def search_pending_news_pages(self) -> int:
        res = self.__news_dao.search_pending_news_pages()
        if res == 0:
            res = 1
        return res

    # update status of new from pending to approved
    def approve_pending_news(self, news_id):
        self.__news_dao.approve_pending_news(news_id=news_id)

    # search news list by page number
    def search_news_list(self, page) -> list:
        res = self.__news_dao.search_news_list(page)
        return res

    # search news pages count
    def search_news_pages(self):
        res = self.__news_dao.search_news_pages()
        if res == 0:
            res = 1
        return res

    # delete news content in mongodb first, then delete the news info
    def delete_news(self, news_id):
        content_id = self.__news_dao.search_news_content_id(news_id)
        self.__news_dao.delete_news(news_id)
        self.__mongodb_news_dao.delete(content_id)

    #  insert new news to mySQL and its content to mongodb
    def insert_news(self, title, editor_id, type_id, content, is_top):
        content_id = self.__mongodb_news_dao.insert(content)
        self.__news_dao.insert_news(title, editor_id, type_id, content_id, is_top)

    # search news info by news_id
    def search_news(self, news_id) -> list:
        res = self.__news_dao.search_news(news_id)
        return res

    # insert news info into redis
    def cache_insert_news(self, news_id, title, username, news_type, content, is_top, create_time):
        self.__redis_news_dao.insert(news_id, title, username, news_type, content, is_top, create_time)

    # delete news info in redis
    def cache_delete_news(self, news_id):
        self.__redis_news_dao.delete(news_id)

    # update news content in mongodb , update news info in mySQL then remove it form redis
    def update_news(self, news_id, title, type_id, content, is_top):
        content_id = self.__news_dao.search_news_content_id(news_id)
        self.__mongodb_news_dao.update(content_id, content)
        self.__news_dao.update_news(news_id, title, type_id, content_id, is_top)
        self.cache_delete_news(news_id)

    # search news content_id by news_id
    def search_news_content_id(self, news_id):
        res = self.__news_dao.search_news_content_id(news_id)
        return res

    # read news content by content_id
    def search_content_by_content_id(self, content_id):
        res = self.__mongodb_news_dao.read(content_id)
        return res


