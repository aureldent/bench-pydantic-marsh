import json
from uuid import UUID, uuid4

from enum import Enum

import tracemalloc

N_ELEM_ARRAY = 50

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
        "orgs": [BASIC_ORG] * N_ELEM_ARRAY,
        "ids": [i for i in range(N_ELEM_ARRAY)],
        "names": [f"n_{i}" for i in range(N_ELEM_ARRAY)]
    }

    BASIC_USER_STRING = json.dumps(BASIC_USER)

    ##########
    # msgspec
    ##########
    import msgspec

    class InfoMsgspec(msgspec.Struct):
        tag: str

    class OrgMsgspec(msgspec.Struct):
        id: str
        status: Status
        info: InfoMsgspec
        super_id: UUID

    class BasicUserMqgspec(msgspec.Struct):
        email: str
        id: int
        is_admin: bool = msgspec.field(name="isAdmin")
        orgs: list[OrgMsgspec]
        ids: list[int]
        names: list[str]


    MSGSPEC_ORG = OrgMsgspec(
        id="2002",
        status=Status.LIVE,
        info=InfoMsgspec(
            tag= "tag"
        ),
        super_id=uuid4()
    )
        
    MSGSPEC_USER = BasicUserMqgspec(
        email = "test@test.com",
        id = 100,
        is_admin = True,
        orgs=[MSGSPEC_ORG] * N_ELEM_ARRAY,
        ids=[i for i in range(N_ELEM_ARRAY)],
        names=[f"n_{i}" for i in range(N_ELEM_ARRAY)]
    )

    snapshot = tracemalloc.take_snapshot()
    total_bytes = sum(stat.size for stat in snapshot.statistics('lineno'))
    # convert to kb
    total_kb = total_bytes / 1024.0
    print(f"Msgspec cosumes {total_kb} kb")

if __name__ == "__main__":
    main()
