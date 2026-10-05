from PyQt6.QtCore import QVariantAnimation
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget

from core.theme import GOLD, GREEN, GREY, INK, PANEL_DARK, RED, BLUE, WHITE
from core.widgets import draw_sprite


class Journey(QWidget):
    def __init__(self, avatar):
        super().__init__()
        self.avatar = avatar
        self.value = 0.0
        self.done = 0
        self.total = 0
        self.setMinimumHeight(120)
        self.setMaximumHeight(140)
        self.anim = QVariantAnimation(self)
        self.anim.setDuration(700)
        self.anim.valueChanged.connect(self._set)

    def _set(self, value):
        self.value = float(value)
        self.update()

    def set_progress(self, done, total, animate=True):
        self.done = done
        self.total = total
        target = done / total if total else 0.0
        self.anim.stop()
        if animate:
            self.anim.setStartValue(float(self.value))
            self.anim.setEndValue(float(target))
            self.anim.start()
        else:
            self._set(target)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        rect = self.rect().adjusted(3, 3, -3, -3)
        painter.fillRect(rect, QColor(PANEL_DARK))
        painter.setPen(QPen(QColor(WHITE), 2))
        painter.drawRect(rect)

        painter.setPen(QColor(GOLD))
        painter.drawText(24, 28, "★  TRAINER PROGRESS")

        painter.setPen(QColor(WHITE))
        painter.drawText(
            max(220, self.width() - 230),
            28,
            f"{self.done} / {self.total} QUESTS CLEAR" if self.total else "0 / 0 QUESTS CLEAR",
        )

        x0 = 28
        x1 = self.width() - 150
        y = 65
        width = max(120, x1 - x0)

        painter.setPen(QPen(QColor(WHITE), 3))
        painter.setBrush(QColor("#DCECF5"))
        painter.drawRect(x0, y, width, 25)

        painter.setPen(QPen(QColor(BLUE), 1))
        painter.setBrush(QColor(BLUE))
        painter.drawRect(x0 + 3, y + 3, max(0, int((width - 6) * self.value)), 19)

        if self.total:
            for k in range(1, self.total + 1):
                marker_x = x0 + int(width * k / self.total)
                painter.setPen(QPen(QColor(PANEL_DARK), 2))
                painter.setBrush(QColor(GREEN if k <= self.done else GREY))
                painter.drawEllipse(marker_x - 5, y + 8, 10, 10)

        percent = int(round(self.value * 100))
        painter.setPen(QColor(GOLD))
        painter.drawText(self.width() - 125, 82, f"{percent}%")

        avatar_x = x0 + int(width * self.value) - 20
        draw_sprite(painter, self.avatar, avatar_x, 91, 3)

        flag_x = self.width() - 75
        painter.setPen(QPen(QColor(WHITE), 3))
        painter.drawLine(flag_x, 84, flag_x, 45)
        painter.setBrush(QColor(RED))
        painter.drawRect(flag_x, 45, 30, 16)
        painter.setPen(QColor(WHITE))
        painter.drawText(flag_x - 5, 108, "GOAL")
