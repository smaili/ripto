# System
import os

# Flask
from flask import g, request

# RIP
from config import APP_ROOT, LANGUAGES, BABEL_DEFAULT_LOCALE
from lib import sessions


# http://pythonhosted.org/Flask-Babel/
# http://stackoverflow.com/questions/11955506/python-flask-babel-message-and-e-g-spanish-how-to
# http://www.meirkriheli.com/talks/django-i18n/django-i18n.html
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n
# http://hg.flowblok.id.au/enscribe/src/3e89de1d94a386c5e20165e20dd3e94b5e0fb6b1/enscribe/helpers/babel_integration.py


locale = None



"""
Value used for <html lang="">
"""
def get_html_lang():
    return locale.split('_')[0]



"""
Returns ltr or rtl
"""
def get_dir():
    for (lang, display, ldir, enabled) in LANGUAGES:
        if lang == locale:
            return ldir

    return ''



"""
Gets display name of current language
"""
def get_name():
    curr = locale
    for (lang, display, ldir, enabled)  in LANGUAGES:
        if lang == curr:
            return display


def is_avail(l):
    for (lang, display, ldir, enabled)  in LANGUAGES:
        if lang == l and enabled:
            return True
    return False

"""
Update lang in session
"""
def set_locale(lang):
    # TODO - add logic to saving lang in DB (if user is not anonymous)
    sessions.lang('set', lang)



"""
Get the appropriate locale
"""
def get_locale():
    subdomain = request.host[:request.host.index('ripto.com')].split('.')[0].replace('-','_')
    if (subdomain):
        return subdomain
    elif sessions.lang('has'):
        return sessions.lang('get')

    # convert our array of tuples to just an array of lang codes
    langs = [(lang if enabled else '') for (lang,display,ldir,enabled) in LANGUAGES]
    return request.accept_languages.best_match(langs) or BABEL_DEFAULT_LOCALE



"""
Get the appropriate timezone
"""
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


# http://polib.readthedocs.org/en/latest/
def get_po_data(lang, filename):
    from lib import polib

    lang = ''.join( [ c if i < 3 else c.upper() for i,c in enumerate(lang) ] ) # e.g., zh_cn -> zh_CN
    lang_file = APP_ROOT + '/translations/' + lang + '/LC_MESSAGES/' + filename
    if os.path.exists(lang_file):
        return polib.pofile(lang_file)
    
    return []
