class Message:
    def __init__(self, sender, receiver, type, content):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.content = content

    def __str__(self):
        return f"{self.sender} -> {self.receiver} [{self.type}]\n{self.content}"