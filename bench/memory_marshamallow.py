import json, sys
from uuid import UUID, uuid4

from dataclasses import dataclass, field
from enum import Enum

import tracemalloc


def main():
    tracemalloc.start()
    class Status(Enum):
        LIVE = "live"

    BASIC_ORG = {
        "id": "001",
        "status": "live",
        "info": {
            "tag": "true"
        },
        "super_id": "6122888b-3e2b-42af-88a0-0bc365ac4adb"
    }

    BASIC_USER = {
        "email": "test@test.com",
        "id": 100,
        "isAdmin": True,
        "orgs": [BASIC_ORG] * 10
    }

    BASIC_USER_STRING = json.dumps(BASIC_USER)

    ##############
    # Marshmallow
    ##############

    @dataclass
    class Info:
        tag: str

    @dataclass
    class OrgMarsh:
        id: str
        status: Status =  field(
            metadata={"by_value": True}
        )
        info: Info
        super_id: UUID

    @dataclass
    class BasicUserMarsh:
        email: str
        id: int
        is_admin: bool = field(metadata={"data_key": "isAdmin"})
        orgs: list[OrgMarsh]
        ids: list[int]
        names: list[str]

    MARSH_ORG = OrgMarsh(
        id="2002",
        status=Status.LIVE,
        info=Info(tag="tag"),
        super_id=uuid4()
    )
        
    MARSHMALLOW_USER = BasicUserMarsh(
        email = "test@test.com",
        id = 100,
        is_admin = True,
        orgs=[MARSH_ORG] * 50,
        ids=[i for i in range(50)],
        names=[f"n_{i}" for i in range(30)]
    )

    snapshot = tracemalloc.take_snapshot()
    total_bytes = sum(stat.size for stat in snapshot.statistics('lineno'))
    # convert to kb
    total_kb = total_bytes / 1024.0
    print(f"Marhsh cosumes {total_kb} kb")


if __name__ == "__main__":
    main()
