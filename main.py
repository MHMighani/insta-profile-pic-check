from profile import *
import sys
import os

#This is for argument passing for fast checking all pages
#I used this option for fast page checking in my startup
numberOfArguments = len(sys.argv)
if numberOfArguments == 2:
    choice = sys.argv[1]
    if str(choice)=="fast":
        option_three()
        input("Press any key")
menuItems = [
    {'Check one particular saved user' : option_one},
    {'Add a new user' : option_two},
    {'Check all users': option_three},
    {'Delete a User': option_four},
    {'See a user\'s profile pic': option_five},
    {'To see all bio\'s': option_six},
    {'To see bio of a user ':option_seven},
    {'Exit' : exit}
]

def main():
    if "dic.pickle" not in os.listdir():
        dic = {}
        pickle_file_dump("dic.pickle",dic)
    if "dic2.pickle" not in os.listdir():
        dic2 = {}
        pickle_file_dump("dic2.pickle",dic2)

    clear_screen()
    fig = Figlet(font='doom')
    print(fig.renderText("profile check"))

    for item in menuItems:
        print("[" + str(menuItems.index(item)) + "]" + list(item.keys())[0])
    choice = int(input(">>"))
    list(menuItems[choice].values())[0]()




main()
