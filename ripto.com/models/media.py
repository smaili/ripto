# RIP
from models import db


class Media(db.Model):
    # Table
    __tablename__ = 'media'
    # Types
    media_types = {
        'photo': 1, # Buried
        'video': 2 # Cremated
    }
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    memorial_id = db.Column(db.Integer)
    media_type = db.Column(db.Integer)
    filename = db.Column(db.Text)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, memorial_id=0, media_type='', filename=''):
        self.memorial_id = memorial_id
        self.media_type = media_type
        self.filename = filename
        # Validate Fields
        self.errors = { 'media_type':'', 'filename':'' }


    """
        Custom methods
    """
    def validate(self):
        # TODO - sanitize all text inputs
        # TODO - make sure file size/length/type is all correct

        # validate each field depending on what the current step it is
        isValid = True
        for field in self.errors:
            methodToCall = getattr(self, 'check_' + field)
            self.errors[field] = methodToCall(getattr(self, field))
            if self.errors[field] != 'ok':
                isValid = False

        return isValid


    def save_new_media(self):
        db.session.add(self)
        db.session.commit()


    def update_filename(self, filename):
        self.filename = filename
        db.session.commit()



    """
        Validator helpers
    """
    @staticmethod
    def check_media_type(media_type):
        if media_type:
            for a_type in Media.media_types:
                if Media.media_types[a_type] == media_type:
                    return 'ok'
            return 'invalid'
        else:
            return 'blank'

    @staticmethod
    def check_filename(filename):
        if filename:
            import os
            from config import ALLOWED_EXTENSIONS
            ext = os.path.splitext(filename)[1].replace('.', '').lower()
            if ext in ALLOWED_EXTENSIONS:
                return 'ok'
            else:
                return 'invalid'
        else:
            return 'blank'


    """
        Other helpers
    """
    @staticmethod
    def get_from_file(the_file, the_type):
        media = Media()
        if the_file:
            media.media_type = Media.media_types[the_type]
            media.filename = the_file.filename
        return media


    @staticmethod
    def get_media(memorial_id, init=True, validate=True):
        media = Media.query.filter_by(memorial_id=memorial_id).first() # first() for now since each memorial will have just one picture
        if media and init:
            media.errors = { 'media_type':'', 'filename':'' }
            if validate:
                media.validate()
        
        return media
