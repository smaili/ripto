# System
import urllib2

# Flask
from sqlalchemy import and_, desc

# RIP
from config import SHARE_SERVICES
from lib import jinjer, geo


request = None



def init():
    pass


def get_services():
    # TODO - figure out fallbacks
    try:
        country = SHARE_SERVICES[ geo.country_code() ]
    except:
        country = SHARE_SERVICES['default']

    return country


def memorial(service, memorial):
    share_url = jinjer.memorial_url(memorial, _short=True)
    share_title = jinjer.memorial_share_title(memorial)
    share_desc = jinjer.memorial_share_desc(memorial)

    if service == 'fk':
        url = 'http://www.facebook.com/sharer.php?'
        uri = [
            ('u', share_url),
            ('t', share_title)
        ]

    elif service == 'tr':
        url = 'https://twitter.com/intent/tweet?'
        uri = [
            ('url', share_url),
            ('text', share_title)
        ]

    elif service == 'rd':
        url = 'http://reddit.com/submit?'
        uri = [
            ('url', share_url),
            ('title', share_title)
        ]

    elif service == 'ge':
        url = 'https://plus.google.com/share?'
        uri = [
            ('url', share_url),
            ('hl', 'en')
        ]

    # https://github.com/JimmyBryant/Instreet_plugin/blob/master/meiding.html
    elif service == 'wechat':
        url = jinjer.url_for('wechat', _external=True) + '?'
        uri = [
            ('url', share_url),
            ('title', share_title)
        ]

    elif service == 'weibo':
        url = 'http://v.t.sina.com.cn/share/share.php?'
        uri = [
            ('url', share_url),
            ('title', share_title),
            ('pic', jinjer.static(memorial.media.filename, 'memorial'))
        ]

    elif service == 'qq':
        url = 'http://connect.qq.com/widget/shareqq/index.html?'
        uri = [
            ('url', share_url),
            ('title', share_title),
            ('desc', share_desc),
            ('pics', jinjer.static(memorial.media.filename, 'memorial')), # e.g., http://g2.ykimg.com/0100641F46521CAEC101220881BA8B7EA14ABC-0CBA-61F8-DFFF-D4F0CEADD26F
            ('site', 'RIPto')
        ]

    elif service == 'qqweibo':
        url = 'http://v.t.qq.com/share/share.php?'
        uri = [
            ('url', share_url),
            ('title', share_title),
            ('pic', jinjer.static(memorial.media.filename, 'memorial')),
            #('appkey', 'e7ad0b0199994bda85ecc0a44ce9915f'),
            ('site', 'ripto.com'),
            ('assname', 'RIPto')
        ]

    else:
        url = ''
        uri = []


    for i, (param, val) in enumerate(uri):
        url = url + param + '=' + _encode(val) + ('&amp;' if i < len(uri) - 1 else '')

    return url


def _encode(s):
    return urllib2.quote( jinjer.encode( s ), '' )
