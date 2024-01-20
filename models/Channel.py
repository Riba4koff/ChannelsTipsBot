# Класс для хранения данных о канале
class Channel:
    def __init__(self, id, name, link, description=None):
        self.id = id
        self.name = name
        self.link = link
        self.description = description
