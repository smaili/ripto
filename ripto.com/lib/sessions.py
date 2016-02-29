# Flask
from flask import session

# RIP
from config import APP_MODE, APP_MODES, SESSION_DIR


app = None


def init():
    from flask.ext.kvsession import KVSessionExtension
    from simplekv.fs import FilesystemStore
    store = FilesystemStore(SESSION_DIR)
    KVSessionExtension(store, app)


def lang(action, value=''):
    if action == 'has':
        return _has('lang')
    elif action == 'get':
        return _get('lang')
    elif action == 'set':
        _set('lang', value)
    elif action == 'del':
        _del('lang')


def new_memorial(action, value=''):
    if action == 'has':
        return _has('new_memorial')
    elif action == 'get':
        return _get('new_memorial')
    elif action == 'set':
        _set('new_memorial', value)
    elif action == 'del':
        _del('new_memorial')


def save_photo(action, value=''):
    if action == 'has':
        return _has('save_photo')
    elif action == 'get':
        return _get('save_photo')
    elif action == 'set':
        _set('save_photo', value)
    elif action == 'del':
        _del('save_photo')


def comment(action, value=''):
    if action == 'has':
        return _has('comment')
    elif action == 'get':
        return _get('comment')
    elif action == 'set':
        _set('comment', value)
    elif action == 'del':
        _del('comment')


def reset_password(action, value=''):
    if action == 'has':
        return _has('reset_password')
    elif action == 'get':
        return _get('reset_password')
    elif action == 'set':
        _set('reset_password', value)
    elif action == 'del':
        _del('reset_password')


def logout():
    session.destroy()



"""
Helpers
"""

def _has(key):
    return key in session

def _get(key):
    return session[key]

def _set(key, value):
    session[key] = value

def _del(key):
    del session[key]

# http://stackoverflow.com/questions/16694006/why-does-flask-security-cause-a-new-kvsession-record-for-each-request
# http://blog.startuptale.com/2012/10/security-flask-cookie-based-session.html
