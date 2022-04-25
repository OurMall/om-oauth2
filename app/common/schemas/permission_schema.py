import pymongo
from beanie import Document, Indexed

class Permission(Document):
    code_name: str = Indexed(str, index_type=pymongo.ASCENDING, unique=True)
    name: str
    description: str | None
    
    class Collection:
        name = "permissions"