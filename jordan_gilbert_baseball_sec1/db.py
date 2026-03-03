import csv
import objects

filename = "players.csv"

def read_lineup():
    lineup = objects.Lineup()
    try:
        with open(filename, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                # row: "Full Name", pos, ab, hits
                if len(row) < 4:
                    continue

                full_name = row[0].strip()
                pos = row[1].strip()
                ab = row[2]
                hits = row[3]

                parts = full_name.split()
                if len(parts) == 0:
                    continue
                first = parts[0]
                last = " ".join(parts[1:])  

                player = objects.Player(first, last, pos, ab, hits)
                lineup.add_player(player)
    except FileNotFoundError:
        lineup = objects.Lineup()
    return lineup

def write_lineup(lineup):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for player in lineup:
            writer.writerow([
                player.full_name,
                player.position,
                player.at_bats,
                player.hits
            ])