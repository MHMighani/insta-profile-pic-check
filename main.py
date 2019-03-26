from profile import *

menuItems = [
    {'Check one particular saved user' : option_one},
    {'Add a new user' : option_two},
    {'Check all users': option_three},
    {'Delete a User': option_four},
    {'Archive profile pictures' : option_five},
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
    try:
        if int(choice) < 0: 
            raise ValueError
        list(menuItems[choice].values())[0]()
    except(ValueError,IndexError):
        pass


main()