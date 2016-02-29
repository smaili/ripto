# Flask
from flask import Flask, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import uwsgi



#----------------------------------------
# App
#----------------------------------------
app = Flask(__name__)
app.config.from_object('config')

app.url_map.strict_slashes = False



#----------------------------------------
# DB
#----------------------------------------
db = SQLAlchemy()
db.init_app(app)



#----------------------------------------
# Views
#----------------------------------------
@app.route('/')
@app.route('/<memorial>', methods = ['GET', 'POST'])
def index(memorial=None):
    uri = ''
    if memorial:
        found = db.session.execute('SELECT id FROM memorials WHERE BINARY memorials.url = :url LIMIT 1', { 'url': memorial } ).fetchone()
        if found:
            uri = '/~' + memorial


    scheme = uwsgi.env['wsgi.url_scheme']
    return redirect( "%s://ripto.com%s" % (scheme, uri) )
