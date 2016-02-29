# System
from time import strptime
from datetime import datetime

# Flask
import flask
from flask.ext.babel import format_date, gettext

# RIP
from models import db

class Memorial(db.Model):
    # Table
    __tablename__ = 'memorials'
    # Types
    funeral_types = {
        '1': 1, # Buried
        '2': 2, # Cremated
        '3': 3  # Don't know
    }
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    dob = db.Column(db.DateTime)
    dod = db.Column(db.DateTime)
    cause = db.Column(db.Integer)
    epitaph = db.Column(db.Text)
    funeral_type = db.Column(db.Integer)
    funeral_date = db.Column(db.DateTime)
    funeral_loc = db.Column(db.Text)
    url = db.Column(db.Text)
    condolences = db.Column(db.Integer)
    remembers = db.Column(db.Integer)
    views = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)



    def __init__(self, user_id, name='', dob=0, dod=0, cause=1, epitaph='', funeral_type=1, funeral_date=0, funeral_loc='', url='', condolences=0, remembers=0, views=0, status=0):
        self.user_id = user_id
        self.name = name
        self.dob = dob
        self.dod = dod
        self.cause = cause
        self.epitaph = epitaph
        self.funeral_type = funeral_type
        self.funeral_date = funeral_date
        self.funeral_loc = funeral_loc
        self.url = url
        self.condolences = condolences
        self.remembers = remembers
        self.views = views
        self.status = status


    """
        Custom methods
    """
    def validate(self):
        # TODO - sanitize all text inputs
        isValid = True
        for field in self.errors:
            methodName = 'check_' + field
            methodToCall = getattr(self, 'check_' + field)
            self.errors[field] = methodToCall(self)
            if self.errors[field] != 'ok':
                isValid = False

        return isValid


    def save_new_memorial(self):
        db.session.add(self)
        db.session.commit()


    def update(self):
        if hasattr(self.media, 'filename_old'):
            from lib import uploader
            uploader.remove_memorial_photo( self.media.filename_old )

        if not self.media.id:
            db.session.add(self.media)

        if not self.media.memorial_id:
            self.media.memorial_id = self.id

        if not self.url:
            from lib import helper
            self.url = helper.gen_url(self.id)

        if self.status == 1: #i.e., it's a new memorial
            self.status = 2
            from lib import uploader
            uploader.move_memorial_media(self.media)

        db.session.commit()



    def get_error(self, field='', exclude=''):
        if field:
            # assume empty means we have yet to validate so for that we'll just return ok
            return self.errors[field] if ( self.errors and field in self.errors and self.errors[field] ) else 'ok'
        else:
            for e in self.errors:
                if self.errors[e] and e != exclude:
                    return e
            return 'ok'



    def get_date(self, field):
        date = getattr(self, field)
        try:
            return date.strftime('%m/%d/%Y') # month/day/year
        except:
            return ''


    def set_date(self, date):
        try:
            date = datetime.strptime(date, '%m/%d/%Y') # http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        except:
            date = False

        return date


    def print_date(self, field):
        date = getattr(self, field)
        try:
            return format_date(date, 'MMM d, yyyy') # http://babel.edgewall.org/wiki/Documentation/0.9/dates.html
        except:
            return ''


    def condolence_count(self):
        # Count = comments plus replies
        count = len( self.comments )
        for comment in self.comments:
            count = count + len( comment.replies )

        return count



    """
        Validator helpers
    """
    @staticmethod
    def check_name(memorial):
        if memorial.name:
            return 'ok'
        else:
            return 'blank'


    @staticmethod
    def check_dob(memorial):
        if memorial.dob:
            memorial.dob = memorial.set_date( memorial.dob )
            if memorial.dob:
                return 'ok'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_dod(memorial):
        if memorial.dod:
            memorial.dod = memorial.set_date( memorial.dod )
            if memorial.dod:
                if not memorial.dob or (memorial.dob and memorial.dod >= memorial.dob):
                    return 'ok'
                else:
                    return 'invalid'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_cause(memorial):
        if memorial.cause:
            if memorial.cause in Memorial.cause_types():
                return 'ok'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_epitaph(memorial):
        if memorial.epitaph:
            return 'ok'
        else:
            return 'blank'


    @staticmethod
    def check_funeral_type(memorial):
        if memorial.funeral_type:
            if str(memorial.funeral_type) in Memorial.funeral_types:
                return 'ok'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_funeral_date(memorial):
        if memorial.funeral_type == 3:
            return 'ok'
        elif memorial.funeral_date:
            memorial.funeral_date = memorial.set_date( memorial.funeral_date )
            if memorial.funeral_date:
                if not memorial.dod or (memorial.dod and memorial.funeral_date >= memorial.dod):
                    return 'ok'
                else:
                    return 'invalid'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_funeral_loc(memorial):
        if memorial.funeral_loc:
            return 'ok'
        elif memorial.funeral_type == 3:
            return 'ok'
        else:
            return 'blank'


    @staticmethod
    def check_media(memorial):
        if memorial.media:
            if memorial.media.validate():
                return 'ok'
            else:
                return memorial.media.errors['filename']
        else:
            return 'blank'



    """
        Other helpers
    """
    @staticmethod
    def get_memorial(url=None, user_id=None, create_if_none=True, init=False):
        from models.media import Media
        from models.comment import Comment

        memorial = None

        if url:
            # TODO - figure out how to condense into just a single db query.  Either we have to build the Memorial obj from the tuple returned from exec, or research more on case sensitive searching using SQLAlchemy
            # https://bitbucket.org/mitsuhiko/flask/src/tip/examples/minitwit/minitwit.py --> db_query()
            memorial = db.session.execute('SELECT id FROM memorials WHERE BINARY memorials.url = :url and memorials.status < 5 LIMIT 1', { 'url': url } ).fetchone()

            if memorial:
                memorial = Memorial.query.filter_by(id=memorial[0]).first()
                memorial.media = Media.get_media(memorial.id, init=init, validate=False)
                memorial.comments = Comment.get_comments(memorial.id)
        else:
            if user_id > 0:
                memorial = Memorial.query.filter(Memorial.user_id == user_id, Memorial.status == 1).first()
                if memorial:
                    memorial.media = Media.get_media(memorial.id, init=True, validate=False)

                elif create_if_none:
                    memorial = Memorial(user_id, status=1)
                    memorial.save_new_memorial()
            else:
                from lib import sessions
                memorial = Memorial(user_id, status=1)
                if sessions.save_photo('has'):
                    memorial.media = Media(media_type=Media.media_types['photo'], filename=sessions.save_photo('get'))

        if memorial:
            # Need ordered to ensure validation goes through date checking in order
            from collections import OrderedDict
            memorial.errors = OrderedDict([ ('name', ''), ('dob', ''), ('dod', ''), ('cause', ''), ('epitaph', ''), ('funeral_type', ''), ('funeral_date', ''), ('funeral_loc', ''), ('media', '') ])
            memorial.media = ( memorial.media if hasattr(memorial, 'media') and memorial.media else None ) #media = db.relationship('Media', backref = 'memorial', lazy = 'dynamic')


        return memorial



    @staticmethod
    def update_memorial(request, memorial):
        memorial.name = request.form.get('name') or ''
        memorial.dob = request.form.get('dob') or ''
        memorial.dod = request.form.get('dod') or ''
        memorial.cause = request.form.get('cause', type=int) or 1
        memorial.epitaph = request.form.get('epitaph') or ''
        memorial.funeral_type = request.form.get('ftype', type=int) or 1
        memorial.funeral_date = 0 if memorial.funeral_type == 3 else request.form.get('fdate') or ''
        memorial.funeral_loc = '' if memorial.funeral_type == 3 else request.form.get('floc') or ''

        if request.form.get('nophoto', type=int) == 1:
            if memorial.media and memorial.media.filename != 'nophoto.png':
                memorial.media.filename_old = memorial.media.filename
                memorial.media.filename = 'nophoto.png'
            else:
                from models.media import Media
                memorial.media = Media(memorial.id, Media.media_types['photo'], 'nophoto.png')

        return memorial


    @staticmethod
    def cause_types():
        return {
            1: gettext('Natural'),
            2: gettext('Accidental'),
            3: gettext('Homicide'),
            4: gettext('Suicide'),
            5: gettext('War')
        }

    @staticmethod
    def status_types():
        return {
            1: 'New',
            2: 'Just Created',
            3: 'Active',
            4: 'Private',
            5: 'Deactive',
            6: 'Banned'
        }
