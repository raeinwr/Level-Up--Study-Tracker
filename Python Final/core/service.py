from features.student.service import StudentService
from features.tracker.service import TrackerService


class StudyService:

    def __init__(
        self,
        student_repo,
        tracker_repo
    ):

        self.student = StudentService(
            student_repo
        )

        self.tracker = TrackerService(
            tracker_repo
        )