import os
import pickle
import urllib.request
from lxml import html
import webbrowser
from pyfiglet import Figlet
import re
import json
import requests
import sys
import shutil
import datetime

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
    url = "https://www.instagram.com/" + username + '/?__a=1'
    try:
        r = requests.get(url)
    except:
        print("\ncheck your internet connection please\n")
        return

    requesContent = r.json()
    userInformation = requesContent["graphql"]["user"]
    isPrivateStatus = userInformation["is_private"]
    hdProfilePicUrl = userInformation["profile_pic_url_hd"]
    bioText = userInformation["biography"]
    externalSiteLink = userInformation["external_url"]

    if externalSiteLink:
        bioText = bioText + "\n\n" + externalSiteLink

    checkPrivateOrPublicStatus(username,isPrivateStatus)

    return hdProfilePicUrl,bioText

#this function checks whether the privacy status of a user is changed or not
def checkPrivateOrPublicStatus(username,new_status):
    dic = pickle_file_load("dic3.pickle")
    keys = list(dic.keys())
    if username not in keys:
        dic[username] = new_status
        pickle_file_dump("dic3.pickle",dic)
        print("privacy status added for %s "%username)
        return

    old_status = dic[username]

    if old_status!=new_status:
        dic[username] = new_status
        if new_status:
            message = "public"
        else:
            message = "privae"
        pickle_file_dump("dic3.pickle",dic)        

        warningMessage = "\n"+"*"*5+"---- important ----"+"*"*5+"\n"
        mainMessage = "this user is no longer %s---> %s"%(message,username) 
        print(warningMessage + mainMessage +warningMessage)                

    
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

def deleteFromBioDic(username):
    dic = pickle_file_load("dic2.pickle")
    del dic[username]
    pickle_file_dump("dic2.pickle",dic)


def delete_a_user():
    old_dic = pickle_file_load("dic.pickle")
    username = show_saved_profile_images(old_dic)

    while True:
        option = input(
            "Do you want to delete user images and bio from archive too?? (Y/N) > ")
        if option == "Y" or option == "y":
            shutil.rmtree("archive/" + username)
            deleteFromBioDic(username)
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
        url = get_url(self.username)[0]
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

def bioGetFunction(userName,newBioText):
    dic2 = pickle_file_load("dic2.pickle")
    savedUsers = dic2.keys()
    if userName not in savedUsers:
        dic2[userName] = newBioText
        print("Bio--> " + newBioText)
        saveBioInFolder(userName,dic2)
    else:
        oldBioText = dic2[userName]
        if oldBioText != newBioText:
            print(userName+" has changed Bio")
            print("this is new Bio --->  ",newBioText)
            dic2[userName] = newBioText
            saveBioInFolder(userName,dic2)
    pickle_file_dump("dic2.pickle",dic2)

#saves new bio in related folder for a user
def saveBioInFolder(user,dic2):
    directory = "archive/" + user + '/'
    name = user + "bio.txt"
    date = str(datetime.datetime.now().date())
    if name not in os.listdir(directory):
        with open(directory+name,"w") as file:
            file.write(date)
            file.write("\n\n")
            file.write(dic2[user])
    else:
        with open(directory+name,"a") as file:
            file.write("*"*100)
            file.write("\n" + date + "\n")
            file.write("\n"+dic2[user])

def continueQuestionFunction(question):
    while True:
        answer = input("Do you want to continue %s (Y/N)"%question)
        answer = answer.lower()
        if answer == "y":
            return 1
        elif answer == "n":
            return 0
        else:
            print("Not valid input")
#--------------------------------------------------------------------------------------------------------------


def option_one():
    old_dic = pickle_file_load("dic.pickle")

    username = show_saved_profile_images(old_dic)
    new_dic = {}

    (a_website,newBioText) = get_url(username)
    bioGetFunction(username,newBioText)
    old_url = old_dic[username]
    try:
        if check_profile_image_change(username, old_url, a_website):
            print("profile image is changed")
            save_profile_url(username, a_website, old_dic)
            archive = Archive(username)
            archive.archive_profile_image()
        else:
            print("profile image is not changed")
            input("Press any key! ")
    except IndexError:
        print("%s doesn\'t have profile pic "%username)
    else:
        print("%s has probably changed username"%username)

def option_two():
    new_username = input("enter new username: ")

    (a_website,newBioText) = get_url(new_username)

    archive = Archive(new_username)
    archive.archive_profile_image()
    add_new_user(new_username, a_website)
    bioGetFunction(new_username,newBioText)

def option_three():
    old_dic = pickle_file_load("dic.pickle")
    for username in old_dic:
        try:
            (a_website,newBioText) = get_url(username)

            old_url = old_dic[username]
            result = check_profile_image_change(username, old_url, a_website)
            if check_profile_image_change(username, old_url, a_website):
                print("%s profile is changed!" % username)
                save_profile_url(username, a_website, old_dic)
                archive = Archive(username)
                archive.archive_profile_image()
            bioGetFunction(username,newBioText)
        except IndexError:
            print("%s doesn't have profile pic"%username)
        except:
            print("%s username has probably changed"%username)
        


def option_four():
    delete_a_user()

def option_five():
    dic = pickle_file_load("dic.pickle")
    username = show_saved_profile_images(dic)

    os.system("feh -F archive/" + username)

def option_six():
    dic2 = pickle_file_load("dic2.pickle")
    with open("bios.txt","w") as file:
        for key in dic2:
            file.write("\n"+"**********" + key + "************"+"\n")
            file.write(dic2[key])
    os.system("gedit bios.txt")

def option_seven():
    dic = pickle_file_load("dic.pickle")

    while True:
        username = show_saved_profile_images(dic)

        directory = "archive/"+username+'/'+username+"bio.txt"
        command = "gedit " + directory
        os.system(command)

        ans = continueQuestionFunction("seeing bio of a user?")
        if not ans:
            break




def exit():
    sys.exit()

#--------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    pass
