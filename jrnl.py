class Journals:
    def __init__(self, id, author, emotion, weather, content, date, private):
        self.id = id
        self.author = author
        self.emotion = emotion
        self.weather = weather
        self.content = content
        self.date = date
        self.private = private

    def __str__(self):
        return "Author:{},Emotion:{},Weather:{},Content:{},Date:{},Private:{}".format(self.author, self.emotion, self.weather, self.content, self.date,self.private)
