from ..enums.state_enum import State
import queue

class Archive:
    state = State.NONE
    is_cracked = False
    password = None
    processing_queue = queue.SimpleQueue()

    def __init__(self, state=State.NONE, is_cracked=False, password=None):
        self.state = state
        self.is_cracked = is_cracked
        self.password = password

    def append_processing(self, processing):
        self.processing_queue.put(processing)

    def start_processing(self):
        if not self.processing_queue.empty():
            self.state = State.PROCESSING
            processing = self.processing_queue.get()
            processing()
            self.state = State.PROCESSED
            self.start_processing()

    def serialize(self):  
        return {           
            'state': self.state,
            'is_cracked': self.is_cracked,
            'password': self.password
        }