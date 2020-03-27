class MusicProposition():
    def __init__(self, name, channel, id):
        self.name = name
        self.channel = channel
        self.id = id

    def __repr__(self):
        return f'{self.name}, from {self.channel}'
