# this script downloads profile picture of a person from instagram

import click
import os
import pickle
import urllib.request
from lxml import html
from bs4 import BeautifulSoup
import webbrowser
from pyfiglet import Figlet

os.system('clear')


def pickle_file_load(name):
    file = open(name, "rb")
    file1 = pickle.load(file)
    file.close()
    return file1


def pickle_file_dump(name, dic):
    file = open(name, "wb")
    pickle.dump(dic, file)
    file.close()


def get_url(username):
    url = "https://www.instagram.com/" + username + '/'
    page = (urllib.request.urlopen(url).read())
    soup = BeautifulSoup(page, 'html.parser')
    value = (soup.find_all('meta', property="og:image")[0])
    a_website = value['content']
    return a_website


def save_profile_image(username, a_website, directory=""):
    if directory != "":
        save_adress = directory + "/" + username
    else:
        save_adress = username
    f = open(save_adress + '.jpg', 'wb')
    f.write(urllib.request.urlopen(a_website).read())
    f.close()


def show_profile_image(username):
    os.system('feh ' + username + '.jpg')


def show_saved_profile_images(dic):
    count = 1
    for user in dic:
        print('%d.%s' % (count, user))
        count += 1
    number_input = int(input("please enter number of the user that you want to check >  "))
    username = list(dic.keys())[number_input - 1]
    return username


def add_new_user(username, a_website):
    old_dic = pickle_file_load("dic.pickle")
    old_dic[username] = a_website
    pickle_file_dump("dic.pickle", old_dic)
    print("user successfully added!!")


def check_profile_image_change(username, old_url, new_url):
    new_image_name = get_image_adress(new_url)
    old_image_name = get_image_adress(old_url)
    if new_image_name == old_image_name:
        return False
    else:
        return False


def save_profile_url(username, new_url, dic):
    dic[username] = new_url
    pickle_file_dump("dic.pickle", dic)


def delete_a_user():
    old_dic = pickle_file_load("dic.pickle")
    username = show_saved_profile_images(old_dic)
    old_dic.pop(username)
    print(list(old_dic))
    pickle_file_dump("dic.pickle", old_dic)


# should modify and make better
class Archive():
    def __init__(self, username):
        dirname1 = "archive"
        list1 = os.listdir()
        if dirname1 not in list1:
            os.mkdir(dirname1)
        list2 = os.listdir(dirname1)
        self.dirname2 = dirname1 + '/' + username
        if username not in list2:
            os.mkdir(self.dirname2)

    def archive_profile_image(self):
        url = get_url(username)
        user_image_name = get_image_adress(url)
        save_profile_image(user_image_name, url, self.dirname2)


# this function returns profile image name
def get_image_adress(url):

    url_list = url.split('/')[8].split('_')[0:3]
    image_string = ""
    for string in url_list:
        image_string += string
    return image_string


def clear_screen():
    os.system("clear")

# -------------------------------------------------------------------------------------------------
if("dic.pickle" not in os.listdir()):
    dic = {}
    pickle_file_dump("dic.pickle",dic)


fig = Figlet(font='doom')
print(fig.renderText("profile check"))


option = input(
    "If you want to check saved user enter 1\nTo add a new user enter 2\nTo check all users enter 3"
    "\nTo check a delete a user enter 4\nTo archive a profile pic 5\nNow enter your option > ")

if option == "1":
    old_dic = pickle_file_load("dic.pickle")

    username = show_saved_profile_images(old_dic)
    new_dic = {}

    a_website = get_url(username)
    old_url = old_dic[username]
    if check_profile_image_change(username, old_url, a_website):
        print("profile image is changed")
        save_profile_image(username, a_website)
        show_profile_image(username)
        save_profile_url(username, a_website, old_dic)
    else:
        print("profile image is not changed")


elif option == "2":
    new_username = input("enter new username: ")
    a_website = get_url(new_username)
    save_profile_image(new_username, a_website)
    show_profile_image(new_username)
    add_new_user(new_username, a_website)

elif option == "3":
    old_dic = pickle_file_load("dic.pickle")
    for username in old_dic:
        a_website = get_url(username)
        old_url = old_dic[username]
        if check_profile_image_change(username, old_url, a_website):
            print("%s profile is changed!" % username)
            save_profile_image(username, a_website)
            show_profile_image(username)
            save_profile_url(username, a_website, old_dic)

elif option == "4":
    delete_a_user()


elif option == "5":
    old_dic = pickle_file_load("dic.pickle")

    while True:
        clear_screen()
        check_question = input("for archiving all users enter 'a'\nelse\n for archiving single user enter s\n")
        if check_question == "s":
            username = show_saved_profile_images(old_dic)
            archive = Archive(username)
            archive.archive_profile_image()
            break
        elif check_question == "a":
            for username in old_dic:
                archive = Archive(username)
                archive.archive_profile_image()
            break
