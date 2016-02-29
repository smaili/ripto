# System
import re

# Flask
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import exists

# RIP
from models import db


class User(db.Model):
    # Table
    __tablename__ = 'users'
    # Types
    status_types = {
        'registered': 1,
        'active': 2,
        'deactive': 3,
        'banned': 4,
        'admin': 5
    }
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)
    status = db.Column(db.Integer, default=status_types['active'])
    created = db.Column(db.DateTime, default=db.func.now())
    modified = db.Column(db.DateTime)


    def __init__(self, name='', username='', password='', email=''):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        # fields to validate
        self.errors = { 'name' : '', 'username' : '', 'password' : '', 'email' : '' }



    """
        Flask-Login Overrides
    """
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)



    """
        Custom methods
    """
    def validate(self):
        # remove start/end spaces, tabs, newlines and carriage returns
        self.name = self.name.strip()
        self.email = self.email.strip()

        # validate each field
        isValid = True
        for field in self.errors:
            methodToCall = getattr(self, 'check_' + field)
            self.errors[field] = methodToCall(getattr(self, field))
            if self.errors[field] != 'ok':
                isValid = False

        return isValid


    def save_new_user(self):
        # hash password before saving new user to db
        self.password = User.gen_password(self.password)
        db.session.add(self)
        db.session.commit()


    def update(self, name, email, username, password):
        save = None
        valid = None
        if name != self.name or email != self.email or username != self.username or password:
            save = True
            valid = {}
            if name != self.name:
                valid['name'] = User.check_name(name)
                self.name = name
                if valid['name'] != 'ok':
                    save = False
            if email != self.email:
                valid['email'] = User.check_email(email)
                self.email = email
                if valid['email'] != 'ok':
                    save = False
            if username != self.username:
                valid['username'] = User.check_username(username)
                self.username = username
                if valid['username'] != 'ok':
                    save = False
            if password:
                valid['password'] = User.check_password(password)
                self.password = User.gen_password(password)
                if valid['password'] != 'ok':
                    save = False
        if save:
            db.session.commit()

        return save, valid


    def activate_user(self):
        self.status = User.status_types['active']
        db.session.commit()


    def change_password(self, new_password):
        self.password = User.gen_password(new_password)
        db.session.commit()


    def get_memorial_count(self):
        # TODO - figure out how to optimize this. very slow right now
        from models.memorial import Memorial
        count = Memorial.query.filter_by( user_id=self.id, status=3 ).count()
        return count

    def deactivate(self):
        self.status = User.status_types['deactive']
        db.session.commit()

    def isadmin(self):
        return not self.is_anonymous() and self.status == User.status_types['admin']




    """
        Validator helpers
    """
    @staticmethod
    def check_name(name):
        return 'ok'


    @staticmethod
    def check_username(username):
        if username:
            if re.match(r'([A-Za-z0-9_]+$)', username):
                if len(username) > 3 and not db.session.query(exists().where(User.username == username)).scalar():
                    return 'ok'
                else:
                    return 'taken'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_password(password):
        if password:
            if len(password) > 5:
                score = User._score_password(password)
                if score > 80:
                    return 'ok' # perfect
                elif score > 50:
                    return 'ok'
                elif score >=30:
                    return 'ok' # weak
                else:
                    return 'tooweak'
            else:
                return 'invalid'
        else:
            return 'blank'


    @staticmethod
    def check_email(email):
        if email:
            if re.match(r'[^@]+@[^@]+\.[^@]+', email):
                if not db.session.query(exists().where(User.email == email)).scalar():
                    return 'ok'
                else:
                    return 'taken'
            else:
                return 'invalid'
        else:
            return 'ok'


    @staticmethod
    def _score_password(word):
        score = 0
        if word:
            #award every unique letter until 5 repetitions
            letters = {}
            for letter in word:
                if letter in letters:
                    letters[letter] = letters[letter] + 1
                else:
                    letters[letter] = 1
                score = score + 5.0 / letters[letter];

            # bonus points for mixing it up
            variations = [
                re.match(r'\d', word), # digits
                re.match(r'[a-z]', word), # lower
                re.match(r'[A-Z]', word), # upper
                re.match(r'\W', word) # non words
            ]

            variationCount = 0
            for check in variations:
                if check:
                    variationCount = variationCount + 1

            score = score + (variationCount - 1) * 10;

        return int(score)



    """
        Other helpers
    """
    @staticmethod
    def gen_password(password):
        return generate_password_hash(password)


    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username) \
            .filter( (User.status == User.status_types['active']) | (User.status == User.status_types['admin']) ).first()
        if user:
            if check_password_hash(user.password, password):
                return user

        return None
