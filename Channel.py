# Класс для хранения данных о канале
class Channel:
    def __init__(self, name, link, description=None):
        self.name = name
        self.link = link
        self.description = description