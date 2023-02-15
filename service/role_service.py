from db.role_dao import RoleDao


class RoleService:
    __role_dao = RoleDao()

    # search role list
    def search_role_list(self) -> list:
        res = self.__role_dao.search_role_list()
        return res



