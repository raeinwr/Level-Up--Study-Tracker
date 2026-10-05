class Pomodoro:

    WORK = 25 * 60
    BREAK = 5 * 60

    def __init__(self):
        self.reset()

    def reset(self):
        self.mode = "FOCUS"
        self.remaining = self.WORK
        self.running = False

    def toggle(self):
        self.running = not self.running

    @property
    def total(self):
        if self.mode == "FOCUS":
            return self.WORK

        return self.BREAK

    @property
    def fraction(self):
        return self.remaining / self.total

    @property
    def clock(self):

        minutes, seconds = divmod(
            self.remaining,
            60
        )

        return f"{minutes:02d}:{seconds:02d}"

    def tick(self):

        if not self.running:
            return False

        self.remaining -= 1

        if self.remaining <= 0:

            if self.mode == "FOCUS":
                self.mode = "BREAK"
            else:
                self.mode = "FOCUS"

            self.remaining = self.total

            return True

        return False