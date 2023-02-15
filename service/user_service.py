from db.user_dao import UserDao


class UserService:
    __user_dao = UserDao()

    # Authenticate user by username and password
    def login(self, username, password):
        res = self.__user_dao.login(username=username, password=password)
        return res

    # Query user role
    def search_user_role(self, username):
        res = self.__user_dao.search_user_role(username=username)
        return res

    #  insert new user
    def insert_user(self, username, password, email, role_id):
        self.__user_dao.insert_user(username, password, email, role_id)

    # search user list by page number
    def search_user_list(self, page) -> list:
        res = self.__user_dao.search_user_list(page)
        return res

    # search user pages count
    def search_user_pages(self):
        res = self.__user_dao.search_user_pages()
        if res == 0:
            res = 1
        return res

    # update user info by id
    def update_user(self, user_id, username, password, email, role_id):
        self.__user_dao.update_user(user_id, username, password, email, role_id)

    # delete user by id
    def delete_user(self, user_id):
        self.__user_dao.delete_user(user_id)

    # search user id by username
    def search_user_id(self, username) -> int:
        res = self.__user_dao.search_user_id(username)
        return res


