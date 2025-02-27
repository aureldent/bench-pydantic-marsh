import json
from uuid import UUID, uuid4
import orjson

from dataclasses import dataclass, field
from enum import Enum

from marshmallow_dataclass import class_schema
from pydantic import BaseModel, Field

NB_ORGS = 100
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
    "orgs": [BASIC_ORG] * NB_ORGS
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
    orgs=[MARSH_ORG] * NB_ORGS
)

def deserialize_with_marshmallow():
    return class_schema(BasicUserMarsh)().load(BASIC_USER)

def serialize_with_marshmallow():
    return class_schema(BasicUserMarsh)().dump(MARSHMALLOW_USER)

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
    orgs=[PYDANTIC_ORG] * NB_ORGS
)

def deserialize_with_pyandtic_standard():
    return BasicUserPydantic.model_validate(BASIC_USER)

def serialize_with_pyandtic_standard():
    return PYDANTIC_USER.model_dump_json()

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
    id = 1000,
    is_admin = True,
    orgs=[MSGSPEC_ORG] * NB_ORGS
)

def deserialize_with_msg_spec():
    return msgspec.json.decode(BASIC_USER_STRING, type=BasicUserMqgspec)

def serialize_with_msg_spec():
    return msgspec.json.encode(MSGSPEC_USER)

###
# json
##
def load_json_standard():
    return json.loads(BASIC_USER_STRING)

def load_json_orjson():
    return orjson.loads(BASIC_USER_STRING)

def dump_json_standard():
    return json.dumps(BASIC_USER)

def dump_json_orjson():
    return orjson.dumps(BASIC_USER)

__benchmarks__ = [
    (deserialize_with_marshmallow, deserialize_with_pyandtic_standard, "pydantic instead of marshmallow: deserialize"),
    (serialize_with_marshmallow, serialize_with_pyandtic_standard, "pydantic instead of marshmallow: serialize"),
    (deserialize_with_pyandtic_standard, deserialize_with_msg_spec, "msgspec instead of pydantic: deserialize"),
    (serialize_with_pyandtic_standard, serialize_with_msg_spec, "msgspec instead of pydantic: serialize"),
    (deserialize_with_marshmallow, deserialize_with_msg_spec, "msgspec instead of marshmallow: deserialize"),
    (serialize_with_marshmallow, serialize_with_msg_spec, "msgspec instead of marshmallow: serialize"),
]
