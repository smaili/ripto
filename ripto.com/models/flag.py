# RIP
from models import db

class Flag(db.Model):
    # Table
    __tablename__ = 'flags'
    # Types
    flag_types = {
        'u': 1, # User
        'm': 2, # Memorial
        'c': 3, # Comment
        'e': 4 # Email
    }
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    flag_type = db.Column(db.Integer)
    accused_id = db.Column(db.Integer)
    reporter_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, flag_type, accused_id, reporter_id):
        self.flag_type = flag_type
        self.accused_id = accused_id
        self.reporter_id = reporter_id
        # fields to validate
        self.errors = { 'flag_type':'', 'accused_id':'', 'reporter_id':'' }



    """
        Custom methods
    """
    def validate(self):
        # validate each field depending on what the current step it is
        isValid = True
        for field in self.errors:
            methodToCall = getattr(self, 'check_' + field)
            self.errors[field] = methodToCall(getattr(self, field))
            if self.errors[field] != 'ok':
                isValid = False

        return isValid


    def save_new_flag(self):
        db.session.add(self)
        db.session.commit()



    """
        Validator helpers
    """
    @staticmethod
    def check_flag_type(flag_type):
        if flag_type:
            return 'ok'
        else:
            return 'blank'


    @staticmethod
    def check_accused_id(accused_id):
        if accused_id:
            return 'ok'
        else:
            return 'blank'


    @staticmethod
    def check_reporter_id(reporter_id):
        if reporter_id:
            return 'ok'
        else:
            return 'blank'




    """
        Other helpers
    """
    @staticmethod
    def get_flag_name(flag_type):
        if flag_type == 'u':
            return 'user'
        elif flag_type == 'm':
            return 'memorial'
        elif flag_type == 'c':
            return 'comment'


    @staticmethod
    def report(flag_type, accused_id, reporter_id):
        flag = False

        if flag_type in Flag.flag_types:
            if flag_type == 'u':
                from models.user import User
                user = User.query.filter_by(username=accused_id).first()
                accused_id = user.id if user else False

            elif flag_type == 'm':
                from models.memorial import Memorial
                memorial = Memorial.query.filter_by(url=accused_id).first()
                accused_id = memorial.id if memorial else False
            
            elif flag_type == 'c':
                from models.comment import Comment
                comment = Comment.query.filter_by(id=accused_id).first()
                accused_id = comment.id if comment else False

            if accused_id:
                flag_type = Flag.flag_types[flag_type]
                exists = Flag.query.filter_by(flag_type=flag_type, accused_id=accused_id, reporter_id=reporter_id).first()
                if not exists:
                    flag = Flag(flag_type, accused_id, reporter_id)
                    flag.save_new_flag()

        return flag
