import enum

class MessagePriority(enum.Enum):
    Top = "Success"
    High = "Warning"
    Medium = "Info"
    Low = "Error"
