# user.py

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.skills = []
        self.is_premium = False

    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
            return f"{skill} added."
        return f"{skill} already exists."

    def display_skills(self):
        return ", ".join(self.skills) if self.skills else "No skills listed yet."
