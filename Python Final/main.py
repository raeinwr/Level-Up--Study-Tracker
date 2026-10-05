"""Entry point for Level Up: Study Tracker."""

import sys

from PyQt6.QtWidgets import QApplication

from database.connection import get_connection, init_db
from core.theme import apply_theme
from core.window import MainWindow
from core.service import StudyService

from features.student.repository import Repository as StudentRepository
from features.tracker.repository import Repository as TrackerRepository


def main():
    init_db()

    app = QApplication(sys.argv)

    apply_theme(app)

    connection = get_connection()

    student_repo = StudentRepository(connection)
    tracker_repo = TrackerRepository(connection)

    service = StudyService(
        student_repo,
        tracker_repo
    )

    window = MainWindow(service)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()