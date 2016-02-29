# RIP
from models import db

class Viewed(db.Model):
    # Table
    __tablename__ = 'viewed'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ip_addr = db.Column(db.Text)
    memorial_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, user_id, ip_addr, memorial_id):
        self.user_id = user_id
        self.ip_addr = ip_addr
        self.memorial_id = memorial_id




    """
        Helpers
    """
    @staticmethod
    def viewed_memorial(user_id, ip_addr, memorial_id):
#        if user_id > 0:
#            viewed = Viewed.query.filter_by(user_id=user_id, memorial_id=memorial_id).first()
#        else:
#            viewed = Viewed.query.filter_by(ip_addr=ip_addr, memorial_id=memorial_id).first()
#        if viewed:
#            viewed.modified = db.func.now()
#        else:

        from models.memorial import Memorial
        viewed = Viewed(user_id, ip_addr, memorial_id)
        db.session.add(viewed)
        db.session.query(Memorial).filter_by(id=memorial_id).update({'views': Memorial.views + 1})
        db.session.commit()
