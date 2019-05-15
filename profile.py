import os
import pickle
import urllib.request
from lxml import html
from bs4 import BeautifulSoup
import webbrowser
from pyfiglet import Figlet
import re
import json
import requests
import sys
import shutil


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
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    scripts = soup.find_all('script', type="text/javascript",
                            text=re.compile('window._sharedData'))
    stringified_json = scripts[0].get_text().replace(
        'window._sharedData = ', '')[:-1]

    dic_file = (json.loads(stringified_json)['entry_data']['ProfilePage'][0])

    a_website = (dic_file["graphql"]["user"]["profile_pic_url_hd"])
    return a_website


def save_profile_image(username, a_website, directory=""):
    if directory != "":
        save_adress = directory + "/" + username
    else:
        save_adress = username
    f = open(save_adress + '.jpg', 'wb')
    f.write(urllib.request.urlopen(a_website).read())
    f.close()


def show_saved_profile_images(dic):
    count = 1
    for user in dic:
        print('%d.%s' % (count, user))
        count += 1
    number_input = int(
        input("please enter number of the user that you want to check >  "))
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
        return True


def save_profile_url(username, new_url, dic):
    dic[username] = new_url
    pickle_file_dump("dic.pickle", dic)


def delete_a_user():
    old_dic = pickle_file_load("dic.pickle")
    username = show_saved_profile_images(old_dic)

    while True:
        option = input(
            "Do you want to delete user images from archive too?? (Y/N) > ")
        if option == "Y" or option == "y":
            shutil.rmtree("archive/" + username)
            break
        elif option == "N" or option == "n":
            break
        else:
            pass

    old_dic.pop(username)
    pickle_file_dump("dic.pickle", old_dic)


class Archive():
    def __init__(self, username):
        self.username = username
        dirname1 = "archive"
        list1 = os.listdir()
        if dirname1 not in list1:
            os.mkdir(dirname1)
        list2 = os.listdir(dirname1)
        self.dirname2 = dirname1 + '/' + username
        if username not in list2:
            os.mkdir(self.dirname2)

    def archive_profile_image(self):
        url = get_url(self.username)
        user_image_name = get_image_adress(url)
        save_profile_image(user_image_name, url, self.dirname2)
        os.system("feh archive/" + self.username +
                  "/" + user_image_name + ".jpg")


def get_image_adress(url):

    url_list = url.split('/')[8].split('_')[0:3]
    image_string = ""
    for string in url_list:
        image_string += string
    return image_string


def clear_screen():
    os.system("clear")

#--------------------------------------------------------------------------------------------------------------


def option_one():
    old_dic = pickle_file_load("dic.pickle")

    username = show_saved_profile_images(old_dic)
    new_dic = {}

    a_website = get_url(username)
    old_url = old_dic[username]
    if check_profile_image_change(username, old_url, a_website):
        print("profile image is changed")
        save_profile_url(username, a_website, old_dic)
        archive = Archive(username)
        archive.archive_profile_image()

    else:
        print("profile image is not changed")
        input("Press any key! ")


def option_two():
    new_username = input("enter new username: ")
    a_website = get_url(new_username)
    archive = Archive(new_username)
    archive.archive_profile_image()
    add_new_user(new_username, a_website)


def option_three():
    old_dic = pickle_file_load("dic.pickle")
    for username in old_dic:
        try:
            print(username)
            a_website = get_url(username)
            old_url = old_dic[username]
            result = check_profile_image_change(username, old_url, a_website)
            if check_profile_image_change(username, old_url, a_website):
                print("%s profile is changed!" % username)
                save_profile_url(username, a_website, old_dic)
                archive = Archive(username)
                archive.archive_profile_image()
        except:
            print("%s username has changed" % username)
            pass


def option_four():
    delete_a_user()

def option_five():
    dic = pickle_file_load("dic.pickle")
    username = show_saved_profile_images(dic)

    os.system("feh -F archive/" + username)

def exit():
    sys.exit()

#--------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
