from ..enums.state_enum import State

class ArchiveInfo:
    state = State.NONE
    is_cracked = False
    password = None

    def serialize(self):  
        return {           
            'state': self.state,
            'is_cracked': self.is_cracked,
            'password': self.password
        }