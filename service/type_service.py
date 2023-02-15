from db.type_dao import TypeDao


class TypeService:
    __type_dao = TypeDao()

    # search news type list
    def search_type_list(self) -> list:
        res = self.__type_dao.search_type_list()
        return res

