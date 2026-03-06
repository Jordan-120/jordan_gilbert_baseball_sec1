import csv
import sqlite3
from contextlib import closing
from pathlib import Path

import objects

"""
Database module for the Baseball Manager application.

This module handles all database-related operations including:
- Establishing and closing database connections
- Creating tables
- Importing player data from CSV files
- Running SELECT, INSERT, UPDATE, and DELETE queries
- Converting database records into Lineup and Player objects
"""

# Only one connection is maintained during program execution
conn = None

DB_FILENAME = "baseball.sqlite"
CSV_FILENAME = "players.csv"


# ==========================================================
#                DB connections
# ==========================================================

def connect():
    """
    Establish a connection to the SQLite database.

    Creates a database connection if one does not already exist.
    The connection is stored in the global `conn` variable and
    configured to return rows as dictionary-like objects.
    """
    global conn

    if not conn:
        db_file = Path(__file__).parent / DB_FILENAME
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row


def close():
    """
    Close the active database connection.

    Safely closes the connection and resets the global connection
    variable so a new connection can be created later if needed.
    """
    global conn

    if conn:
        conn.close()
        conn = None


def init_db():
    """
    Initialize the database schema.

    Creates the Player table if it does not already exist.
    """
    connect()

    sql = """
        CREATE TABLE IF NOT EXISTS Player(
            playerID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            batOrder   INTEGER NOT NULL,
            firstName  TEXT    NOT NULL,
            lastName   TEXT    NOT NULL,
            position   TEXT    NOT NULL,
            atBats     INTEGER NULL,
            hits       INTEGER NULL
        );
    """

    with closing(conn.cursor()) as c:
        c.execute(sql)
        conn.commit()


def _player_count() -> int:
    """
    Return the total number of players currently stored in the database.

    Returns:
        int: Number of records in the Player table.
    """
    connect()

    with closing(conn.cursor()) as c:
        c.execute("SELECT COUNT(*) AS c FROM Player;")
        row = c.fetchone()
        return int(row["c"]) if row else 0


def import_csv_if_empty():
    """
    Import player data from players.csv if the Player table is empty.

    Reads player data from the CSV file and inserts it into the database.
    Each row should contain:
        Full Name, Position, At Bats, Hits
    """
    init_db()

    if _player_count() != 0:
        return

    csv_path = Path(__file__).parent / CSV_FILENAME
    if not csv_path.exists():
        return

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        bat_order = 1

        for row in reader:
            if len(row) < 4:
                continue

            full_name = row[0].strip()
            position = row[1].strip()

            try:
                at_bats = int(row[2])
                hits = int(row[3])
            except ValueError:
                continue

            parts = full_name.split()
            if not parts:
                continue

            first = parts[0]
            last = " ".join(parts[1:]).strip()

            sql = """
                INSERT INTO Player (batOrder, firstName, lastName, position, atBats, hits)
                VALUES (?, ?, ?, ?, ?, ?);
            """

            with closing(conn.cursor()) as c:
                c.execute(sql, (bat_order, first, last, position, at_bats, hits))

            bat_order += 1

    conn.commit()


# ==========================================================
#                      Select Quries
# ==========================================================

def get_players():
    """
    Retrieve all players ordered by batting order.

    Returns:
        list[sqlite3.Row]: Player records ordered by batOrder.
    """
    connect()

    query = """
        SELECT playerID, batOrder, firstName, lastName, position, atBats, hits
        FROM Player
        ORDER BY batOrder;
    """

    with closing(conn.cursor()) as c:
        c.execute(query)
        return c.fetchall()


def get_player(player_id: int):
    """
    Retrieve a single player record by player ID.

    Args:
        player_id (int): The unique database ID for the player.

    Returns:
        sqlite3.Row | None: The player record if found.
    """
    connect()

    query = """
        SELECT playerID, batOrder, firstName, lastName, position, atBats, hits
        FROM Player
        WHERE playerID = ?;
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (player_id,))
        return c.fetchone()


# ==========================================================
#                          CRUD
# ==========================================================

def add_player(first_name, last_name, position, at_bats=0, hits=0):
    """
    Insert a new player into the Player table.

    Automatically assigns the next available bat order.

    Returns:
        int: The database ID of the newly inserted player.
    """
    connect()

    with closing(conn.cursor()) as c:
        c.execute("SELECT COALESCE(MAX(batOrder), 0) AS m FROM Player;")
        row = c.fetchone()
        next_order = int(row["m"]) + 1

    sql = """
        INSERT INTO Player (batOrder, firstName, lastName, position, atBats, hits)
        VALUES (?, ?, ?, ?, ?, ?);
    """

    with closing(conn.cursor()) as c:
        c.execute(sql, (next_order, first_name, last_name, position, int(at_bats), int(hits)))
        conn.commit()
        return c.lastrowid


def delete_player(player_id: int):
    """
    Remove a player from the database.

    Args:
        player_id (int): The ID of the player to delete.
    """
    connect()

    with closing(conn.cursor()) as c:
        c.execute("DELETE FROM Player WHERE playerID = ?", (player_id,))

        c.execute("""
            SELECT playerID
            FROM Player
            ORDER BY batOrder
        """)
        rows = c.fetchall()

        for i, row in enumerate(rows, start=1):
            c.execute(
                "UPDATE Player SET batOrder = ? WHERE playerID = ?",
                (i, row["playerID"])
            )

        conn.commit()


def update_player(player_id: int, position: str, at_bats: int, hits: int):
    """
    Update a player's position and statistics.

    Args:
        player_id (int): ID of the player to update.
        position (str): Updated field position.
        at_bats (int): Updated at-bats value.
        hits (int): Updated hits value.
    """
    connect()

    sql = """
        UPDATE Player
        SET position = ?,
            atBats = ?,
            hits = ?
        WHERE playerID = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(sql, (position, int(at_bats), int(hits), int(player_id)))
        conn.commit()


def set_bat_orders(player_ids_in_order):
    """
    Update batting order values based on a list of player IDs.

    Args:
        player_ids_in_order (list[int]): Player IDs in the desired batting order.
    """
    connect()

    sql = "UPDATE Player SET batOrder = ? WHERE playerID = ?"

    with closing(conn.cursor()) as c:
        for i, pid in enumerate(player_ids_in_order, start=1):
            c.execute(sql, (i, int(pid)))
        conn.commit()


# ==========================================================
#                     Lineup objects
# ==========================================================


def swap_bat_order(from_order, to_order):
    """
    Swap the batting order positions of two players.

    Args:
        from_order (int): The first batting order position.
        to_order (int): The second batting order position.

    Raises:
        ValueError: If either batting order position does not exist.
    """
    connect()

    query = """
        SELECT playerID, batOrder
        FROM Player
        WHERE batOrder IN (?, ?);
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (int(from_order), int(to_order)))
        rows = c.fetchall()

    if len(rows) != 2:
        raise ValueError("Both bat order numbers must exist to swap.")

    id_a = rows[0]["playerID"]
    id_b = rows[1]["playerID"]

    sql = "UPDATE Player SET batOrder = ? WHERE playerID = ?;"

    with closing(conn.cursor()) as c:
        c.execute(sql, (int(to_order), int(id_a)))
        c.execute(sql, (int(from_order), int(id_b)))
        conn.commit()


def read_lineup():
    """
    Build and return a Lineup object using player records from the database.

    Returns:
        Lineup: A Lineup object populated with Player objects from the database.
    """
    import_csv_if_empty()

    lineup = objects.Lineup()
    for row in get_players():
        lineup.add_player(
            objects.Player(
                row["firstName"],
                row["lastName"],
                row["position"],
                row["atBats"] or 0,
                row["hits"] or 0,
            )
        )

    return lineup


def write_lineup(lineup):
    """
    Replace the Player table contents with data from a Lineup object.

    Args:
        lineup (Lineup): The lineup whose players should be written to the database.
    """
    init_db()

    with closing(conn.cursor()) as c:
        c.execute("DELETE FROM Player;")

        sql = """
            INSERT INTO Player (batOrder, firstName, lastName, position, atBats, hits)
            VALUES (?, ?, ?, ?, ?, ?);
        """

        bat_order = 1
        for player in lineup:
            c.execute(
                sql,
                (
                    bat_order,
                    player.first_name,
                    player.last_name,
                    player.position,
                    int(player.at_bats),
                    int(player.hits),
                ),
            )
            bat_order += 1

        conn.commit()