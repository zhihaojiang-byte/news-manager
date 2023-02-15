import os
import sys
import time

from colorama import Fore, Style
from getpass import getpass

from service.user_service import UserService
from service.news_service import NewsService
from service.role_service import RoleService
from service.type_service import TypeService

__user_service = UserService()
__news_service = NewsService()
__role_service = RoleService()
__type_service = TypeService()


while True:
    os.system("cls")
    print(Fore.LIGHTBLUE_EX, "\n\t=========================================")
    print(Fore.LIGHTBLUE_EX, "\n\tWelcome to News Management System")
    print(Fore.LIGHTBLUE_EX, "\n\t=========================================")
    print(Fore.LIGHTGREEN_EX, "\n\t1. Login")
    print(Fore.LIGHTGREEN_EX, "\n\t2. Exit")
    print(Style.RESET_ALL)
    opt = input("\n\tChoose an option: ")

    if opt == '1':
        current_username = input("\n\tUsername: ")
        password = getpass("\n\tPassword: ")
        result = __user_service.login(username=current_username, password=password)

        if result:
            current_user_role = __user_service.search_user_role(username=current_username)

            while True:
                os.system("cls")
                if current_user_role == "editor":
                    print(Fore.LIGHTGREEN_EX, "\n\t1. Publish news")
                    print(Fore.LIGHTGREEN_EX, "\n\t2. Edit news")
                    print(Fore.LIGHTRED_EX, "\n\tback. Logout")
                    print(Fore.LIGHTRED_EX, "\n\texit. Exit")
                    print(Style.RESET_ALL)

                    opt = input("\n\tChoose an option: ")

                    if opt == "1":
                        os.system("cls")

                        title = input("\n\tTitle: ")
                        current_user_id = __user_service.search_user_id(username=current_username)
                        type_list = __type_service.search_type_list()
                        for index in range(len(type_list)):
                            one = type_list[index]
                            print(Fore.LIGHTBLUE_EX, f"\n\t{index + 1}. {one[1]}")
                        print(Style.RESET_ALL)
                        opt = input("\n\tplease input the news type number: ")
                        if not (opt.isdigit() and 1 <= int(opt) <= len(type_list)):
                            print("\n\tInput invalid. (going back in 3 seconds)")
                            time.sleep(3)
                            continue
                        type_id = type_list[int(opt) - 1][0]

                        path = input("\n\tplease input file path: ")
                        try:
                            with open(path, "r") as f:
                                content = f.read()
                        except Exception as e:
                            print(f"\n\t{e}")
                            print("\n\tInput invalid. (going back in 3 seconds)")
                            time.sleep(3)
                            continue

                        opt = input("\n\tPlease input top level (0-5): ")
                        if not (opt.isdigit() and 0 <= int(opt) <= 5):
                            print("\n\tInput invalid. (going back in 3 seconds)")
                            time.sleep(3)
                            continue
                        is_top = int(opt)

                        __news_service.insert_news(title, current_user_id, type_id, content, is_top)

                        print("\n\tNews saved. (going back in 3 seconds)")
                        time.sleep(3)

                    elif opt == "2":
                        page_number = 1

                        while True:
                            pages_count = __news_service.search_news_pages()
                            news_list = __news_service.search_news_list(page=page_number)

                            os.system("cls")
                            news_count_current_page = len(news_list)

                            if news_count_current_page == 0:
                                if page_number > 1:
                                    page_number -= 1
                                    continue
                                elif page_number == 1:
                                    print(Fore.LIGHTBLUE_EX, "\n\t( news list is empty )")

                            for index in range(news_count_current_page):
                                print(Fore.LIGHTGREEN_EX, f"\n\t{index + 1}. {news_list[index][1]} "
                                                          f"{news_list[index][2]} {news_list[index][3]}")
                            print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                            print(Fore.LIGHTBLUE_EX, f"\n\t{page_number}/{pages_count}")
                            print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                            if page_number > 1:
                                print(Fore.LIGHTRED_EX, "\n\tprev. Previous page")
                            if page_number < pages_count:
                                print(Fore.LIGHTRED_EX, "\n\tnext. Next page")
                            print(Fore.LIGHTRED_EX, "\n\tback. Go back")

                            opt = input("\n\tChoose an option or \n\tinput the news title number to edit: ")

                            if opt.isdigit() and 1 <= int(opt) <= news_count_current_page:
                                news_id = news_list[int(opt) - 1][0]

                                os.system("cls")
                                print(Style.RESET_ALL)
                                title = input("\n\tTitle: ")
                                type_list = __type_service.search_type_list()
                                for index in range(len(type_list)):
                                    one = type_list[index]
                                    print(Fore.LIGHTBLUE_EX, f"\n\t{index + 1}. {one[1]}")
                                print(Style.RESET_ALL)
                                opt = input("\n\tplease input the news type number: ")
                                if not (opt.isdigit() and 1 <= int(opt) <= len(type_list)):
                                    print("\n\tInput invalid. (going back in 3 seconds)")
                                    time.sleep(3)
                                    continue
                                type_id = type_list[int(opt) - 1][0]

                                path = input("\n\tplease input file path: ")
                                try:
                                    with open(path, "r") as f:
                                        content = f.read()
                                except Exception as e:
                                    print(f"\n\t{e}")
                                    print("\n\tInput invalid. (going back in 3 seconds)")
                                    time.sleep(3)
                                    continue

                                opt = input("\n\tPlease input top level (0-5): ")
                                if not (opt.isdigit() and 0 <= int(opt) <= 5):
                                    print("\n\tInput invalid. (going back in 3 seconds)")
                                    time.sleep(3)
                                    continue
                                is_top = int(opt)

                                __news_service.update_news(news_id, title, type_id, content, is_top)

                                print("\n\tNews updated. (going back in 3 seconds)")
                                time.sleep(3)

                            elif opt == "next" and page_number < pages_count:
                                page_number += 1
                            elif opt == "prev" and page_number > 1:
                                page_number -= 1
                            elif opt == "back":
                                break
                    elif opt == "back":
                        break
                    elif opt == "exit":
                        sys.exit(0)
                    else:
                        pass

                elif current_user_role == "admin":
                    print(Fore.LIGHTGREEN_EX, "\n\t1. News Management")
                    print(Fore.LIGHTGREEN_EX, "\n\t2. User Management")
                    print(Fore.LIGHTRED_EX, "\n\tback. Logout")
                    print(Fore.LIGHTRED_EX, "\n\texit. Exit")
                    print(Style.RESET_ALL)

                    opt = input("\n\tChoose an option: ")

                    if opt == "1":

                        while True:
                            os.system("cls")
                            print(Fore.LIGHTGREEN_EX, "\n\t1. Approve pending news")
                            print(Fore.LIGHTGREEN_EX, "\n\t2. Delete news")
                            print(Fore.LIGHTRED_EX, "\n\tback. Go back")
                            print(Fore.LIGHTRED_EX, "\n\texit. Exit")
                            print(Style.RESET_ALL)

                            opt = input("\n\tChoose an option: ")

                            if opt == "1":
                                page_number = 1

                                while True:
                                    pages_count = __news_service.search_pending_news_pages()
                                    news_list = __news_service.search_pending_news_list(page=page_number)

                                    os.system("cls")
                                    news_count_current_page = len(news_list)

                                    if news_count_current_page == 0:
                                        if page_number > 1:
                                            page_number -= 1
                                            continue
                                        elif page_number == 1:
                                            print(Fore.LIGHTBLUE_EX, "\n\t( news list is empty )")

                                    for index in range(news_count_current_page):
                                        print(Fore.LIGHTGREEN_EX, f"\n\t{index+1}. {news_list[index][1]} "
                                                                  f"{news_list[index][2]} {news_list[index][3]}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    print(Fore.LIGHTBLUE_EX, f"\n\t{page_number}/{pages_count}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    if page_number > 1:
                                        print(Fore.LIGHTRED_EX, "\n\tprev. Previous page")
                                    if page_number < pages_count:
                                        print(Fore.LIGHTRED_EX, "\n\tnext. Next page")
                                    print(Fore.LIGHTRED_EX, "\n\tback. Go back")

                                    opt = input("\n\tChoose an option or \n\tinput the news title number to approve: ")

                                    if opt.isdigit() and 1 <= int(opt) <= news_count_current_page:
                                        news_id = news_list[int(opt)-1][0]
                                        __news_service.approve_pending_news(news_id)
                                        result = __news_service.search_news(news_id)

                                        title = result[0]
                                        username = result[1]
                                        news_type = result[2]
                                        content_id = result[3]
                                        content = __news_service.search_content_by_content_id(content_id)
                                        is_top = result[4]
                                        create_time = str(result[5])

                                        __news_service.cache_insert_news(news_id, title, username, news_type, content,
                                                                         is_top, create_time)

                                    elif opt == "next" and page_number < pages_count:
                                        page_number += 1
                                    elif opt == "prev" and page_number > 1:
                                        page_number -= 1
                                    elif opt == "back":
                                        break

                            elif opt == "2":
                                page_number = 1

                                while True:
                                    pages_count = __news_service.search_news_pages()
                                    news_list = __news_service.search_news_list(page=page_number)

                                    os.system("cls")
                                    news_count_current_page = len(news_list)

                                    if news_count_current_page == 0:
                                        if page_number > 1:
                                            page_number -= 1
                                            continue
                                        elif page_number == 1:
                                            print(Fore.LIGHTBLUE_EX, "\n\t( news list is empty )")

                                    for index in range(news_count_current_page):
                                        print(Fore.LIGHTGREEN_EX, f"\n\t{index+1}. {news_list[index][1]} "
                                                                  f"{news_list[index][2]} {news_list[index][3]}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    print(Fore.LIGHTBLUE_EX, f"\n\t{page_number}/{pages_count}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    if page_number > 1:
                                        print(Fore.LIGHTRED_EX, "\n\tprev. Previous page")
                                    if page_number < pages_count:
                                        print(Fore.LIGHTRED_EX, "\n\tnext. Next page")
                                    print(Fore.LIGHTRED_EX, "\n\tback. Go back")

                                    opt = input("\n\tChoose an option or \n\tinput the news title number to delete: ")

                                    if opt.isdigit() and 1 <= int(opt) <= news_count_current_page:
                                        news_id = news_list[int(opt)-1][0]
                                        __news_service.delete_news(news_id)
                                        __news_service.cache_delete_news(news_id)
                                        print(Fore.LIGHTBLUE_EX, "\n\tnews deleted. ")
                                        time.sleep(3)

                                    elif opt == "next" and page_number < pages_count:
                                        page_number += 1
                                    elif opt == "prev" and page_number > 1:
                                        page_number -= 1
                                    elif opt == "back":
                                        break
                            elif opt == "back":
                                break
                            elif opt == "exit":
                                sys.exit(0)
                            else:
                                pass

                    elif opt == "2":

                        while True:
                            os.system("cls")
                            print(Fore.LIGHTGREEN_EX, "\n\t1. Add user")
                            print(Fore.LIGHTGREEN_EX, "\n\t2. Update user")
                            print(Fore.LIGHTGREEN_EX, "\n\t3. Delete user")
                            print(Fore.LIGHTRED_EX, "\n\tback. Go back")
                            print(Fore.LIGHTRED_EX, "\n\texit. Exit")
                            print(Style.RESET_ALL)

                            opt = input("\n\tChoose an option: ")

                            if opt == "1":
                                os.system("cls")
                                username = input("\n\tUsername: ")
                                password = getpass('\n\tPassword: ')
                                re_password = getpass('\n\tRepeat password: ')
                                if password != re_password:
                                    print("\n\t2 passwords are different. (going back in 3 seconds)")
                                    time.sleep(3)
                                    continue
                                email = input("\n\temail: ")
                                role_list = __role_service.search_role_list()
                                for index in range(len(role_list)):
                                    one = role_list[index]
                                    print(Fore.LIGHTBLUE_EX, f"\n\t{index+1}. {one[1]}")
                                print(Style.RESET_ALL)
                                opt = input("\n\tplease input the role number: ")
                                if opt.isdigit() and 1 <= int(opt) <= len(role_list):
                                    role_id = role_list[int(opt)-1][0]
                                    __user_service.insert_user(username, password, email, role_id)
                                    print("\n\tUser saved. (going back in 3 seconds)")
                                    time.sleep(3)
                                else:
                                    print("\n\tInput invalid. (going back in 3 seconds)")
                                    time.sleep(3)

                            elif opt == "2":
                                page_number = 1

                                while True:
                                    pages_count = __user_service.search_user_pages()
                                    user_list = __user_service.search_user_list(page=page_number)

                                    os.system("cls")
                                    user_count_current_page = len(user_list)

                                    if user_count_current_page == 0:
                                        if page_number > 1:
                                            page_number -= 1
                                            continue
                                        elif page_number == 1:
                                            print(Fore.LIGHTBLUE_EX, "\n\t( user list is empty )")

                                    for index in range(user_count_current_page):
                                        print(Fore.LIGHTGREEN_EX, f"\n\t{index+1}. {user_list[index][1]} "
                                                                  f"{user_list[index][2]} {user_list[index][3]}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    print(Fore.LIGHTBLUE_EX, f"\n\t{page_number}/{pages_count}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    if page_number > 1:
                                        print(Fore.LIGHTRED_EX, "\n\tprev. Previous page")
                                    if page_number < pages_count:
                                        print(Fore.LIGHTRED_EX, "\n\tnext. Next page")
                                    print(Fore.LIGHTRED_EX, "\n\tback. Go back")

                                    opt = input("\n\tChoose an option or \n\tinput the user number to update: ")

                                    if opt.isdigit() and 1 <= int(opt) <= user_count_current_page:
                                        user_id = user_list[int(opt)-1][0]

                                        os.system("cls")
                                        print(Style.RESET_ALL)
                                        username = input("\n\tUsername: ")
                                        password = getpass('\n\tPassword: ')
                                        re_password = getpass('\n\tRepeat password: ')
                                        if password != re_password:
                                            print("\n\t2 passwords are different. (going back in 3 seconds)")
                                            time.sleep(3)
                                            continue
                                        email = input("\n\temail: ")
                                        role_list = __role_service.search_role_list()
                                        for index in range(len(role_list)):
                                            one = role_list[index]
                                            print(Fore.LIGHTBLUE_EX, f"\n\t{index + 1}. {one[1]}")
                                        print(Style.RESET_ALL)
                                        opt = input("\n\tplease input the role number: ")
                                        if opt.isdigit() and 1 <= int(opt) <= len(role_list):
                                            role_id = role_list[int(opt) - 1][0]
                                            __user_service.update_user(user_id, username, password, email, role_id)
                                            print("\n\tUser saved. (going back in 3 seconds)")
                                            time.sleep(3)
                                        else:
                                            print("\n\tInput invalid. (going back in 3 seconds)")
                                            time.sleep(3)
                                    elif opt == "next" and page_number < pages_count:
                                        page_number += 1
                                    elif opt == "prev" and page_number > 1:
                                        page_number -= 1
                                    elif opt == "back":
                                        break
                            elif opt == "3":
                                page_number = 1

                                while True:
                                    pages_count = __user_service.search_user_pages()
                                    user_list = __user_service.search_user_list(page=page_number)

                                    os.system("cls")
                                    user_count_current_page = len(user_list)

                                    if user_count_current_page == 0:
                                        if page_number > 1:
                                            page_number -= 1
                                            continue
                                        elif page_number == 1:
                                            print(Fore.LIGHTBLUE_EX, "\n\t( user list is empty )")

                                    for index in range(user_count_current_page):
                                        print(Fore.LIGHTGREEN_EX, f"\n\t{index+1}. {user_list[index][1]} "
                                                                  f"{user_list[index][2]} {user_list[index][3]}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    print(Fore.LIGHTBLUE_EX, f"\n\t{page_number}/{pages_count}")
                                    print(Fore.LIGHTBLUE_EX, "\n\t--------------------------")
                                    if page_number > 1:
                                        print(Fore.LIGHTRED_EX, "\n\tprev. Previous page")
                                    if page_number < pages_count:
                                        print(Fore.LIGHTRED_EX, "\n\tnext. Next page")
                                    print(Fore.LIGHTRED_EX, "\n\tback. Go back")

                                    opt = input("\n\tChoose an option or \n\tinput the user number to delete: ")

                                    if opt.isdigit() and 1 <= int(opt) <= user_count_current_page:
                                        user_id = user_list[int(opt)-1][0]
                                        __user_service.delete_user(user_id)
                                        print("\n\tUser deleted. (going back in 3 seconds)")
                                        time.sleep(3)
                                    elif opt == "next" and page_number < pages_count:
                                        page_number += 1
                                    elif opt == "prev" and page_number > 1:
                                        page_number -= 1
                                    elif opt == "back":
                                        break

                    elif opt == "back":
                        break
                    elif opt == "exit":
                        sys.exit(0)
                    else:
                        pass

                else:
                    pass

        else:
            print("\n\tIncorrect username or password. (Returning in 3 seconds)")
            time.sleep(3)

    elif opt == '2':
        sys.exit(0)
    else:
        pass

