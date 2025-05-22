import enum

class ObjectivePriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class ObjectiveStatus(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    at_risk = "at_risk"
    on_hold = "on_hold"
    delayed = "delayed"
    completed = "completed"
    cancelled = "cancelled"
