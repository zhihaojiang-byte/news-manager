from db.mongo_db import client
from bson.objectid import ObjectId


class MongoNewsDao:
    # insert news content and into mongodb and return its _id
    def insert(self, content):
        try:
            insert = client.news_management_system.new_content.insert_one({"content": content})
            return str(insert.inserted_id)
        except Exception as e:
            print(e)

    # update news content by content_id
    def update(self, content_id, content):
        try:
            client.news_management_system.new_content.update_one(
                {"_id": ObjectId(content_id)},
                {"$set": {"content": content}}
            )
        except Exception as e:
            print(e)

    # read news content by content_id
    def read(self, content_id):
        try:
            find = client.news_management_system.new_content.find_one({"_id": ObjectId(content_id)})
            return find["content"]
        except Exception as e:
            print(e)

    # delete news by content_id
    def delete(self, content_id):
        try:
            client.news_management_system.new_content.delete_one({"_id": ObjectId(content_id)})
        except Exception as e:
            print(e)


