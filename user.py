
class User:
    def __init__(self, id, name, email, password, role):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    def __str__(self):
        return "Name:{},Email:{},Password:{},Role:{}".format(self.name, self.email, self.password, self.role)
    @property   
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    @property
    def is_admin(self):
        if str(self.role).replace("\n","")=="admin":
            return True
        else:
            return False
    def get_id(self):
        return self.email