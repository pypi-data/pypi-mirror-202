class MessageQue:
    def __init__(self, name: str):
        self.messages = []
        self.name = name

    def get(self) -> (tuple, None):
        if len(self.messages):
            return self.messages.pop()

    def add(self, topic: str, message: str):
        self.messages.append((topic, message))