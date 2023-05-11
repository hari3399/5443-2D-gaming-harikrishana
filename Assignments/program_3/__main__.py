import sys

from game import SpaceRocks
from utils import mykwargs

if __name__ == "__main__":
    args, kwargs = mykwargs(sys.argv)
    queue = kwargs.get("queue", None)
    playerId = kwargs.get("player", None)
    creds = {
        "exchange": queue,
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": playerId,
        "password": playerId + "2023!!!!!",
    }

    space_rocks = SpaceRocks(queue,playerId,creds)
    space_rocks.main_loop()
