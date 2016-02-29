# System
import glob, os, subprocess

# Flask
from flask import Flask, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename


#----------------------------------------
# App
#----------------------------------------
# TODO - phase out `static` folder
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
@app.before_request
def before_request():
    username = request.form.get('u') or ''
    password = request.form.get('p') or ''
    if username != app.config['APP_USERNAME'] or password != app.config['APP_PASSWORD']:
        return redirect('http://ripto.com')



@app.route('/c', methods = ['POST'])
def c():
    # get pages and files
    results = db.session.execute( 'SELECT page,css,js FROM rtimg').fetchall()
    pages = []
    for (page,css,js) in results:
        pages.extend(( 'css/' + page + str(css) + '.css', 'js/' + page + str(js) + '.js' ))
    files = glob.glob( 'css/*' ) + glob.glob( 'js/*' )

    # iterate over files and delete those not currently in use
    for f in files:
        if f not in pages:
            try:
                subprocess.call(['rm', '-fr', f ])
            except:
                pass
    return ''


@app.route('/f', methods = ['POST'])
def f():
    f = request.files.get('f') or ''
    if f:
        # get info
        filename = os.path.basename( f.filename )
        page = os.path.splitext(filename)[0]
        file_type = os.path.splitext(filename)[1][1:]

        # update db
        db.session.execute( 'UPDATE rtimg set ' + file_type + ' = ' + file_type + ' + 1 WHERE page = :page', { 'page': page } )
        db.session.commit()

        # save file
        version = db.session.execute( 'SELECT ' + file_type + ' FROM rtimg WHERE page = :page', { 'page': page } ).scalar()
        save_dir = app.config['APP_ROOT'] + '/' + file_type
        save_name = page + str( version ) + '.' + file_type
        f.save( os.path.join( save_dir, save_name ) )
        return ''
