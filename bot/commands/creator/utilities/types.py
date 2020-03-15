from enum import Enum


class Option(Enum):
    TO_SUBOPTION: str = ""
    
    # /data
    IDS: str = "ids"
    USERNAME: str = "username"
    FIRSTNAME: str = "firstname"
    NUMBER: str = "number"
    INDEX: str = "index"
    NAME: str = "name"
    GROUP: str = "group"
    YEAR: str = "year"
    
    # /broadcast
    MESSAGE: str = "message"
    SIGNED: str = "signed"
    
    # /dayoff
    ADD: str = "add"
    DROP: str = "drop"

class Suboption(Enum):
    ALL: str = "all"
    UNLOGIN: str = "unlogin"
    ME: str = "me"
    
    LIST: str = "list"
    
    WEEK: str = "week"
