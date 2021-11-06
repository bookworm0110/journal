
class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


    def __str__(self):
        return "Name:{},Email:{},Password:{}".format(self.name, self.email, self.password)
    @property   
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.email
    
