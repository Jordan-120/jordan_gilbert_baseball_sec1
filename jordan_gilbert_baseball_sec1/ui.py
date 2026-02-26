import db
import objects

#have put in until object import fix
positions = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")

#Choice #1
def display_lineup(players):
    print("{:<5}{:<15}{:<6}{:<8}{:<8}{:<6}".format("#","player","POS","AB","H","AVG"))
    print("-" * 50)

    number = 1
    for player in players:
        name = player[0]
        pos = player[1]
        at_bats = int(player[2])
        hits = int(player[3])

        try:
            avg = round(hits / at_bats, 3)
        except ZeroDivisionError:
            avg = 0.0

            print("{:<5}{:<15}{:<6}{:<8}{:<8}{:<6}".format("#","player","POS","AB","H","AVG"))
            number += 1

#Choice #2
def add_player(players):
    name = input("Name:")
    position = input("Postions:")

    while position not in positions: #Learned I have to capitalize
        print("please try again")
        position = input("postion")

    try:
        at_bats = int(input("At bats:"))
        hits = int(input("Hits:"))
        if at_bats <0 or hits <0 or hits > at_bats:
            print("please try again")
            return
    except ValueError:
        print("please try again")
        return
    
    players.append([name, position, at_bats, hits])
    print(f"{name} added")


#Choice #3
def remove_player(players):
    try:
        number = int(input("number:"))
        if number < 1 or number > len(players):
            print("please try again")
            return
    except ValueError:
        print("invaild int")
        return
    
    player = players.pop(number - 1) #found pop best method
    print(f"{player[0]} deleted")

#Choice #4
def move_player(players):
    try:
        current = int(input("current lineup:"))
        if current <1 or current > len(players):
            print("please try again")
            return
    except ValueError:
        print("invaild int")
        return
    player = players.pop(current-1)

    try:
        new = int(input("NEw lineup:"))
        if new <1 or new > len(players) +1:
            print("please try again")
            player.insert(current - 1, player)
            return
    except ValueError:
        print("invaild int")
        players.insert(current = 1, player)
        return
    players.insert(new - 1, player)
    print(f"{player[0]} moved")

#Choice #5
def edit_player_position(players):
    try:
        number = int(input("Lineup number:"))
        if number <1 or number >len(players):
            print("invaild")
            return
    except ValueError:
        print("invaild int")
        return
    player = player[number -1]
    print(f"player:{player[0]} at PSO:{player[1]}")
    position = input("New postion")
    while position not in positions:
        print("invaild, try again")
        position = input("new postion")

    player[1] = position
    print(f"{player[0]} updated")


#Choice #6
def edit_player_stats(players):
    try: 
        number = int(input("Lineup number:"))
        if number <1 or number > len(players):
            print("invaild")
            return
    except ValueError:
        print("invaild int")
        return
    player = players[number -1]
    try: 
        at_bats = int(input("At bats:"))
        hits = int(input("hits:"))

        if at_bats <0 or hits <0 or hits > at_bats:
            print("invaid input")
            return
    except ValueError:
        print("invalid int")
        return
    player[2] = at_bats
    player[3] = hits
    print(f"{player[0]} updated")


#Choice #7
def exit_program(players):
    print("Exiting Program....")


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
    players = db.read_players()
    while True:
        display_menu()
        choice = input("Select what you would like to do (1-7): ")
        #had syntax issuies with print, fixed with seperate line
        match choice:
            case "1":
                display_lineup(players)
            case "2":
                add_player(players)
                db.write_players(players)
            case "3":
                remove_player(players)
                db.write_players(players)
            case "4":
                move_player(players)
                db.write_players(players)
            case "5":
                edit_player_position(players)
                db.write_players(players)
            case "6":
                edit_player_stats(players)
                db.write_players(players)
            case "7":
                exit_program(players)
                print("Program End")
                break
            case _:
                print("Invalid try again.")

        input("enter somthing to return")

if __name__ == "__main__":
    main()

'''
Use this for documentation
'''