from PyQt6.QtCore import (
    Qt,
    QVariantAnimation,
    pyqtSignal
)

from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QPixmap
)

from PyQt6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QVBoxLayout
)

from core.theme import (
    GOLD,
    GREEN,
    RED,
    GREY,
    PANEL
)


AVATAR_IMAGES = {
    "girl": "images/girl_avatar.png",
    "boy": "images/boy_avatar.png"
}


CENTER = Qt.AlignmentFlag.AlignCenter


def draw_sprite(painter, key, x, y, px):

    pixmap = QPixmap(
        AVATAR_IMAGES[key]
    )

    target_height = 14 * px

    pixmap = pixmap.scaled(
        int(
            pixmap.width()
            * target_height
            / pixmap.height()
        ),
        target_height,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.FastTransformation
    )

    painter.drawPixmap(
        x,
        y,
        pixmap
    )


class Sprite(QWidget):

    clicked = pyqtSignal(str)

    def __init__(self, key, px=6):

        super().__init__()

        self.key = key
        self.px = px
        self.selected = False

        self.setFixedSize(
            14 * px + 12,
            14 * px + 12
        )

    def mousePressEvent(self, event):

        self.clicked.emit(
            self.key
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        draw_sprite(
            painter,
            self.key,
            6,
            6,
            self.px
        )

        if self.selected:

            painter.setPen(
                QPen(
                    QColor(GOLD),
                    4
                )
            )

            painter.drawRect(
                2,
                2,
                self.width() - 4,
                self.height() - 4
            )


def lab(text, role=None):

    label = QLabel(text)

    label.setAlignment(
        CENTER
    )

    if role:
        label.setProperty(
            "role",
            role
        )

    return label


def btn(text, slot, variant=None):

    button = QPushButton(text)

    def safe_slot():

        try:
            slot()

        except Exception as e:

            QMessageBox.critical(
                None,
                "ERROR",
                f"{type(e).__name__}:\n{e}"
            )

            raise

    button.clicked.connect(
        safe_slot
    )

    button.setCursor(
        Qt.CursorShape.PointingHandCursor
    )

    if variant:

        button.setProperty(
            "variant",
            variant
        )

    return button


class Page(QWidget):

    def __init__(self, win, top=False):

        super().__init__()

        self.win = win
        self.svc = win.svc

        self.root = QVBoxLayout(
            self
        )

        self.root.setSpacing(12)

        if top:

            self.root.setAlignment(
                Qt.AlignmentFlag.AlignTop
                | Qt.AlignmentFlag.AlignHCenter
            )

        else:

            self.root.setAlignment(
                CENTER
            )

    def add(self, *widgets):

        for widget in widgets:

            self.root.addWidget(
                widget,
                alignment=CENTER
            )

    def warn(self, message):

        QMessageBox.warning(
            self,
            "Hey!",
            message
        )