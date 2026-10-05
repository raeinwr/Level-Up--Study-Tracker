from dataclasses import dataclass, field


@dataclass
class Topic:
    id: int | None
    tracker_id: int
    name: str
    hours: float
    done: int = 0
    studied_seconds: int = 0

    @property
    def planned_seconds(self):
        return int(round(self.hours * 3600))

    @property
    def remaining_seconds(self):
        return max(0, self.planned_seconds - self.studied_seconds)

    @property
    def time_progress(self):
        if self.planned_seconds <= 0:
            return 0.0
        return min(1.0, self.studied_seconds / self.planned_seconds)


@dataclass
class Tracker:
    id: int
    student_id: int
    name: str
    done: int = 0
    topics: list[Topic] = field(default_factory=list)

    @property
    def total(self):
        return len(self.topics)

    @property
    def completed(self):
        return sum(1 for topic in self.topics if topic.done)

    @property
    def complete(self):
        return self.total > 0 and self.completed == self.total

    @property
    def planned_seconds(self):
        return sum(topic.planned_seconds for topic in self.topics)

    @property
    def studied_seconds(self):
        return sum(topic.studied_seconds for topic in self.topics)
