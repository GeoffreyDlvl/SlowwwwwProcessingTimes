from enum import Enum

class State(str, Enum):
    NONE       = 'None'
    UPLOADING  = 'Uploading'
    UPLOADED   = 'Uploaded'
    CRACKING   = 'Cracking'
    CRACKED    = 'Cracked'
    PROCESSING = 'Processing'
    PROCESSED  = 'Processed'
