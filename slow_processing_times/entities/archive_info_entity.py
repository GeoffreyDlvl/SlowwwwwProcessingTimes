from ..enums.state_enum import State

class ArchiveInfo:
    state = State.NONE
    is_cracked = False
    password = ""

    def __init__(self, state=State.NONE, is_cracked=False, password=""):
        self.state = state
        self.is_cracked = is_cracked
        self.password = password

    def serialize(self):  
        return {           
            'state': self.state,
            'is_cracked': self.is_cracked,
            'password': self.password
        }