import asyncio
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))
from src.pydynalist import Dynalist


def test_sync():
    dyno = Dynalist(os.environ.get("DYNALIST_TOKEN"))
    print(dyno.get_doc_id("Untitled"))


async def test_async():
    dyno = Dynalist(os.environ.get("DYNALIST_TOKEN"))
    print(await dyno.get_doc_id("Untitled"))


if __name__ == "__main__":
    # test_sync()
    asyncio.run(test_async())
