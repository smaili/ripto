# RIP
from models import db

class Liked(db.Model):
    # Table
    __tablename__ = 'liked'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, user_id, comment_id, status):
        self.user_id = user_id
        self.comment_id = comment_id
        self.status = status



    """
        Helpers
    """
    @staticmethod
    def liked_comment(user_id, comment_id, action):
        if action in [1, -1]:
            from models.comment import Comment

            liked = Liked.query.filter_by(user_id=user_id, comment_id=comment_id).first()
            if liked:
                if action == Liked.status_types()['like']:
                    if liked.status == Liked.status_types()['like']:
                        liked.status = Liked.status_types()['undo']
                        #multi = -1
                        db.session.query(Comment).filter_by(id=comment_id).update( {'likes': Comment.likes - 1} )
                    else:
                        if liked.status == Liked.status_types()['dislike']:
                            #multi = 2
                            db.session.query(Comment).filter_by(id=comment_id).update( {'likes': Comment.likes + 1, 'dislikes': Comment.dislikes - 1} )
                        else:
                            #multi = 1
                            db.session.query(Comment).filter_by(id=comment_id).update( {'likes': Comment.likes + 1} )
                        liked.status = Liked.status_types()['like']

                else:
                    if liked.status == Liked.status_types()['dislike']:
                        liked.status = Liked.status_types()['undo']
                        #multi = 1
                        db.session.query(Comment).filter_by(id=comment_id).update( {'dislikes': Comment.dislikes - 1} )
                    else:
                        if liked.status == Liked.status_types()['like']:
                            #multi = -2
                            db.session.query(Comment).filter_by(id=comment_id).update( {'likes': Comment.likes - 1, 'dislikes': Comment.dislikes + 1} )
                        else:
                            #multi = -1
                            db.session.query(Comment).filter_by(id=comment_id).update( {'dislikes': Comment.dislikes + 1} )
                        liked.status = Liked.status_types()['dislike']

            else:
                liked = Liked(user_id, comment_id, action)
                db.session.add(liked)
                if action == Liked.status_types()['like']:
                    #multi = 1
                    db.session.query(Comment).filter_by(id=comment_id).update( {'likes': Comment.likes + 1} )
                else:
                    #multi = -1
                    db.session.query(Comment).filter_by(id=comment_id).update( {'dislikes': Comment.dislikes + 1} )

            #db.session.query(Comment).filter_by(id=comment_id).update({'likes': Comment.likes + (1 * multi)})
            db.session.commit()




    @staticmethod
    def status_types():
        return {
            'dislike': -1,
            'undo': 0,
            'like': 1
        }
