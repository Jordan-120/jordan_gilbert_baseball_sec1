import csv
filename = "players.csv"

def read_players():
    players = []
    try:
        with open(filename, newline="") as file:
            reader = csv.reader(file)
            for row in reader(file): #forgot :, had error
                row[2] = int(row[2])
                row[3] = int(row[3])
                players.append(row)
    except FileNotFoundError: #had syntax issuies with spaceing
        players = []
    return players 

def write_players(players):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for player in players:
            writer.writerow(player)