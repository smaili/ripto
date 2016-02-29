# Flask
from flask import Flask, abort, render_template, request, redirect, url_for, g
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, gettext

# RIPto
from lib import babler, geo, helper, jinjer, mailer, logger, searcher, sessions, sharer, tracker
from models import db
from models.user import User


#----------------------------------------
# App
#----------------------------------------
app = Flask(__name__, template_folder='templates')
app.config.from_object('config')

app.url_map.strict_slashes = False



#----------------------------------------
# Sessions
#----------------------------------------
sessions.app = app
sessions.init()



#----------------------------------------
# Logging
#----------------------------------------
logger.app = app
logger.init()

@app.errorhandler(Exception)
def catch_all(e):
    logger.exception()


#----------------------------------------
# Login Manager
#----------------------------------------
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
# http://www.vurt.ru/eng/2013/06/using-flask-and-rauth-for-github-authentication/
# http://net.tutsplus.com/tutorials/python-tutorials/intro-to-flask-signing-in-and-out/
# https://github.com/insynchq/flask-googlelogin
login_manager = LoginManager()
login_manager.init_app(app)


# callback used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# callback used for unauthorized users trying to access @login_required views
@login_manager.unauthorized_handler
def unauthorized():
    # endpoint gives the function name, so need to get route with url_for()
    url = jinjer.url_for( 'login', _next=True, _args=True, _show=True )
    if request.is_xhr:
        return render(ajax=True, status='login', message=url)
    else:
        return redirect(url)




#----------------------------------------
# DB / Models
#----------------------------------------
db.init_app(app)



#----------------------------------------
# Bable
#----------------------------------------
# TODO - https://github.com/mrjoes/flask-babelex/pull/1
babel = Babel(app)

@babel.localeselector
def get_locale():
    return babler.get_locale()
"""
@babel.timezoneselector
def get_timezone():
    return babler.get_timezone()
"""



#----------------------------------------
# Mail
#----------------------------------------
mailer.mail.init_app(app)
mailer.app = app



#----------------------------------------
# Jinja
#----------------------------------------
jinjer.app = app
jinjer.request = request
jinjer.init()



#----------------------------------------
# Geo
#----------------------------------------
geo.request = request
geo.init()



#----------------------------------------
# Sharer
#----------------------------------------
sharer.request = request
sharer.init()



#----------------------------------------
# Views
#----------------------------------------
@app.before_request
def before_request():
    g.user = current_user
    g.user.id = 0 if g.user.is_anonymous() else g.user.id
    g.babler = babler
    babler.locale = get_locale()
    g.sharer = sharer
    g.is_mobile = helper.is_mobile( request.user_agent.string )



@app.after_request
def after_request(response):
    logger.log_uwsgi(request, response)
    return response


def render(page='', ajax=False, status_code=200, **args):
    if ajax:
        if args['message'] == list:
            args['message'] = '[%s]' % ( ', '.join( ['"%s"' % s for s in args['message']] ) )
        else:
            args['message'] = '"%s"' % args['message']
        response = '{"s": "%s", "m": %s}' % ( args['status'], args['message'] )
    else:
        layout = app.config['PAGES'][page]
        if app.config['APP_MODE'] == app.config['APP_MODES'].PRODUCTION:
            css = [ page + str( db.session.execute( 'SELECT css FROM rtimg WHERE page = :page', { 'page': page } ).scalar() ) ]
            js = [ page + str( db.session.execute( 'SELECT js FROM rtimg WHERE page = :page', { 'page': page } ).scalar() ) ]
        else:
            css = app.config['PAGES_CSS'][page]
            js = app.config['PAGES_JS'][page]
        if g.is_mobile:
            if app.config['APP_MODE'] == app.config['APP_MODES'].PRODUCTION:
                css.append( 'mobile' + str( db.session.execute( 'SELECT css FROM rtimg WHERE page = :page', { 'page': 'mobile' } ).scalar() ) )
            else:
                css.append( 'mobile' )
        response = helper.minify(render_template(layout, css=css, js=js, page=page, **args))
    

    return response, status_code



@app.route('/')
@app.route('/', subdomain='<lang>')
def index(lang=None):
    filter_by = request.args.get('f', type=int) or request.form.get('f', type=int) or 0
    time_by = request.args.get('t', type=int) or request.form.get('t', type=int) or 0
    page_offset = request.args.get('p', type=int) or request.form.get('p', type=int) or 0

    results = searcher.most(filter_by, time_by, page_offset)

    if request.is_xhr:
        return helper.minify( jinjer.element('results', results=results) )
    else:
        return render(page='index', title='', results=results, filter_by=filter_by, time_by=time_by, page_offset=page_offset)




@app.route('/lang')
def lang():
    next_url = request.args.get('next') or ''
    lang = request.args.get('lang') or ''
    invalid = False

    if lang:
        if babler.is_avail(lang):
            babler.set_locale(lang)
            return redirect(next_url or url_for('index'))
        invalid=True

    return render(page='lang', title=gettext('Languages'), user=g.user, next_url=next_url, invalid=invalid)



@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    section = 'mine'
    results = searcher.created(g.user.id)

    return render(page='home', title=gettext('Home'), section=section, results=results, paging=False)



@app.route('/remembered', methods = ['GET', 'POST'])
@login_required
def remembered():
    section = 'remembered'
    results = searcher.remembered(g.user.id)

    return render(page='home', title=gettext('Home'), section=section, results=results, paging=False)




@app.route('/~', methods = ['GET', 'POST'])
def new_memorial():
    from models.memorial import Memorial

    memorial = Memorial.get_memorial( user_id=g.user.id )

    if request.method == 'POST':
        memorial = Memorial.update_memorial(request, memorial)
        if memorial.validate():
            if not memorial.id:
                memorial.save_new_memorial()
            memorial.update()
            if sessions.save_photo('has'):
                sessions.save_photo('del')
            return redirect( jinjer.memorial_url(memorial) )

    meta_desc = gettext('Remember someone by creating a new memorial and sharing it with your friends and family.')
    meta_words = gettext('RIPto, new memorial, new, create, remember')
    return render(page='new_memorial', title=gettext('New Memorial'), meta_desc=meta_desc, meta_words=meta_words, modals=['calendar'], preloaders=['calendar'], memorial=memorial)



@app.route('/~<memorial_url>')
@app.route('/~<memorial_url>/<action>', methods = ['GET', 'POST'])
def memorial(memorial_url=None, action=None):
    if memorial_url:
        from models.memorial import Memorial
        memorial = Memorial.get_memorial(url=memorial_url)
        if memorial:
            tracker.viewed_memorial(memorial)

            comment = None
            commented = False
            updated_comment = False
            if sessions.comment('has'):
                commented = sessions.comment('get')
                sessions.comment('del')


            if memorial.user_id == g.user.id and memorial.status == 2: # i.e., just created
                memorial.status = 3
                db.session.commit()
                memorial.is_new = True

            if action is None:
                pass

            elif action == 'comment':
                if g.user.is_anonymous():
                    return redirect( jinjer.url_for( 'login', _next=True, _args=True, _show=True ) )
                else:
                    from models.comment import Comment
                    text = request.form.get('comment') or request.args.get('comment') or ''
                    edit = request.form.get('e', type=int) or request.args.get('e', type=int) or 0
                    parent = request.form.get('p', type=int) or request.args.get('p', type=int) or 0

                    if edit:
                        updated_comment = Comment.update(edit, memorial.id, g.user.id, text)
                    else:
                        comment = Comment(text, parent)
                        if comment.validate():
                            comment.memorial_id = memorial.id
                            comment.user_id = g.user.id
                            comment.save_new_comment()
                            sessions.comment( 'set', 1 if not parent else 2 )
                            return redirect( jinjer.memorial_url(memorial) )

            elif action == 'share' and request.method == 'POST' and request.is_xhr:
                sharer = g.user.name or g.user.username or g.user.email or ''
                email = request.form.get('email') or ''
                message = request.form.get('message') or ''

                s = 'error'
                m = gettext('Invalid email address.')
                if email:
                    emails = email.split(',')
                    for e in emails:
                        mailer.share_memorial(e, sharer, memorial, message)
                    s = 'ok'
                    m = gettext('Memorial was successfully shared.')

                return render(ajax=True, status=s, message=m)

            elif action == 'remember':
                if g.user.is_anonymous():
                    s = 'login'
                    m = jinjer.url_for( 'login', _next=True, _args=True, _show=True )
                else:
                    tracker.remembered_memorial(memorial)
                    s = 'ok'
                    m = jinjer.format_num(memorial.remembers)

                if request.is_xhr:
                    return render(ajax=True, status=s, message=m)
                else:
                    return redirect( jinjer.memorial_url(memorial) )

            elif action == 'like':
                if g.user.is_anonymous():
                    s = 'login'
                    m = jinjer.url_for( 'login', _next=True, _args=True, _show=True )
                else:
                    from models.comment import Comment
                    comment_id = request.form.get('c', type=int) or request.args.get('c', type=int) or 0
                    action = request.form.get('a', type=int) or request.args.get('a', type=int) or 1

                    comment = Comment.query.filter_by(id=comment_id).first()
                    if comment:
                        tracker.liked_comment(comment, action)
                        if request.is_xhr:
                            return render(ajax=True, status='ok', message=[ jinjer.format_num(comment.likes), jinjer.format_num(comment.dislikes) ])
                    else:
                        s = 'error'
                        m = ''

                if request.is_xhr:
                    return render(ajax=True, status=s, message=m)
                else:
                    return redirect( jinjer.memorial_url(memorial) )

            elif action == 'edit' and not g.user.is_anonymous() and g.user.id == memorial.user_id:
                memorial = Memorial.get_memorial(url=memorial_url, init=True) # for now we're just reselecting and initing, till we can figure out a better/more efficient way of doing this
                if request.method == 'POST':
                    memorial = Memorial.update_memorial(request, memorial)
                    if memorial.validate():
                        memorial.update()
                        return redirect( jinjer.memorial_url(memorial) )

                return render(page='edit_memorial', title=memorial.name, modals=['calendar'], preloaders=['calendar'], memorial=memorial)

            # TODO - implement embedding
            elif action == 'embed':
                pass

            else:
                return redirect( jinjer.memorial_url(memorial) )

            return render(page='memorial', title=memorial.name, section=action, modals=['share', 'flag'], memorial=memorial, comments=memorial.comments, comment=comment, commented=commented, updated_comment=updated_comment, tracker=tracker)

    abort(404)



@app.route('/~/save_photo', methods = ['POST'])
@app.route('/~<memorial_url>/edit/save_photo', methods = ['POST'])
def save_photo(memorial_url=None):
    from lib import uploader
    from models.memorial import Memorial
    from models.media import Media

    photo = request.files.get('photo') or ''
    new_file = uploader.process_media( photo ) if photo else ''
    if photo and new_file:
        if g.user.is_anonymous():
            status = 'ok'
            message = jinjer.static( new_file, 'tmp' )
            # replace current photo in user's session with new one
            if sessions.save_photo('has'):
                uploader.remove_memorial_photo( sessions.save_photo('get') )
            sessions.save_photo('set', new_file)

        else:
            memorial = Memorial.get_memorial( url=memorial_url, user_id=g.user.id, create_if_none=False )
            if memorial:
                status = 'ok'
                # is this a new memorial?
                if memorial.status == 1:
                    message = jinjer.static( new_file, 'tmp' )
                else:
                    uploader.move_file( new_file, app.config['MEDIA_FOLDER'] )
                    message = jinjer.static( new_file, 'memorial' )

                media = Media.query.filter_by(memorial_id=memorial.id).first()
                if media:
                    uploader.remove_memorial_photo(media.filename) # remove current file stored on disk
                    media.update_filename(new_file)
                else:
                    media = Media(memorial.id, Media.media_types['photo'], new_file)
                    media.save_new_media()
            else:
                status = 'invalid'
                message = ''
    else:
        status = 'unknown'
        message = ''


    return render(ajax=True, status=status, message=message)



@app.route('/wechat')
def wechat():
    url = request.args.get('url') or ''
    title = request.args.get('title') or ''

    return render(page='wechat', title=gettext('Share On WeChat'), url=url, url_title=title)


@app.route('/qr')
def qr():
    text = request.args.get('t') or ''
    print text
    if text:
        # TODO - figure out how to make image fixed width/height
        import flask, qrcode, StringIO

        data = StringIO.StringIO()
        code = qrcode.QRCode( error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=0 )
        code.add_data(text)
        code.make_image().save(data, 'png')
        return flask.send_file( StringIO.StringIO(data.getvalue()), mimetype='image/png' )

    abort(404)



@app.route('/results', methods = ['GET', 'POST'])
def results():
    query = request.args.get('q') or request.form.get('q') or ''
    page_offset = request.args.get('p', type=int) or request.form.get('p', type=int) or 0

    if query:
        results = searcher.query(query, page_offset)
        
        if request.is_xhr:
            return helper.minify( jinjer.element('results', results=results) )
        else:
            total = results[0].total if results else 0
            return render(page='results', title=query, results=results, query=query, total=total)

    return redirect(url_for('index'))



@app.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    user = g.user
    name = helper.get_arg(request, 'name', default=user.name)
    email = helper.get_arg(request, 'email', default=user.email)
    username = helper.get_arg(request, 'username', default=user.username)
    password = helper.get_arg(request, 'password', default=None)
    save, valid = g.user.update(name, email, username, password)
    # TODO - send confirmation email if email was changed
    #from models.code import Code
    #code = Code(user.id)
    #code.save_new_code()
    #mailer.confirm_email(user.name, user.email, code.code)
    #paragraphs = [
    #    'We will be sending you an email shortly containing instructions on how to activate your new account.',
    #    'Be sure to also check your <strong>spam</strong> folder in case it does not appear in your inbox.'
    #]
    #return render(page='confirm', title='Registered!', section='registered', paragraphs=paragraphs)

    return render(page='settings', title=gettext('Settings'), section='profile', user=user, save=save, valid=valid)




@app.route('/profile')
@login_required
def profile():
    return redirect(url_for('settings'))



@app.route('/membership', methods = ['GET', 'POST'])
@login_required
def membership():
    if request.method == 'POST':
        confirm = request.form.get('confirm') or ''
        if confirm:
            action = request.form.get('submit') or ''
            if action and action == 'delete':
                user = g.user
                if user.email:
                    mailer.deactivate_user(user.email, user.name, user.username)

                user.deactivate()
                sessions.logout()
                logout_user()
                paragraphs = [
                    gettext('Your membership has been deactivated.'),
                    gettext('You will now be logged out and taken back to the home page.')
                ]
                return render(page='confirm', title=gettext('Deleted'), section='deleted', header=gettext('Membership Canceled'), paragraphs=paragraphs, refresh=True, url='index')
        else:
            return render(page='settings', title=gettext('Membership'), user=g.user, section='membership', confirm=True)

    return render(page='settings', title=gettext('Membership'), user=g.user, section='membership')



@app.route('/user')
@app.route('/user/<username>')
@app.route('/user/<username>/<action>')
def user(username=None, action=None):
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            if g.user.is_anonymous() or g.user.id != user.id:
                if action is None or action == 'memorials' or action == 'report':
                    results = searcher.created(user.id)
                    return render(page='user', title=user.username, section=action, user=user, results=results, paging=False)

            else:
                return redirect(url_for('settings'))

    abort(404)




@app.route('/user/<username>/report', methods = ['GET', 'POST'])
@login_required
def user_report(username=None):
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            if g.user.id != user.id:
                memorials = searcher.created(user.id)
                report_message = None
                if request.method == 'POST':
                    flag = request.form.get('flag') or ''
                    if flag:
                        from models.flag import Flag
                        flag_type, accused_id = flag[:1], flag[1:]
                        flag = Flag.report(flag_type, accused_id, user.id)
                        if flag:
                            mailer.contact_us('Flagged', user.username, "%s %s has been reported by user %s" % (Flag.get_flag_name(flag_type), accused_id, user.username))
                            report_message = gettext('Thank you. Your report was successfully sent.')
                        else:
                            report_message = gettext('You can only flag each thing once.')

                return render(page='user', title=user.username, section='report', user=user, results=memorials, report_message=report_message)

    return redirect(url_for('settings'))



@app.route('/login', methods = ['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next') or ''
    show_notice = request.args.get('show', type=bool) or request.form.get('show', type=bool) or 0

    if not g.user.is_anonymous():
        return redirect(next_url or url_for('home'))

    username = request.form.get('username') or ''
    password = request.form.get('password') or ''
    remember = ( request.form.get('stay_in', type=bool) or False ) == True

    invalid = False
    if request.method == 'POST':
        if username and password:
            user = User.login(username, password)
            if user:
                if login_user(user, remember):
                    return redirect(next_url or url_for('home'))
        invalid = True

    return render(page='login', title=gettext('Log in'), section='login', username=username, password=password, invalid=invalid, next_url=next_url, show_notice=show_notice)



@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    next_url = request.args.get('next') or request.form.get('next') or ''

    if not g.user.is_anonymous():
        return redirect(next_url or url_for('home'))

    user = User()
    if request.method == 'POST':
        username = request.form.get('username') or ''
        password = request.form.get('password') or ''
        #discoverable = request.form.get('discoverable_by_email', True, bool) == True
        user = User(username=username, password=password)
        if user.validate():
            user.save_new_user()
            login_user(user, True)
            return redirect(next_url or url_for('home'))

    return render(page='signup', title=gettext('Sign up'), section='signup', user=user, next_url=next_url)



@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    next_url = request.args.get('next') or request.form.get('next') or ''

    if not g.user.is_anonymous():
        return redirect(url_for('home'))

    username = ''
    invalid = False
    if request.method == 'POST':
        from models.code import Code
        username = request.form.get('username') or ''
        user, code = Code.forgot_password(username)
        if code:
            mailer.reset_password(user.email, code.code)
            paragraphs = [
                gettext('An email has been sent containing a link to reset your password.'),
                gettext('Be sure to also check your junk or spam folder or filter in case it does not appear in your inbox.')
            ]
            return render(page='confirm', title=gettext('Sent!'), section='sent', paragraphs=paragraphs)
        invalid = True

    return render(page='forgot', title=gettext('Forgot'), section='forgot', invalid=invalid, username=username, next_url=next_url)



@app.route('/reset', methods = ['GET', 'POST'])
def reset():
    if not g.user.is_anonymous():
        return redirect(url_for('home'))


    if sessions.reset_password('has'):
        code = request.form.get('c') or request.args.get('c') or ''
        if code:
            if request.method == 'GET':
                return render(page='reset', title=gettext('Change Password'), code=code)
            else:
                new_password = request.form.get('password') or ''
                valid = User.check_password(new_password)
                if valid == 'ok':
                    from models.code import Code
                    code = Code.query.filter_by(code=code).first()
                    user = User.query.filter_by(id=code.user_id).first()
                    code.deactivate_code()
                    user.change_password(new_password)
                    sessions.reset_password('del')
                    login_user(user, True)
                    paragraphs = [
                        gettext('Your password was successfully changed.'),
                        gettext('Please wait while we log you in.')
                    ]
                    return render(page='confirm', title=gettext('Changed!'), section='changed', paragraphs=paragraphs, refresh=True, url='home')
                else:
                    return render(page='reset', title=gettext('Change Password'), code=code, valid=valid)


    return redirect(url_for('index'))



@app.route('/logout')
@login_required
def logout():
    sessions.logout()
    logout_user()
    return redirect(url_for('index'))





@app.route('/about')
def about():
    meta_desc = gettext('Learn more about why RIPto was created, what our features are, and how you can contribute.')
    meta_words = gettext('RIPto, about, why, history, features, terms, privacy')
    return render(page='footer', title=gettext('About'), section='about', meta_desc=meta_desc, meta_words=meta_words)



@app.route('/support', methods = ['GET', 'POST'])
def support():
    email = request.form.get('email') or ''
    message = request.form.get('message') or ''

    invalid = False
    if request.method == 'POST':
        import re
        if re.match(r'[^@]+@[^@]+\.[^@]+', email) and message:
            mailer.contact_us('Support', email, message)
            paragraphs = [
                gettext('Your message was sent successfully.'),
                gettext('You will now be taken back.')
            ]
            return render(page='confirm', title=gettext('Sent'), section='sent', header=gettext('Message Sent!'), paragraphs=paragraphs, refresh=True, url='support')
        invalid = True

    meta_desc = gettext('Need assistance? Let us know and we will do our best to help.')
    meta_words = gettext('RIPto, support, help')
    return render(page='footer', title=gettext('Support'), section='support', meta_desc=meta_desc, meta_words=meta_words, invalid=invalid, email=email, message=message)



@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    email = request.form.get('email') or ''
    feedback = request.form.get('feedback') or ''

    invalid = False
    if request.method == 'POST':
        import re
        if feedback and (not email or re.match(r'[^@]+@[^@]+\.[^@]+', email)):
            mailer.contact_us('Feedback', email, feedback)
            paragraphs = [
                gettext('Your feedback was sent successfully.'),
                gettext('You will now be taken back.')
            ]
            return render(page='confirm', title=gettext('Sent'), section='sent', header=gettext('Feedback Sent!'), paragraphs=paragraphs, refresh=True, url='feedback')
        invalid = True

    meta_desc = gettext('Have a suggestion? Found a problem? Help us by sending your feedback so we can improve RIPto for everyone.')
    meta_words = gettext('RIPto, feedback, suggestion, problem, bug, report, improve')
    return render(page='footer', title=gettext('Feedback'), section='feedback', meta_desc=meta_desc, meta_words=meta_words, invalid=invalid, email=email, feedback=feedback)



@app.route('/terms')
def terms():
    meta_desc = False
    meta_words = False
    return render(page='footer', title=gettext('Terms'), section='terms', meta_desc=meta_desc, meta_words=meta_words)



@app.route('/privacy')
def privacy():
    meta_desc = False
    meta_words = False
    return render(page='footer', title=gettext('Privacy'), section='privacy', meta_desc=meta_desc, meta_words=meta_words)




@app.route('/translate', methods = ['GET', 'POST'])
def translate():
    from models.liked import Liked
    add_likes = 10
    add_dis = 1
    user = 0
    comment = 6

    for i in range(add_likes):
        db.session.add( Liked(user, comment, 1) )
    for i in range(add_dis):
        db.session.add( Liked(user, comment, -1) )

    db.session.commit()
    lang = request.args.get('lang') or ''
    pofile = []
    saved = False

    if lang:
        pofile = babler.get_po_data(lang, 'messages.po')

        if request.method == 'POST':
            # TODO - add file locking -> github.com/jamesls/flask-shelve/blob/master/flask_shelve.py
            for i in range(len(pofile)):
                msgstr = request.form.get('msgstr' + str(i)) or ''
                pofile[i].msgstr = msgstr # for now we will allow blank fields but need to be aware of accidental deleting
                if ( request.form.get('fuzzy' + str(i)) or '' ) and 'fuzzy' in pofile[i].flags:
                    pofile[i].flags.remove('fuzzy')
            pofile.save()
            pofile.save_as_mofile()
            saved = True


    return render(page='translate', title=gettext('Translate'), section=lang, pofile=pofile, saved=saved)




@app.route('/flag', methods = ['POST'])
@login_required
def flag():
    user = g.user
    flag = request.form.get('flag') or ''

    if flag and request.is_xhr:
        from models.flag import Flag
        flag_type, accused_id = flag[:1], flag[1:]
        flag = Flag.report(flag_type, accused_id, user.id)

        if flag:
            mailer.contact_us('Flagged', user.username, "%s %s has been reported by user %s" % (Flag.get_flag_name(flag_type), accused_id, user.username))
            return render(ajax=True, status='ok', message=gettext('Thank you. Your report was successfully sent.'))

        return render(ajax=True, status='error', message=gettext('You can only flag each thing once.'))


    abort(404)



@app.route('/confirmemail')
def confirmemail():
    code = request.args.get('c') or ''
    email = request.args.get('e') or ''
    report = request.args.get('report') or ''
    if code and email:
        user = User.query.filter_by(email=email).first()
        if user:
            from models.code import Code
            code = Code.query.filter_by(user_id=user.id, code=code, used=False).first()
            if code:
                if report:
                    # TODO - add logic to remove code from db plus render page with: `we apologize for the inconvenience. we have removed this request from our systems. thank you for letting us know. etc...`
                    pass
                if code.code_type == Code.code_types['activation'] and user.status == User.status_types['registered']:
                    code.deactivate_code()
                    user.activate_user()
                    login_user(user, True)
                    return redirect(url_for('home'))
                elif code.code_type == Code.code_types['password'] and user.status == User.status_types['active']:
                    sessions.reset_password('set', True)
                    return redirect(url_for("reset", c=code.code))

    return redirect(url_for('index'))


@app.route('/admin')
@app.route('/admin/<action>', methods = ['GET', 'POST'])
def admin(action=None):
    if g.user.isadmin():
        from models.comment import Comment
        from models.memorial import Memorial

        data = {}
        section = action or 'users' # default to users

        data['users'] = User.query.all()
        data['memorials'] = Memorial.query.all()
        data['comments'] = Comment.query.all()

        return render(page='admin', title=gettext('Admin'), section=section, modals=['calendar'], preloaders=['calendar'], data=data)


    abort(404)



#----------------------------------------
# APIs
#----------------------------------------
@app.route('/field_ok')
def field_ok():
    valid = ''
    if request.args.get('u') or request.args.get('e'):
        if request.args.get('u'):
            valid = User.check_username( request.args.get('u') )
        else:
            valid = User.check_email( request.args.get('e') )

    return '{"valid": "%s"}' % valid



#----------------------------------------
# Errors
#----------------------------------------
@app.errorhandler(404)
def error_404(e):
    return error(404)

@app.errorhandler(Exception)
def error_500(e=None):
    return error(500)

@app.route('/nginxerror.html')
def nginx_error():
    code = int(request.args.get('c'))
    return error(code)

def error(code):
    return render(page='error', status_code=code, code=code)


if __name__ == '__main__':
    # setting up iPhone to Flask:  https://discussions.apple.com/thread/3107930?start=0&tstart=0
    # setting up Virtual Box to Flask: http://stackoverflow.com/questions/1261975/addressing-localhost-from-a-virtualbox-virtual-machine
    app.debug = True
    app.run(host='0.0.0.0')
