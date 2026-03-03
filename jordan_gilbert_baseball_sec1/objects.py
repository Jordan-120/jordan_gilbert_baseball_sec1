class Player:
    def __init__(self, first_name, last_name, position, at_bats=0, hits=0):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.at_bats = int(at_bats)
        self.hits = int(hits)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avg(self):
        if self.at_bats == 0:
            return 0.0
        return self.hits / self.at_bats


class Lineup:
    def __init__(self):
        self._players = []

    def add_player(self, player):
        self._players.append(player)

    def remove_player(self, number):
        return self._players.pop(number - 1)

    def move_player(self, current, new):
        player = self._players.pop(current - 1)
        self._players.insert(new - 1, player)
        return player

    def get_player(self, number):
        return self._players[number - 1]

    def edit_player_position(self, number, position):
        player = self.get_player(number)
        player.position = position
        return player

    def edit_player_stats(self, number, at_bats, hits):
        player = self.get_player(number)
        player.at_bats = int(at_bats)
        player.hits = int(hits)
        return player

    def __len__(self):
        return len(self._players)

    def __iter__(self):
        for player in self._players:
            yield player