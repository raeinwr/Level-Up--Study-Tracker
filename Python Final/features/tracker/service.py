class TrackerService:

    def __init__(self, repo):
        self.repo = repo

    def list_trackers(self, student_id):
        return self.repo.list_trackers(student_id)

    def get_tracker(self, tracker_id):
        return self.repo.get_tracker(tracker_id)

    def save_tracker(self, student_id, tracker_id, name, topics):
        name = name.strip()

        if not name:
            raise ValueError("Give the tracker a name.")

        if not topics:
            raise ValueError("Add at least one topic.")

        if any(topic.hours <= 0 for topic in topics):
            raise ValueError("Hours must be greater than zero.")

        if tracker_id is None:
            tracker_id = self.repo.create_tracker(student_id, name)
        else:
            self.repo.update_tracker(tracker_id, name)

            keep = {
                topic.id
                for topic in topics
                if topic.id
            }

            for old in self.repo.list_topics(tracker_id):
                if old.id not in keep:
                    self.repo.delete_topic(old.id)

        for topic in topics:
            if topic.id:
                self.repo.update_topic(
                    topic.id,
                    topic.name,
                    topic.hours,
                )
            else:
                self.repo.add_topic(
                    tracker_id,
                    topic.name,
                    topic.hours,
                )

        # EditorPage needs the numeric ID.
        return tracker_id

    def set_topic_done(self, tracker_id, topic_id, done):
        self.repo.set_topic_done(topic_id, done)
        return self.sync_done(tracker_id)

    def add_study_seconds(self, tracker_id, topic_id, seconds):
        self.repo.add_study_seconds(topic_id, seconds)
        return self.repo.get_tracker(tracker_id)

    def sync_done(self, tracker_id):
        tracker = self.repo.get_tracker(tracker_id)

        if tracker is None:
            return None

        self.repo.set_tracker_done(
            tracker_id,
            tracker.complete,
        )

        tracker.done = int(tracker.complete)
        return tracker
