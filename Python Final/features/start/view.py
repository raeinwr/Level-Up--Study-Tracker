from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit

from core.widgets import (
    Page,
    Sprite,
    btn,
    lab
)

from features.student.service import AVATARS


CENTER = Qt.AlignmentFlag.AlignCenter


class StartPage(Page):

    def __init__(self, win):

        super().__init__(win)

        title = lab("")

        pixmap = QPixmap(
            "images/title.png"
        )

        title.setPixmap(
            pixmap.scaled(
                850,
                180,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        row = QHBoxLayout()

        row.setAlignment(
            CENTER
        )

        for key in AVATARS:

            row.addWidget(
                Sprite(key, 5)
            )

        self.add(title)

        self.root.addLayout(
            row
        )

        actions = QHBoxLayout()
        actions.setAlignment(CENTER)
        actions.setSpacing(12)

        start = btn("START", win.show_name, "blue")
        exit_button = btn("EXIT", win.close, "red")

        start.setFixedSize(180, 52)
        exit_button.setFixedSize(180, 52)

        actions.addWidget(start)
        actions.addWidget(exit_button)
        self.root.addLayout(actions)


class NamePage(Page):

    def __init__(self, win):

        super().__init__(win)

        self.edit = QLineEdit()

        self.edit.setMaxLength(20)

        self.edit.setFixedWidth(360)

        self.edit.setAlignment(
            CENTER
        )

        self.edit.returnPressed.connect(
            self.go
        )

        self.add(
            lab(
                "WHO IS STUDYING?",
                "h2"
            ),
            self.edit
        )

        actions = QHBoxLayout()
        actions.setAlignment(CENTER)
        actions.setSpacing(12)

        ok = btn("OK", self.go, "gold")
        back = btn("BACK", win.show_start, "grey")

        ok.setFixedSize(180, 52)
        back.setFixedSize(180, 52)

        actions.addWidget(back)
        actions.addWidget(ok)
        self.root.addLayout(actions)

    def go(self):

        try:

            student = (
                self.svc
                .student
                .find(
                    self.edit.text()
                )
            )

        except ValueError as e:

            return self.warn(
                str(e)
            )

        if student:

            self.win.student = student

            self.win.show_trackers()

        else:

            self.win.show_avatar(
                self.edit.text().strip()
            )


class AvatarPage(Page):

    def __init__(self, win, name):

        super().__init__(win)

        self.name = name
        self.choice = None
        self.sprites = {}

        row = QHBoxLayout()

        row.setAlignment(
            CENTER
        )

        for key in AVATARS:

            sprite = Sprite(
                key,
                9
            )

            sprite.clicked.connect(
                self.pick
            )

            self.sprites[key] = sprite

            row.addWidget(
                sprite
            )

        self.add(

            lab(
                f"WELCOME, {name.upper()}!",
                "h2"
            ),

            lab(
                "PICK YOUR AVATAR"
            )
        )

        self.root.addLayout(
            row
        )

        actions = QHBoxLayout()
        actions.setAlignment(CENTER)
        actions.setSpacing(12)

        back = btn("BACK", win.show_name, "grey")
        confirm = btn("OK", self.confirm, "gold")

        back.setFixedSize(180, 52)
        confirm.setFixedSize(180, 52)

        actions.addWidget(back)
        actions.addWidget(confirm)
        self.root.addLayout(actions)

    def pick(self, key):

        self.choice = key

        for name, sprite in self.sprites.items():

            sprite.selected = (
                name == key
            )

            sprite.update()

    def confirm(self):

        try:

            self.win.student = (
                self.svc
                .student
                .register(
                    self.name,
                    self.choice
                )
            )

        except ValueError as e:

            return self.warn(
                str(e)
            )

        self.win.show_trackers()