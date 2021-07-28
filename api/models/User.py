class CreateUserRequest():
    def __init__(self):
        self.nama = None
        self.username = None
        self.password = None
        self.jabatan = None
        self.isAdmin = None

class UserModelView():
    def __init__(self):
        self.id = None
        self.username = None
        self.nama = None
        self.jabatan = None
        self.isAdmin = None

class EditUserRequest():
    def __init__(self):
        self.id = None
        self.username = None
        self.nama = None
        self.jabatan = None
        self.isAdmin = None
        self.password = None