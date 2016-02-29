# RIP
from models import db


class Code(db.Model):
    # Table
    __tablename__ = 'codes'
    # Types
    code_types = {
        'activation': 1, # Account Activation
        'username': 2, # Forgot Username
        'password': 3 # Forgot Password
    }
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    code_type = db.Column(db.Integer)
    code = db.Column(db.Text)
    used = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)



    def __init__(self, user_id, code_type=code_types['activation'], code='', used=False):
        self.user_id = user_id
        self.code_type = code_type
        self.code = code
        self.used = used



    """
        Custom methods
    """
    def save_new_code(self):
        # create a code if none has been made
        if not self.code:
            self.code = Code.gen_code(self.user_id)
        db.session.add(self)
        db.session.commit()


    def deactivate_code(self):
        self.used = True
        db.session.commit()



    """
        Other helpers
    """
    @staticmethod
    def confirm(user_id, code, code_type):
        return Code.query.filter_by(user_id=user_id, code=code, code_type=code_type, used=False).first()


    @staticmethod
    def gen_code(user_id):
        import hashlib
        import uuid
        h = hashlib.sha256()
        h.update(str(uuid.uuid4()))
        h.update(str(user_id))
        return h.hexdigest()


    @staticmethod
    def forgot_password(username):
        from models.user import User
        user = User.query.filter_by(username=username, status=User.status_types['active']).first()
        code = False
        # need to make sure user has an email address registered before creating a code
        if user and user.email:
            code = Code(user.id, Code.code_types['password'])
            code.save_new_code()

        return user, code
