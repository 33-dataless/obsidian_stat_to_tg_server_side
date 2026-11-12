from data.models import Payload
from data.event import Event

class Receiver:
    def __init__(self):
        pass

    def process(self, payload: Payload):
        match payload.event:
            case Event.OBSIDIAN:
                self._handle_obsidian(payload.snapshot)

            case Event.GITHUB:
                self._handle_github(payload.snapshot)

            case Event.CHESS:
                self._handle_chess(payload.snapshot)
        
        
    def _handle_obsidian(self, snapshot: dict):
        print("obsidian")
        print(snapshot)

    def _handle_chess(self):
        pass

    def _handle_github(self):
        pass
