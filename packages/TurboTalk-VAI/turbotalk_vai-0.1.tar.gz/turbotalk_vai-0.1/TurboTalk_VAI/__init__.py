# TurboTalk_VAI/__init__.py

class TurboTalk:
    def __init__(self, company_name, bot_name, behaviour):
        self.company_name = company_name
        self.bot_name = bot_name
        self.behaviour = behaviour
        self.response = ""

    def generate_response(self, user_input):
        self.response = f"{self.bot_name} says: '{user_input}' is noted. I behave {self.behaviour}."
        
    def get_response(self):
        return self.response
