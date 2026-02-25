import db


#Choice #1
def display_lineup(players):

#Choice #2
def add_player(players):

#Choice #3
def remove_player(players):

#Choice #4
def move_player(players):

#Choice #5
def edit_player_position(players):

#Choice #6
def edit_player_stats(players):

#Choice #7
def exit_program(players):


#did best to make the menu look like the pdf example
def display_menu():
    print("Console")
    print("============================================================")
    print("                Baseball Team Manager")
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print("===========================================================")
    print()




#Thought Case would be cleaner then a bunch of if-else statements
def main():
    while True:
        display_menu()
        choice = input("Select what you would like to do (1-7): ")
        #had syntax issuies with print, fixed with seperate line
        match choice:
            case "1":
                display_lineup(players):
                print()
            case "2":
                def add_player(players):
                print()
            case "3":
                def remove_player(players):
                print()
            case "4":
                def move_player(players):
                print()
            case "5":
                def edit_player_position(players):
                print()
            case "6":
                def edit_player_stats(players):
                print()
            case "7":
                def exit_program(players):
                print()
                break
            case _:
                print("Invalid try again.")

        input("enter somthing to return")

if __name__ == "__main__":
    main()