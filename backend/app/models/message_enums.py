import enum
import logging

logger = logging.getLogger(__name__)


class MessagePriority(enum.Enum):
    Top = "Success"
    High = "Warning"
    Medium = "Info"
    Low = "Error"
