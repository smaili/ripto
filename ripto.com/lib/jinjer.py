# System
import types
import urllib
from urlparse import urlparse

# Flask
import flask
from flask.ext.babel import format_datetime, format_number

# RIP
from config import ASSETS_URL


app = None
request = None


def init():
    from lib import jinjer
    app.jinja_env.globals.update(jinjer=jinjer)



def static(filename, folder, _scheme=None):
    scheme = _scheme or urlparse(request.url_root).scheme or 'http'

    return '%s://%s/%s/%s' % ( scheme, ASSETS_URL, folder, filename )



def url_for(endpoint, **values):
    # TODO - merge this with static and memorial_url functions

    chars = {
        '~': '%7E'
    }

    # pop all custom values
    _safe = values.pop('_safe', None)
    _next = values.pop('_next', None)
    _show = values.pop('_show', None)
    _short = values.pop('_short', None)
    _external = values.get('_external', None)
    _scheme = values.pop('_scheme', None) or urlparse(request.url_root).scheme # either we use the scheme given or we default to whatever is the current scheme being used by the user

    # pre-flask
    if _next and request.path != '/':
        if _next is True: # i.e., use the current path as the next
            values['next'] = request.path[1:] # remove first char since escaped '/' looks messy
        else:
            values['next'] = _next
        _args = values.pop('_args', None)
        if _args:
            values['next'] = values['next'] + ( '?' + urllib.urlencode(request.args or request.form) if len(request.args or request.form) > 0 else '' )
    if _show:
        values['show'] = 1
    if 'next' in values and not values['next']:
        values.pop('next', None)

    # flask
    url = flask.url_for(endpoint, **values)

    # post-flask
    if _safe:
        url = url.replace(chars[_safe], _safe, 1) # replace first occurence
    if _external:
        url = '%s://%s' % ( _scheme, url[7:] ) # substring out the first 7 chars ( http:// ) that flask.url_for generated
    if _short:
        if _external:
            url = url.replace('ripto.com', 'rip.to', 1)
        else:
            url = '%s://rip.to%s' % ( _scheme, url )

    return url



def element(element, **args):
    return flask.render_template( 'elements/' + element + '.pyhtml', **args )



def memorial_url(memorial, action=None, _short=False, _external=False):
    if _short:
        return 'http://rip.to/' + memorial.url
    else:
        return url_for('memorial', memorial_url=memorial.url, action=action, _safe='~', _external=_external)


def memorial_share_title(memorial):
    return "~ %s ~" % memorial.name


def memorial_share_desc(memorial):
    return memorial.epitaph


def escape_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;").replace("\"", "&quot;")


def tabindex():
    flask.g.tabcount = ( flask.g.tabcount if hasattr(flask.g, 'tabcount') else 0 ) + 1
    return flask.g.tabcount


def display(obj, _type):
    text = ''

    if _type == 'textarea':
        r = '&#13;&#10;'
        text = obj.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)

    return text

def preview(obj, _type):
    text = ''

    if _type == 'epitaph':
        text = obj
        if len(text) > 20:
            text = text[0:20] + '<strong>...</strong>'

    return text


def encode(s):
    return s.encode('utf8')


def decode(s):
    return s.decode('utf8')


def format_num(num):
    return format_number(num)


def human_time(datetime):
    # TODO - add localization
    # http://flask.pocoo.org/snippets/33/
    now = datetime.utcnow()
    diff = now - datetime
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for i, (period, singular, plural) in enumerate(periods):
        if period and i > 3: #i.e., less than a day ago
            return "%d %s ago" % (period, singular if period == 1 else plural)
        elif period:
            # http://babel.edgewall.org/wiki/Documentation/0.9/dates.html
            #return format_datetime(datetime, "MMMM d 'at' h:mma")
            if diff.days == 1:
                return "yesterday"
            elif datetime.year - now.year:
                return format_datetime(datetime, "MMMM d, YYYY")
            else:
                return format_datetime(datetime, "MMMM d")

    return "now"
