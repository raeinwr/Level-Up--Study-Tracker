from dataclasses import replace

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QProgressBar,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from core.theme import GREEN, GOLD, RED, PURPLE
from core.widgets import Page, Sprite, btn, lab
from features.pomodoro.service import Pomodoro
from features.progress_bar.view import Journey
from features.tracker.model import Topic


def format_duration(seconds):
    """Turn seconds into a simple player-friendly duration."""
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60

    if hours:
        return f"{hours}h {minutes:02d}m"

    return f"{minutes}m"


class EditorPage(Page):

    def __init__(self, win, tracker):
        super().__init__(win, top=True)

        self.tracker = tracker
        self.editing = None
        self.topics = (
            [replace(topic) for topic in tracker.topics]
            if tracker
            else []
        )

        self.add(
            lab(
                "EDIT TOPICS" if tracker else "NEW TRACKER",
                "h2",
            )
        )

        self.tname = QLineEdit(tracker.name if tracker else "")
        self.tname.setPlaceholderText("Tracker name")
        self.tname.setFixedWidth(400)
        self.tname.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.topic = QLineEdit()
        self.topic.setPlaceholderText("Topic")
        self.topic.setFixedWidth(300)
        self.topic.returnPressed.connect(self.add_topic)

        self.hours = QDoubleSpinBox()
        self.hours.setRange(0.5, 24)
        self.hours.setSingleStep(0.5)
        self.hours.setValue(1)
        self.hours.setSuffix(" h")
        self.hours.setFixedSize(140, 40)
        self.hours.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.UpDownArrows)

        self.addb = btn("ADD", self.add_topic)
        self.addb.setMinimumWidth(130)

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(self.topic)
        row.addWidget(self.hours)
        row.addWidget(self.addb)

        self.lst = QListWidget()
        self.lst.setFixedSize(640, 240)

        actions = QHBoxLayout()
        actions.setSpacing(8)

        for text, slot, variant in (
            ("EDIT", self.edit_sel, "blue"),
            ("DELETE", self.delete_sel, "red"),
            ("DONE", self.save, "gold"),
            (
                "CANCEL",
                (lambda: win.show_main(tracker.id)) if tracker else win.show_trackers,
                "grey",
            ),
        ):
            button = btn(text, slot, variant)
            button.setMinimumWidth(130)
            actions.addWidget(button)

        self.add(self.tname)
        self.root.addLayout(row)
        self.add(self.lst)
        self.root.addLayout(actions)
        self.refresh()

    def refresh(self):
        self.lst.clear()

        for topic in self.topics:
            status = "[x]" if topic.done else "[ ]"
            studied = format_duration(topic.studied_seconds)
            planned = format_duration(topic.planned_seconds)

            self.lst.addItem(
                f"{status}  {topic.name}  |  {planned} planned  |  {studied} studied"
            )

    def add_topic(self):
        name = self.topic.text().strip()
        if not name:
            return

        if self.editing is None:
            self.topics.append(
                Topic(
                    None,
                    self.tracker.id if self.tracker else 0,
                    name,
                    self.hours.value(),
                )
            )
        else:
            topic = self.topics[self.editing]
            topic.name = name
            topic.hours = self.hours.value()
            self.editing = None
            self.addb.setText("ADD")

        self.topic.clear()
        self.hours.setValue(1)
        self.refresh()

    def edit_sel(self):
        index = self.lst.currentRow()
        if index >= 0:
            self.editing = index
            topic = self.topics[index]
            self.topic.setText(topic.name)
            self.hours.setValue(topic.hours)
            self.addb.setText("UPDATE")

    def delete_sel(self):
        index = self.lst.currentRow()
        if index >= 0:
            self.topics.pop(index)
            self.editing = None
            self.addb.setText("ADD")
            self.topic.clear()
            self.hours.setValue(1)
            self.refresh()

    def save(self):
        try:
            tracker_id = self.svc.tracker.save_tracker(
                self.win.student.id,
                self.tracker.id if self.tracker else None,
                self.tname.text(),
                self.topics,
            )
        except ValueError as e:
            return self.warn(str(e))

        self.win.show_main(tracker_id)


class MainPage(QWidget):
    """Main dashboard with planned-vs-actual study-time tracking."""

    def __init__(self, win, tracker):
        super().__init__()

        self.win = win
        self.svc = win.svc
        self.tracker = tracker
        self.pomo = Pomodoro()
        self.session_seconds = 0
        self.save_interval = 5

        student = win.student

        grid = QGridLayout(self)
        grid.setContentsMargins(14, 12, 14, 12)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 1)
        grid.setRowMinimumHeight(0, 86)
        grid.setRowStretch(1, 1)
        grid.setRowMinimumHeight(2, 105)

        header = QFrame()
        header.setObjectName("quest")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 18, 8)
        header_layout.setSpacing(14)

        avatar = Sprite(student.avatar, 4)
        header_layout.addWidget(avatar)

        profile = QVBoxLayout()
        profile.setSpacing(2)
        profile.addWidget(lab(student.name.upper(), "h2"))
        profile.addWidget(lab("TRAINER", "small"))
        header_layout.addLayout(profile)
        header_layout.addSpacing(20)

        quest_info = QVBoxLayout()
        quest_info.setSpacing(3)
        quest_info.addWidget(lab(f"{tracker.name.upper()}", "quest_title"))
        quest_info.addWidget(lab("TRAINER QUEST  •  TRAIN YOUR FOCUS  •  CLEAR YOUR TASKS", "small"))
        header_layout.addLayout(quest_info, 1)

        header_layout.addWidget(btn("BACK", win.show_trackers, "red"))
        grid.addWidget(header, 0, 0, 1, 3)

        sidebar = QFrame()
        sidebar.setObjectName("hud")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(14, 16, 14, 16)
        side_layout.setSpacing(10)
        side_layout.addWidget(lab("TRAINER MENU", "h2"))
        side_layout.addWidget(lab("Choose an action", "small"))
        side_layout.addSpacing(4)

        for button in (
            btn("🎒  TRACKERS", win.show_trackers, "blue"),
            btn("✎  EDIT QUESTS", lambda: win.show_editor(self.tracker), "purple"),
            btn("↩  EXIT", win.show_trackers, "red"),
        ):
            button.setMinimumHeight(46)
            side_layout.addWidget(button)

        side_layout.addStretch()
        grid.addWidget(sidebar, 1, 0)

        grid.addWidget(self._pomo_box(), 1, 1)
        grid.addWidget(self._check_box(), 1, 2)

        self.journey = Journey(student.avatar)
        self.journey.set_progress(tracker.completed, tracker.total, False)
        grid.addWidget(self.journey, 2, 0, 1, 3)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def _pomo_box(self):
        frame = QFrame()
        frame.setObjectName("card")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(8)

        layout.addWidget(lab("FOCUS MODE", "h2"))
        layout.addWidget(lab("Select a topic and start studying.", "small"))

        self.topic_title = lab("CURRENT TOPIC", "small")
        layout.addWidget(self.topic_title)

        self.topic_combo = QComboBox()
        self.topic_combo.setMinimumHeight(40)
        self.topic_combo.currentIndexChanged.connect(self.selected_topic_changed)
        layout.addWidget(self.topic_combo)

        stats = QGridLayout()
        stats.setHorizontalSpacing(10)
        self.planned_label = lab("PLANNED\n0m", "small")
        self.studied_label = lab("STUDIED\n0m", "small")
        self.remaining_label = lab("REMAINING\n0m", "small")
        stats.addWidget(self.planned_label, 0, 0)
        stats.addWidget(self.studied_label, 0, 1)
        stats.addWidget(self.remaining_label, 0, 2)
        layout.addLayout(stats)

        self.topic_time_bar = QProgressBar()
        self.topic_time_bar.setRange(0, 100)
        self.topic_time_bar.setTextVisible(True)
        self.topic_time_bar.setFormat("%p% of planned time")
        self.topic_time_bar.setMinimumHeight(22)
        layout.addWidget(self.topic_time_bar)

        self.msg = lab("")
        layout.addWidget(self.msg)

        self.clock = lab("", "clock")
        layout.addWidget(self.clock)

        self.bar = QProgressBar()
        self.bar.setRange(0, 1000)
        self.bar.setTextVisible(False)
        self.bar.setMinimumHeight(18)
        layout.addWidget(self.bar)

        controls = QHBoxLayout()
        controls.setSpacing(10)
        self.go = btn("▶  START", self.toggle, "blue")
        reset = btn("↻  RESET", self.reset, "purple")
        self.go.setMinimumHeight(46)
        reset.setMinimumHeight(46)
        controls.addWidget(self.go)
        controls.addWidget(reset)
        layout.addLayout(controls)

        self._populate_topics()
        self.draw()
        return frame

    def _populate_topics(self):
        self.topic_combo.blockSignals(True)
        self.topic_combo.clear()
        for topic in self.tracker.topics:
            self.topic_combo.addItem(topic.name, topic.id)
        if self.topic_combo.count():
            self.topic_combo.setCurrentIndex(0)
        self.topic_combo.blockSignals(False)
        self.update_topic_info()

    def _check_box(self):
        frame = QFrame()
        frame.setObjectName("card")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(0)

        layout.addWidget(lab("QUEST OBJECTIVES", "h2"))
        layout.addWidget(lab("Complete each task to clear the quest.", "small"))
        layout.addSpacing(6)

        self.topic_checks = {}
        for topic in self.tracker.topics:
            checkbox = QCheckBox()
            checkbox.setObjectName("questCheck")
            checkbox.setMinimumHeight(62)
            checkbox.setChecked(bool(topic.done))
            self.topic_checks[topic.id] = checkbox
            checkbox.toggled.connect(
                lambda checked, tid=topic.id: self.on_check(tid, checked)
            )
            layout.addWidget(checkbox)

        layout.addStretch()
        self.refresh_topic_checks()
        return frame

    def current_topic_id(self):
        if self.topic_combo.count() == 0:
            return None
        return self.topic_combo.currentData()

    def current_topic(self):
        topic_id = self.current_topic_id()
        return next((topic for topic in self.tracker.topics if topic.id == topic_id), None)

    def selected_topic_changed(self, index):
        if self.pomo.running and self.pomo.mode == "FOCUS":
            self.flush_study_time()
        self.update_topic_info()

    def update_topic_info(self):
        topic = self.current_topic()
        if topic is None:
            self.topic_title.setText("CURRENT TOPIC")
            self.planned_label.setText("PLANNED\n0m")
            self.studied_label.setText("STUDIED\n0m")
            self.remaining_label.setText("REMAINING\n0m")
            self.topic_time_bar.setValue(0)
            return

        planned = topic.planned_seconds
        studied = topic.studied_seconds
        remaining = topic.remaining_seconds
        percent = int(round(topic.time_progress * 100))

        self.topic_title.setText(f"CURRENT TOPIC  •  {topic.name.upper()}")
        self.planned_label.setText(f"PLANNED\n{format_duration(planned)}")
        self.studied_label.setText(f"STUDIED\n{format_duration(studied)}")
        remaining_text = format_duration(remaining) if remaining else "READY!"
        self.remaining_label.setText(f"REMAINING\n{remaining_text}")
        self.topic_time_bar.setValue(percent)
        self.refresh_topic_checks()

    def refresh_topic_checks(self):
        if not hasattr(self, "topic_checks"):
            return
        for topic in self.tracker.topics:
            checkbox = self.topic_checks.get(topic.id)
            if checkbox is None:
                continue
            planned = format_duration(topic.planned_seconds)
            studied = format_duration(topic.studied_seconds)
            detail = f"{planned} planned  •  {studied} studied"
            if not topic.remaining_seconds:
                detail += "  •  TIME GOAL MET"
            checkbox.setText(f"{topic.name}\n{detail}")

    def on_check(self, topic_id, checked):
        self.flush_study_time()
        self.tracker = self.svc.tracker.set_topic_done(self.tracker.id, topic_id, checked)
        self.journey.set_progress(self.tracker.completed, self.tracker.total)
        self.update_topic_info()
        if self.tracker.complete:
            QTimer.singleShot(1300, self.win.show_congrats)

    def flush_study_time(self):
        if self.session_seconds <= 0:
            return
        topic_id = self.current_topic_id()
        if topic_id is None:
            self.session_seconds = 0
            return
        self.tracker = self.svc.tracker.add_study_seconds(
            self.tracker.id, topic_id, self.session_seconds
        )
        self.session_seconds = 0
        self.update_topic_info()

    def draw(self):
        pomo = self.pomo
        self.msg.setText("Time to FOCUS!" if pomo.mode == "FOCUS" else "Take a BREAK!")
        self.clock.setText(pomo.clock)
        self.bar.setValue(int(pomo.fraction * 1000))
        if pomo.fraction > 0.5:
            color = GREEN
        elif pomo.fraction > 0.2:
            color = GOLD
        else:
            color = RED
        self.bar.setStyleSheet(
            f"QProgressBar {{ background:#DDECF4; border:2px solid #1B2A52; border-radius:5px; }} "
            f"QProgressBar::chunk {{ background:{color}; border-radius:3px; }}"
        )

    def tick(self):
        if self.pomo.running and self.pomo.mode == "FOCUS":
            if self.current_topic_id() is not None:
                self.session_seconds += 1
                if self.session_seconds >= self.save_interval:
                    self.flush_study_time()
        if self.pomo.tick():
            self.flush_study_time()
            QApplication.beep()
        self.draw()

    def toggle(self):
        if not self.pomo.running:
            if self.pomo.mode == "FOCUS" and self.current_topic_id() is None:
                return self.warn("Choose a topic before starting the focus timer.")
            self.pomo.toggle()
            self.go.setText("Ⅱ  PAUSE")
            return
        self.flush_study_time()
        self.pomo.toggle()
        self.go.setText("▶  START")

    def reset(self):
        self.flush_study_time()
        self.pomo.reset()
        self.go.setText("▶  START")
        self.draw()

    def closeEvent(self, event):
        self.flush_study_time()
        event.accept()


class CongratsPage(Page):
    def __init__(self, win):
        super().__init__(win)

        self.add(
            lab("CONGRATULATIONS!", "title"),
            Sprite(win.student.avatar, 10),
            lab("QUEST COMPLETE!", "h2"),
            lab("Would you like to create another tracker?"),
        )

        row = QHBoxLayout()
        row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        row.addWidget(btn("YES", lambda: win.show_editor(None)))
        row.addWidget(btn("NO", win.show_trackers, "red"))
        self.root.addLayout(row)
