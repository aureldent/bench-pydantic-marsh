
import json
from uuid import UUID, uuid4

from enum import Enum

from pydantic import BaseModel, Field

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
    # Pydantic
    ##########

    class Info(BaseModel):
        tag: str

    class OrgPydantic(BaseModel):
        id: str
        status: Status
        info: Info
        super_id: UUID

    class BasicUserPydantic(BaseModel):
        email: str
        id: int
        is_admin: bool = Field(serialization_alias="isAdmin", alias="isAdmin")
        orgs: list[OrgPydantic]
        ids: list[int]
        names: set[str]

    PYDANTIC_ORG = OrgPydantic(
        id="2002",
        status=Status.LIVE,
        info=Info(
            tag= "tag"
        ),
        super_id=uuid4()
    )
        
    PYDANTIC_USER = BasicUserPydantic(
        email = "test@test.com",
        id = 100,
        isAdmin = True,
        orgs=[PYDANTIC_ORG] * N_ELEM_ARRAY,
        ids=[i for i in range(N_ELEM_ARRAY)],
        names=[f"n_{i}" for i in range(N_ELEM_ARRAY)]
    )
    snapshot = tracemalloc.take_snapshot()
    total_bytes = sum(stat.size for stat in snapshot.statistics('lineno'))
    # convert to kb
    total_kb = total_bytes / 1024.0
    print(f"Pydantic cosumes {total_kb} kb")



if __name__ == "__main__":
    main()
