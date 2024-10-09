from enum import StrEnum


class WorkoutStatus(StrEnum):
    COMPLETED = "completed"
    TO_BE_STARTED = "to_be_started"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"
