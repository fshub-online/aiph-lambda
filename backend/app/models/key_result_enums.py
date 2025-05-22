import enum

class KeyResultStatus(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    at_risk = "at_risk"
    on_hold = "on_hold"
    delayed = "delayed"
    completed = "completed"
    cancelled = "cancelled"
    current = "current"
    planned = "planned"
    past = "past"

class KeyResultPriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class KeyResultComplexity(enum.Enum):
    trivial = "trivial"
    easy = "easy"
    moderate = "moderate"
    hard = "hard"
    extreme = "extreme"

