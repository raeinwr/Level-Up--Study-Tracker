from .model import Student


AVATARS = ("girl", "boy")


class StudentService:

    def __init__(self, repo):
        self.repo = repo

    @staticmethod
    def clean_name(name):
        name = name.strip()

        if not name:
            raise ValueError("Please enter your name.")

        return name

    def find(self, name):
        name = self.clean_name(name)
        return self.repo.find_student(name)

    def register(self, name, avatar):
        name = self.clean_name(name)

        if avatar not in AVATARS:
            raise ValueError("Pick an avatar first.")

        return self.repo.create_student(name, avatar)