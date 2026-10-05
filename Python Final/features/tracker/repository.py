"""Repository layer: all SQL lives here. Returns model objects."""
from features.tracker.model import Tracker, Topic


class Repository:
    def __init__(self, conn):
        self.conn = conn

    # trackers
    def _tracker(self, r):
        return Tracker(**dict(r), topics=self.list_topics(r["id"]))

    def get_tracker(self, tracker_id):
        r = self.conn.execute(
            "SELECT * FROM trackers WHERE id=?",
            (tracker_id,),
        ).fetchone()
        return self._tracker(r) if r else None

    def list_trackers(self, student_id):
        rows = self.conn.execute(
            "SELECT * FROM trackers WHERE student_id=? ORDER BY id DESC",
            (student_id,),
        ).fetchall()
        return [self._tracker(r) for r in rows]

    def create_tracker(self, student_id, name):
        with self.conn:
            return self.conn.execute(
                "INSERT INTO trackers(student_id,name) VALUES(?,?)",
                (student_id, name),
            ).lastrowid

    def update_tracker(self, tracker_id, name):
        with self.conn:
            self.conn.execute(
                "UPDATE trackers SET name=? WHERE id=?",
                (name, tracker_id),
            )

    def set_tracker_done(self, tracker_id, done):
        with self.conn:
            self.conn.execute(
                "UPDATE trackers SET done=? WHERE id=?",
                (int(done), tracker_id),
            )

    # topics
    def list_topics(self, tracker_id):
        rows = self.conn.execute(
            "SELECT * FROM topics WHERE tracker_id=? ORDER BY id",
            (tracker_id,),
        )
        return [Topic(**dict(r)) for r in rows]

    def add_topic(self, tracker_id, name, hours):
        with self.conn:
            self.conn.execute(
                "INSERT INTO topics(tracker_id,name,hours,studied_seconds) VALUES(?,?,?,0)",
                (tracker_id, name, hours),
            )

    def update_topic(self, topic_id, name, hours):
        with self.conn:
            self.conn.execute(
                "UPDATE topics SET name=?, hours=? WHERE id=?",
                (name, hours, topic_id),
            )

    def delete_topic(self, topic_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM topics WHERE id=?",
                (topic_id,),
            )

    def set_topic_done(self, topic_id, done):
        with self.conn:
            self.conn.execute(
                "UPDATE topics SET done=? WHERE id=?",
                (int(done), topic_id),
            )

    def add_study_seconds(self, topic_id, seconds):
        seconds = int(seconds)
        if seconds <= 0:
            return

        with self.conn:
            self.conn.execute(
                "UPDATE topics SET studied_seconds = studied_seconds + ? WHERE id=?",
                (seconds, topic_id),
            )
