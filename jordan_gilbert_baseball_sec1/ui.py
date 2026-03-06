# ui.py
"""
User interface module for the Baseball Team Manager application.

This module handles menu display, user input, lineup display, player
management actions, and game date handling.
"""

import db
from datetime import date, datetime

positions = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")
double_line = "=" * 64
single_line = "-" * 64

# =====================================================
#               Event Handlers
# =====================================================
#1 - Display lineup
def display_lineup(lineup):
    """
    Display the current baseball lineup in a formatted table.

    Args:
        lineup: A collection of player objects to display.
    """
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
    """
    Prompt the user for player information and add a new player to the lineup.

    Validates the player's position, at-bats, and hits before creating and
    adding the player object.

    Args:
        lineup: The lineup object that stores players.
    """
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
    """
    Remove a player from the lineup by lineup number.

    Prompts the user for the player's lineup position, validates the input,
    removes the player, and displays a confirmation message.

    Args:
        lineup: The lineup object that stores players.
    """
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
    """
    Move a player from one lineup position to another.

    Prompts the user for the current player number and the new position,
    validates both inputs, performs the move, and displays a confirmation.

    Args:
        lineup: The lineup object that stores players.
    """
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
    """
    Update the position of a player in the lineup.

    Prompts the user for a lineup number and a new valid position, then
    updates the selected player's position.

    Args:
        lineup: The lineup object that stores players.
    """
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

#6 - Edit player STATS -- Still working on
def edit_player_stats(lineup):
    """
    Update the at-bats and hits for a player in the lineup.

    Prompts the user for a lineup number, at-bats, and hits. Validates the
    entered stats before applying the update.

    Args:
        lineup: The lineup object that stores players.
    """
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

#input for Game date
def get_game_date():
    """
    Prompt the user to enter a game date.

    Accepts a date in YYYY-MM-DD format. Returns None if the user leaves the
    input blank. Re-prompts until a valid date or blank entry is provided.

    Returns:
        A date object representing the game date, or None if no date is entered.
    """
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



# =====================================================
#                    Layout/Menu
# =====================================================
def display_menu(current_date, game_date):
    """
    Display the main program menu along with date information.

    Shows the current date, the scheduled game date if available, the number
    of days until the game, and the list of available menu options and
    positions.

    Args:
        current_date: The current date.
        game_date: The scheduled game date, or None if unknown.
    """
    print(double_line)
    print("                     Baseball Team Manager") #21x space used
    print()
    print(f"CURRENT DATE:                                         {current_date:%Y-%m-%d}") #41x space used
    if game_date is None:
        print("GAME DATE:                                               Unknown")
    else:
        print(f"GAME DATE:                                            {game_date:%Y-%m-%d}") #45x space used

    #Dynamic spcaing for right aligned code
    if game_date is not None:  
        days_until = (game_date - current_date).days
        if days_until > 0:
            label = "DAYS UNTIL GAME:"
            total_width = 64
            value = str(days_until)

            spaces = total_width - len(label) - len(value)
            print(label + " " * spaces + value)

    #Base MEnu 
    print(double_line)
    print("MENU OPTIONS")
    print("1 - Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Update Game Date")
    print("8 - Exit program")
    print()
    print("POSITIONS")
    print(", ".join(positions))
    print(single_line)


# =====================================================
#                  Main operation
# =====================================================
def main():
    """
    Run the main loop of the Baseball Team Manager program.

    Loads the lineup from storage, gets the current and game dates, displays
    the menu, processes user menu selections, and writes changes back to the
    database when needed.
    """
    lineup = db.read_lineup()
    current_date = date.today() 
    game_date = get_game_date()

    while True:
        display_menu(current_date, game_date)
        choice = input("Menu option: ").strip()

        #Case (better/cleaner then if's, simpler to add)
        match choice: 
            case "1":
                display_lineup(lineup)      #Auto Displays
                print()
                print("~ Press Enter key to continue ~")
            case "2":
                add_player(lineup) #button 1-- pop up/title/label/input box
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "3":
                remove_player(lineup) #button 2
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "4":
                move_player(lineup) #button 3
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "5":
                edit_player_position(lineup) #button 4
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "6":
                edit_player_stats(lineup) #button 5
                db.write_lineup(lineup)
                print()
                print("~ Press Enter key to continue ~")
            case "7": #sneaky way, but just re-runs program to re-enter date ////// #button 1
                main()
            case "8":
                print("Program Ended") #button 6
                break
            case _:
                print("Invalid try again.")

        input()

if __name__ == "__main__":
    main()