from profile import *

menuItems = [
    {'Check one particular saved user' : option_one},
    {'Add a new user' : option_two},
    {'Check all users': option_three},
    {'Delete a User': option_four},
    {'See a user\'s profile pic': option_five},
    {'Exit' : exit}
] 

def main():
    if("dic.pickle" not in os.listdir()):
        dic = {}
        pickle_file_dump("dic.pickle",dic)

    
    clear_screen()
    fig = Figlet(font='doom')
    print(fig.renderText("profile check"))

    for item in menuItems:
        print("[" + str(menuItems.index(item)) + "]" + list(item.keys())[0])
    choice = int(input(">>"))
    list(menuItems[choice].values())[0]()




main()