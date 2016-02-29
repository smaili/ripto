# RIP
from models import db

class Remembered(db.Model):
    # Table
    __tablename__ = 'remembered'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    memorial_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, user_id, memorial_id, status):
        self.user_id = user_id
        self.memorial_id = memorial_id
        self.status = status



    """
        Helpers
    """
    @staticmethod
    def remembered_memorial(user_id, memorial_id):
        from models.memorial import Memorial

        remembered = Remembered.query.filter_by(user_id=user_id, memorial_id=memorial_id).first()
        if remembered:
            if remembered.status == Remembered.status_types()['remembered']:
                remembered.status = Remembered.status_types()['unremembered']
                multi = -1
            else:
                remembered.status = Remembered.status_types()['remembered']
                multi = 1
        else:
            remembered = Remembered(user_id, memorial_id, Remembered.status_types()['remembered'])
            db.session.add(remembered)
            multi = 1
        
        db.session.query(Memorial).filter_by(id=memorial_id).update({'remembers': Memorial.remembers + (1 * multi)})
        db.session.commit()




    @staticmethod
    def status_types():
        return {
            'remembered': 1,
            'unremembered': 2
        }
