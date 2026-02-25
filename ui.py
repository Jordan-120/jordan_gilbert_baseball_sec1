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
                print("Display lineup selected")
            case "2":
                print("Add player selected")
            case "3":
                print("Remove player selected")
            case "4":
                print("Move player selected")
            case "5":
                print("Edit player position selected")
            case "6":
                print("Edit player stats selected")
            case "7":
                print("Exiting program...")
                break
            case _:
                print("Invalid option. Please try again.")

        input("enter somthing to return")

if __name__ == "__main__":
    main()