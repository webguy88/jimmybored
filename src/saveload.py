import json
import os.path


class GameState:

    def __init__(self):
        pass

    def save(self, player, filename="file.json"):
        state = {}

        state["stamina"] = player.stamina
        state["games"] = player.games

        # Saving
        f = open(filename, "w")
        f.write(json.dumps(state))
        f.close()

    def load(self, player, filename="file.json"):
        # Read
        f = open(filename, "r")
        state = json.load(f)

        player.stamina = state.get("stamina", 5)

        if len(player.games) <= 0:
            player.games = state.get("games", [])

    def state_exists(self, filename="file.json"):
        return os.path.isfile(filename)
