# RIP
from models import db


class Comment(db.Model):
    # Table
    __tablename__ = 'comments'
    # Types
    #relation_types = {
    #    1: gettext('Family'),
    #    2: gettext('Friend'),
    #    3: gettext('Romantic'),
    #    4: gettext('Colleague'),
    #    5: gettext('Fan')
    #}
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    memorial_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    text = db.Column(db.Text)
    parent_id = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, text='', parent_id=0, likes=0, dislikes=0):
        self.memorial_id = 0
        self.user_id = 0
        self.text = text
        self.parent_id = parent_id
        self.likes = likes
        self.dislikes = dislikes
        # fields to validate
        self.errors = { 'text':'' }



    """
        Custom methods
    """
    def validate(self):
        # TODO - sanitize all text inputs
        # TODO - make sure file size/length/type is all correct
        # TODO - make sure no swear words

        # validate each field depending on what the current step it is
        isValid = True
        for field in self.errors:
            methodToCall = getattr(self, 'check_' + field)
            self.errors[field] = methodToCall(getattr(self, field))
            if self.errors[field] != 'ok':
                isValid = False

        return isValid


    def save_new_comment(self):
        db.session.add(self)
        db.session.commit()


    def get_user(self):
        from models.user import User
        return User.query.filter_by(id=self.user_id).first()



    """
        Validator helpers
    """
    @staticmethod
    def check_text(text):
        if text:
            return 'ok'
        else:
            return 'blank'




    """
        Other helpers
    """
    @staticmethod
    def update(comment_id, memorial_id, user_id, text):
        comment = Comment.query.filter_by(id=comment_id, memorial_id=memorial_id, user_id=user_id).first()
        if comment:
            comment.text = text
            db.session.commit()
            return True

        return False

    @staticmethod
    def get_comments(memorial_id):
        #from sqlalchemy import desc
        #comments = Comment.query.filter_by(memorial_id=memorial_id, parent_id=0).order_by(desc(Comment.likes-Comment.dislikes).all()
        comments = Comment.query.filter_by(memorial_id=memorial_id, parent_id=0).all()
        if comments:
            for comment in comments:
                comment.replies = Comment.query.filter_by(memorial_id=memorial_id, parent_id=comment.id).all()

        return comments
