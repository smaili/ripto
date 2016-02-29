# -*- coding: utf-8 -*-




#----------------------------------------
# Domain
#----------------------------------------
SERVER_NAME = 'ripto.com'



#----------------------------------------
# App
#----------------------------------------
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

APP_MODES = lambda:0
APP_MODES.PRODUCTION = ''
APP_MODES.STAGING = 'stag'
APP_MODES.DEVELOPMENT = 'dev'
APP_MODE = APP_MODES.DEVELOPMENT # APP_MODES.PRODUCTION



#----------------------------------------
# Assets
#----------------------------------------
ASSETS_ROOT = '/srv/www/rtimg.com/'
ASSETS_SITE = 'rtimg.com'
ASSETS_CDN = '' # subdomain/dot may be required

if APP_MODE == APP_MODES.DEVELOPMENT:
    ASSETS_ROOT = '/Users/michael/Desktop/www/rtimg.com/'
    ASSETS_SITE = 'rtimg.com'
    ASSETS_CDN = ''

ASSETS_URL = ASSETS_CDN + ASSETS_SITE



#----------------------------------------
# Logging
#----------------------------------------
import logging
PROPAGATE_EXCEPTIONS = True
LOG_LEVEL = logging.DEBUG
LOG_FILE = '/var/log/uwsgi/ripto.com.log'

if APP_MODE == APP_MODES.DEVELOPMENT:
    LOG_FILE = '/usr/local/var/log/uwsgi/ripto.com.log'



#----------------------------------------
# Session
#----------------------------------------
SECRET_KEY = ''
SESSION_DIR = APP_ROOT + '/tmp/sessions'

if APP_MODE == APP_MODES.DEVELOPMENT:
    SESSION_DIR = '/Users/michael/Desktop/www/ripto.com/tmp/sessions'



#----------------------------------------
# DB
#----------------------------------------
# multiple db's -> http://stackoverflow.com/questions/15021292/
db_host = 'localhost'
db_user = 'root'
db_pass = ''
db_name = 'rt'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % ( db_user, db_pass, db_host, db_name )



#----------------------------------------
# Babel
#----------------------------------------
# Examples   -> facebook, twitter, youtube
# Directions -> i18nguy.com/temp/rtl.html
# Biggest    -> en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users
LANGUAGES = [

#    lang           display        direction    enabled
(   'id',       'Bahasa Indonesia',     'ltr',       True    ),       # Indonesian
(   'ms',       'Bahasa Melayu',        'ltr',       True    ),       # Malaysian
(   'de',       'Deutsch',              'ltr',       True    ),       # German
(   'en',       'English (US)',         'ltr',       True    ),       # English USA
(   'en_gb',    'English (UK)',         'ltr',       True    ),       # English UK
(   'es',       'Español',              'ltr',       True    ),       # Spanish
(   'fil',      'Filipino',             'ltr',       True    ),       # Filipino
(   'fr',       'Français',             'ltr',       True    ),       # French
(   'it',       'Italiano',             'ltr',       True    ),       # Italian
(   'pt',       'Português',            'ltr',       True    ),       # Portuguese
(   'pt_br',    'Português (Brasil)',   'ltr',       True    ),       # Portuguese - Brazil
(   'ru',       'Русский',              'ltr',       True    ),       # Russian
(   'vi',       'Tiếng Việt',           'ltr',       True    ),       # Vietnamese
(   'he',       'עִבְרִית',                'rtl',       False   ),       # Hebrew
(   'ar',       'العربية',              'rtl',       False   ),       # Arabic
(   'fa',       'فارسی',                'rtl',       False   ),       # Farsi
(   'hi',       'हिन्दी',                  'ltr',       False   ),       # Hindi
(   'th',       'ภาษาไทย',              'ltr',       False   ),       # Thai
(   'zh_cn',    '简体中文',             'ltr',       True    ),       # Simplified Chinese - China
(   'zh_tw',    '繁體中文',             'ltr',       True    ),       # Traditional Chinese - Taiwan
(   'zh_hk',    '香港中文',             'ltr',       True    ),       # Traditional Chinese - Hong Kong
(   'ja',       '日本語',               'ltr',       True    ),       # Japanese
(   'ko',       '한국어',               'ltr',       True    ),       # Korean

]
BABEL_DEFAULT_LOCALE = 'en' # Locale to use if no locale selector is registered
BABEL_DEFAULT_TIMEZONE = 'UTC' # timezone to use for user facing dates



#----------------------------------------
# Email
#----------------------------------------
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_TIMEOUT = 1
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_SENDERS = {
#    'NOREPLY' : ('RIPto', 'no-reply@ripto.com')
    'NOREPLY' : '"RIPto" <no-reply@ripto.com>'
}
MAIL_HTML = {
    'contact_email' : 'email/contact_email.pyhtml',
    'invite_email' : 'email/invite_email.pyhtml',
    'share_email' : 'email/share_email.pyhtml',
    'reset_email' : 'email/reset_email.pyhtml',
    'deactivate_email' : 'email/deactivate_email.pyhtml',
    'confirm_email' : 'email/confirm_email.pyhtml'
}
MAIL_TEXT = {
    'contact_email' : 'email/contact_email.pytxt',
    'invite_email' : 'email/invite_email.pytxt',
    'share_email' : 'email/share_email.pytxt',
    'reset_email' : 'email/reset_email.pytxt',
    'deactivate_email' : 'email/deactivate_email.pytxt',
    'confirm_email' : 'email/confirm_email.pytxt'
}
MAIL_DEBUG = True
MAIL_MAX_EMAILS = 0



#----------------------------------------
# Uploading
#----------------------------------------
UPLOAD_FOLDER = ASSETS_ROOT + '/tmp'
MEDIA_FOLDER = ASSETS_ROOT + '/memorial'
MEDIA_EXTENSION = 'jpg'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
MAX_CONTENT_LENGTH = 10 * 1024 * 1024 # 10MBs ( same as nginx)
MEDIA_WIDTH = 640
MEDIA_HEIGHT = 480



#----------------------------------------
# Searching
#----------------------------------------
RESULTS_COUNT = 20



#----------------------------------------
# Views
#----------------------------------------
PAGES = {
    'admin':          'layouts/default.pyhtml',
    'index':          'layouts/default.pyhtml',
    'home':           'layouts/default.pyhtml',
    'new_memorial':   'layouts/default.pyhtml',
    'memorial':       'layouts/memorial.pyhtml',
    'edit_memorial':  'layouts/default.pyhtml',
    'results':        'layouts/default.pyhtml',
    'user':           'layouts/default.pyhtml',
    'settings':       'layouts/default.pyhtml',
    'login':          'layouts/default.pyhtml',
    'signup':         'layouts/default.pyhtml',
    'forgot':         'layouts/default.pyhtml',
    'reset':          'layouts/default.pyhtml',
    'confirm':        'layouts/default.pyhtml',
    'lang':           'layouts/default.pyhtml',
    'footer':         'layouts/default.pyhtml',
    'translate':      'layouts/default.pyhtml',
    'wechat':         'layouts/default.pyhtml',
    'error':          'layouts/error.pyhtml',
    'mobile':         ''
}



#----------------------------------------
# CSS
#----------------------------------------
PAGES_CSS = {
    'admin':          [ 'base', 'default', 'form', 'calendar', 'admin' ],
    'index':          [ 'base', 'default', 'form', 'index' ],
    'home':           [ 'base', 'default', 'form', 'home' ],
    'memorial':       [ 'base', 'default', 'form', 'share', 'memorial' ],
    'edit_memorial':  [ 'base', 'default', 'form', 'calendar', 'edit_new_memorial', 'edit_memorial' ],
    'new_memorial':   [ 'base', 'default', 'form', 'calendar', 'edit_new_memorial', 'new_memorial' ],
    'results':        [ 'base', 'default', 'form', 'results' ],
    'user':           [ 'base', 'default', 'form', 'user' ],
    'settings':       [ 'base', 'default', 'form', 'settings' ],
    'login':          [ 'base', 'default', 'form', 'welcome' ],
    'signup':         [ 'base', 'default', 'form', 'welcome' ],
    'forgot':         [ 'base', 'default', 'form', 'welcome' ],
    'reset':          [ 'base', 'default', 'form', 'reset' ],
    'confirm':        [ 'base', 'default', 'form', 'confirm' ],
    'lang':           [ 'base', 'default', 'form', 'lang' ],
    'footer':         [ 'base', 'default', 'form', 'footer' ],
    'translate':      [ 'base', 'default', 'form', 'translate' ],
    'wechat':         [ 'base', 'default', 'form', 'wechat' ],
    'error':          [ 'base', 'default', 'form', 'error' ],
    'mobile':         [ 'mobile' ]
}



#----------------------------------------
# JS
#----------------------------------------
PAGES_JS = {
    'admin':          [ 'rt', 'form', 'notice', 'modal', 'calendar', 'admin' ],
    'index':          [ 'rt', 'ajax', 'memorials', 'index' ],
    'home':           [ 'rt', 'home' ],
    'memorial':       [ 'rt', 'ajax', 'form', 'notice', 'modal', 'memorial' ],
    'edit_memorial':  [ 'rt', 'ajax', 'form', 'notice', 'modal', 'calendar', 'edit_new_memorial' ],
    'new_memorial':   [ 'rt', 'ajax', 'form', 'notice', 'modal', 'calendar', 'edit_new_memorial' ],
    'results':        [ 'rt', 'ajax', 'memorials', 'results' ],
    'user':           [ 'rt' ],
    'settings':       [ 'rt', 'form', 'notice' ],
    'login':          [ 'rt', 'notice' ],
    'signup':         [ 'rt', 'ajax', 'form', 'notice', 'signup' ],
    'forgot':         [ 'rt', 'notice' ],
    'reset':          [ 'rt', 'notice' ],
    'confirm':        [],
    'lang':           [ 'rt', 'notice' ],
    'footer':         [ 'rt', 'form', 'notice' ],
    'translate':      [ 'rt', 'notice' ],
    'wechat':         [ 'rt' ],
    'error':          []
}



#----------------------------------------
# Sharing
#----------------------------------------
SHARE_SERVICES = {
    'default': [
        {
            'name': 'fk',
            'title': 'Facebook'
        },
        {
            'name': 'tr',
            'title': 'Twitter'
        },
        {
            'name': 'rd',
            'title': 'Reddit'
        },
        {
            'name': 'ge',
            'title': 'Google+'
        }
    ],
    'CN': [
        {
            'name': 'wechat',
            'title': '微信'
        },
        {
            'name': 'weibo',
            'title': '新浪微博'
        },
        {
            'name': 'qq',
            'title': 'QQ好友'
        },
        {
            'name': 'qqweibo',
            'title': '腾讯微博'
        }
    ]
}



#----------------------------------------
# GeoIP
#----------------------------------------
GEO_SERVICES = [
    'http://freegeoip.net/json/%s',
    'http://ipinfo.io/%s/json',
    'http://ip-api.com/json/%s',
    'https://www.dailycred.com/api/local.json?ip=%s'
]