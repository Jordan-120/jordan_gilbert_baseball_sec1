class Player:
    """
    Represents a baseball player.

    Stores player information including name, field position,
    number of at-bats, and number of hits. Also provides
    calculated properties such as the player's full name
    and batting average.
    """

# =====================================================
#                    ini player
# =====================================================

    def __init__(self, first_name, last_name, position, at_bats=0, hits=0):
        """
        Initialize a Player object.

        Args:
            first_name (str): The player's first name.
            last_name (str): The player's last name.
            position (str): The player's field position.
            at_bats (int): Number of at-bats (default 0).
            hits (int): Number of hits (default 0).
        """
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.at_bats = int(at_bats)
        self.hits = int(hits)

    @property
    def full_name(self):
        """
        Return the player's full name.

        Returns:
            str: The player's first and last name combined.
        """
        return f"{self.first_name} {self.last_name}"

    @property
    def avg(self):
        """
        Calculate the player's batting average.

        Returns:
            float: The batting average (hits / at_bats).
                   Returns 0.0 if at_bats is zero.
        """
        if self.at_bats == 0:
            return 0.0
        return self.hits / self.at_bats

# =====================================================
#                    attributes
# =====================================================
class Lineup:
    """
    Represents a baseball lineup.

    Manages a list of Player objects and provides methods
    to add, remove, move, retrieve, and edit players in the lineup.
    """

    def __init__(self):
        """
        Initialize an empty lineup.
        """
        self._players = []

    def add_player(self, player):
        """
        Add a player to the lineup.

        Args:
            player (Player): The player to add.
        """
        self._players.append(player)

    def remove_player(self, number):
        """
        Remove a player from the lineup by position number.

        Args:
            number (int): The lineup position of the player.

        Returns:
            Player: The removed player object.
        """
        return self._players.pop(number - 1)

    def move_player(self, current, new):
        """
        Move a player from one position to another in the lineup.

        Args:
            current (int): Current lineup position.
            new (int): New lineup position.

        Returns:
            Player: The player that was moved.
        """
        player = self._players.pop(current - 1)
        self._players.insert(new - 1, player)
        return player

    def get_player(self, number):
        """
        Retrieve a player from the lineup by position number.

        Args:
            number (int): The lineup position.

        Returns:
            Player: The requested player object.
        """
        return self._players[number - 1]

    def edit_player_position(self, number, position):
        """
        Update a player's field position.

        Args:
            number (int): The lineup position.
            position (str): The new field position.

        Returns:
            Player: The updated player object.
        """
        player = self.get_player(number)
        player.position = position
        return player

    def edit_player_stats(self, number, at_bats, hits):
        """
        Update a player's statistics.

        Args:
            number (int): The lineup position.
            at_bats (int): Updated at-bats value.
            hits (int): Updated hits value.

        Returns:
            Player: The updated player object.
        """
        player = self.get_player(number)
        player.at_bats = int(at_bats)
        player.hits = int(hits)
        return player

# =====================================================
#               len and iter
# =====================================================

    def __len__(self):
        """
        Return the number of players in the lineup.

        Returns:
            int: The total number of players.
        """
        return len(self._players)

    def __iter__(self):
        """
        Allow iteration through the lineup.

        Yields:
            Player: Each player in the lineup.
        """
        for player in self._players:
            yield player