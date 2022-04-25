import pymongo
from beanie import Document, Link, Indexed

from .permission_schema import Permission

class Group(Document):
    code_name: str = Indexed(str, index_type=pymongo.ASCENDING, unique=True)
    name: str
    description: str | None
    permissions: list[Link[Permission]]
    
    class Collection:
        name = "groups"