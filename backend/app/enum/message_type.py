from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    PET_CARD = "pet_card"