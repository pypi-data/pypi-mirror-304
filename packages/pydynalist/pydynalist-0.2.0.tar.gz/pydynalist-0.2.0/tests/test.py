import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pydynalist import Dynalist


def test():
    dyno = Dynalist(os.environ.get("DYNALIST_TOKEN"))
    print(dyno.docs)


if __name__ == "__main__":
    test()
