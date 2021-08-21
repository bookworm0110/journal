class Journals:
    def __init__(self, id, author, emotion, weather, content, date):
        self.id = id
        self.author = author
        self.emotion = emotion
        self.weather = weather
        self.content = content
        self.date = date

    def __str__(self):
        return "Author:{},Emotion:{},Weather:{},Content:{},Date:{}".format(self.author, self.emotion, self, weather, self.content, self.date)
