from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QStackedWidget
)

from features.start.view import (
    StartPage,
    NamePage,
    AvatarPage
)

from features.student.view import (
    TrackerListPage
)

from features.tracker.view import (
    EditorPage,
    MainPage,
    CongratsPage
)


class MainWindow(QMainWindow):

    def __init__(self, service):

        super().__init__()

        self.svc = service
        self.student = None

        self.setWindowTitle(
            "Level Up! Study Tracker"
        )

        self.resize(
            960,
            660
        )

        self.stack = QStackedWidget()

        self.setCentralWidget(
            self.stack
        )

        self.background = QLabel(
            self.stack
        )

        self.background.setPixmap(
            QPixmap(
                "images/background.jpg"
            )
        )

        self.background.setScaledContents(
            True
        )

        self.background.lower()

        self.show_start()

    def resizeEvent(self, event):

        self.background.resize(
            self.stack.size()
        )

        self.background.lower()

        super().resizeEvent(
            event
        )

    def _set(self, page):

        old = (
            self.stack.currentWidget()
        )

        self.stack.addWidget(
            page
        )

        self.stack.setCurrentWidget(
            page
        )

        if old:

            self.stack.removeWidget(
                old
            )

            old.deleteLater()

        self.background.lower()

    def show_start(self):

        self._set(
            StartPage(self)
        )

    def show_name(self):

        self._set(
            NamePage(self)
        )

    def show_avatar(self, name):

        self._set(
            AvatarPage(
                self,
                name
            )
        )

    def show_trackers(self):

        self._set(
            TrackerListPage(self)
        )

    def show_editor(self, tracker):

        self._set(
            EditorPage(
                self,
                tracker
            )
        )

    def show_main(self, tracker_id):

        tracker = (
            self.svc.tracker
            .get_tracker(
                tracker_id
            )
        )

        self._set(
            MainPage(
                self,
                tracker
            )
        )

    def show_congrats(self):

        self._set(
            CongratsPage(self)
        )