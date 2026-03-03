# ui.py
import db
from datetime import date, datetime

positions = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
double_line = "=" * 64
single_line = "-" * 64

#1 - Display lineup
def display_lineup(lineup):
    print("   {:<35}{:<8}{:>7}{:>6}{:>8}".format("Player", "POS", "AB", "H", "AVG"))
    print(single_line)

    number = 1
    for player in lineup:
        print("{:<2} {:<35}{:<8}{:>7}{:>6}{:>8.3f}".format(
            number, player.full_name, player.position, player.at_bats, player.hits, player.avg
        ))
        number += 1

#2 - Display Lineup
def add_player(lineup):
    first = input("First name: ")
    last = input("Last name: ")
    position = input("Position: ")

    while position not in positions:
        print("please try again")
        position = input("Position: ")

    try:
        at_bats = int(input("At bats: "))
        hits = int(input("Hits: "))
        if at_bats < 0 or hits < 0 or hits > at_bats:
            print("please try again")
            return
    except ValueError:
        print("please try again")
        return

    import objects
    player = objects.Player(first, last, position, at_bats, hits)
    lineup.add_player(player)
    print(f"{player.full_name} was added.")

#3 - Remove PLayer
def remove_player(lineup):
    try:
        number = int(input("number: "))
        if number < 1 or number > len(lineup):
            print("please try again")
            return
    except ValueError:
        print("invaild int")
        return

    player = lineup.remove_player(number)
    print(f"{player.full_name} deleted")

#4 - Move Player -- Still working on
def move_player(lineup):
    try:
        current = int(input("# of the Player to move: "))
        if current < 1 or current > len(lineup):
            print("please try again")
            return
    except ValueError:
        print("invaild int")
        return

    try:
        new = int(input("# to move to: "))
        if new < 1 or new > len(lineup) + 1:
            print("please try again")
            return
    except ValueError:
        print("invaild int")
        return

    player = lineup.move_player(current, new)
    print(f"{player.full_name} at postion #{current} moved to postion #{new}")

#5 - Edit player -- Still working on
def edit_player_position(lineup):
    try:
        number = int(input("Postion number: "))
        if number < 1 or number > len(lineup):
            print("invaild")
            return
    except ValueError:
        print("invaild int")
        return

    player = lineup.get_player(number)
    print(f"Player: {player.full_name}, Postion: {player.position}")

    position = input("New postion: ")
    while position not in positions:
        print("invaild, try again")
        position = input("New postion: ")

    lineup.edit_player_position(number, position)
    print(f"{player.full_name} updated")

#5 - Edit player STATS -- Still working on
def edit_player_stats(lineup):
    try:
        number = int(input("Postion number: "))
        if number < 1 or number > len(lineup):
            print("invaild")
            return
    except ValueError:
        print("invaild int")
        return

    player = lineup.get_player(number)

    try:
        at_bats = int(input("At bats: "))
        hits = int(input("hits: "))
        if at_bats < 0 or hits < 0 or hits > at_bats:
            print("invaid input")
            return
    except ValueError:
        print("invalid int")
        return

    lineup.edit_player_stats(number, at_bats, hits)
    print(f"{player.full_name} updated")

# want to allow as option 8 to call again
def get_game_date():
    game_date_str = input("GAME DATE: ").strip()
    if game_date_str == "":
        return None

    while True:
        try:
            return datetime.strptime(game_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format EX: YYYY-MM-DD.")
            game_date_str = input("GAME DATE:").strip()
            if game_date_str == "":
                return None

# Displays of UI
def display_menu(current_date, game_date):
    print(double_line)
    print("                     Baseball Team Manager") #6 tabss used
    print()
    print(f"CURRENT DATE:                                         {current_date:%Y-%m-%d}") #finding best format
    if game_date is None:
        print("GAME DATE:                                               Unknown")
    else:
        print(f"GAME DATE:                                            {game_date:%Y-%m-%d}")

    if game_date is not None:  #finding best format
        days_until = (game_date - current_date).days
        if days_until > 0  < 10:
            print(f"DAYS UNTIL GAME:                                               {days_until}")
        elif days_until >= 10:
            print(f"DAYS UNTIL GAME:                                              {days_until}")
        elif days_until >= 100:
            print(f"DAYS UNTIL GAME:                                             {days_until}")

    #Base MEnu
    print(double_line)
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print()
    print("POSITIONS")
    print(", ".join(positions))
    print(single_line)

def main():
    lineup = db.read_lineup()
    current_date = date.today() #Dates, still be adjusted
    game_date = get_game_date()

    while True:
        display_menu(current_date, game_date)
        choice = input("Menu option: ").strip()

        match choice: #LOVE CASE, Always use when I can
            case "1":
                display_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "2":
                add_player(lineup)
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "3":
                remove_player(lineup)
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "4":
                move_player(lineup)
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "5":
                edit_player_position(lineup)
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "6":
                edit_player_stats(lineup)
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "7":
                print("Program Ended")
                break
            case _:
                print("Invalid try again.")

        input()

if __name__ == "__main__":
    main()