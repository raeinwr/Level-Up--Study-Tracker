from core.widgets import (
    Page,
    Sprite,
    btn,
    lab
)


class TrackerListPage(Page):

    def __init__(self, win):

        super().__init__(
            win,
            top=True
        )

        student = win.student

        head = self.root

        header = __import__(
            "PyQt6.QtWidgets",
            fromlist=["QHBoxLayout"]
        ).QHBoxLayout()

        header.addWidget(
            Sprite(
                student.avatar,
                4
            )
        )

        header.addWidget(
            lab(
                student.name.upper()
            )
        )

        header.addStretch()

        self.root.addLayout(
            header
        )

        self.add(

            btn(
                "+ NEW TRACKER",
                lambda: win.show_editor(None),
                "gold"
            ),

            lab(
                "- YOUR TRACKERS -",
                "h2"
            )
        )

        trackers = (
            self.svc.tracker
            .list_trackers(
                student.id
            )
        )

        if not trackers:

            self.add(
                lab(
                    "No trackers yet...",
                    "ghost"
                )
            )

        for tracker in trackers:

            text = (
                f"{tracker.name}  "
                f"({tracker.completed}/{tracker.total})"
            )

            if tracker.done:

                text += "  [CLEAR!]"

            button = btn(
                text,
                lambda tid=tracker.id:
                    win.show_main(tid),
                "green"
                if tracker.done
                else "blue"
            )

            button.setMinimumWidth(
                480
            )

            self.add(
                button
            )

        self.root.addStretch()

        self.add(
            btn(
                "LOG OUT",
                win.show_start,
                "red"
            )
        )