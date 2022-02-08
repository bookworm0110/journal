class Comments:
    def __init__(self, id, author, date, content,entryid):
        self.id=id
        self.date=date
        self.entryid=entryid
        self.content=content
        self.author=author
    def __str__(self):
        return "Date:{},Entry:{},Content:{},Author:{}".format(self.date,self.entryid,self.content,self.author)