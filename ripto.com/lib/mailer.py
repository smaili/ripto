# System
import smtplib
from threading import Thread

# Flask
from flask import render_template, url_for
from flask.ext.mail import Message, Mail
from flask.ext.babel import gettext

# RIP
from config import MAIL_SENDERS, MAIL_HTML, MAIL_TEXT, MAIL_SERVER, MAIL_PORT, MAIL_TIMEOUT
from lib import jinjer



mail = Mail()
app = None


def contact_us(category, email, message):
    subject = '%s message from %s' % (category, email)

    _send_email(
        subject,
        MAIL_SENDERS['NOREPLY'],
        'smaili86@gmail.com', # TODO - create a support email so I don't have to email to myself
        'contact_email',
        header="Message", email=email, message=message, report=False
    )


def share_memorial(email, sharer, memorial, message):
    subject = jinjer.memorial_share_title(memorial)
    cta = jinjer.memorial_url(memorial=memorial, _short=True, _external=True)

    _send_email(
        subject,
        MAIL_SENDERS['NOREPLY'],
        email,
        'share_email',
        header=subject, email=email, cta=cta, sharer=sharer, memorial=memorial, message=message, report=False
    )


def reset_password(email, code):
    subject = gettext('Request for changing your password on RIPto')
    cta = url_for("confirmemail", e=email, c=code, _external=True)

    _send_email(
        subject,
        MAIL_SENDERS['NOREPLY'],
        email,
        'reset_email',
        header=subject, email=email, cta=cta, report=False
    )


def deactivate_user(email, name, username):
    subject = gettext('You have deactivated your RIPto account')

    _send_email(
        subject,
        MAIL_SENDERS['NOREPLY'],
        email,
        'deactivate_email',
        header=subject, email=email, name=name, username=username, report=False
    )


def ban_user(email, name, username):
    subject = gettext('You have been banned from RIPto')

    _send_email(
        subject,
        MAIL_SENDERS['NOREPLY'],
        email,
        'ban_email',
        header=subject, email=email, name=name, username=username, report=False
    )




"""
def confirm_email(name, email, code):
    cta = url_for("confirmemail", e=email, c=code, _external=True)
    report = url_for("confirmemail", report=1, c=code, e=email, _external=True)

    _send_email(
        'Just one more step to get started on RIPto',     # subject
        MAIL_SENDERS['NOREPLY'],                        # sender
        [ email ],                                      # recipients
        'confirm_email',                                # page
        title='RIPto', name=name, email=email, code=code  # template args
    )
"""



"""
    Helpers
"""
def _render(page, **args):
    # layout = MAIL_HTML[page]
    # (TEXT, HTML)
    #return render_template(MAIL_TEXT[page], **args), render_template(layout, page=page, **args)
    return render_template(MAIL_TEXT[page], **args), render_template(MAIL_HTML[page], **args)


def _send_email(subject, sender, recipients, page, **args):
    #msg = Message(subject, sender = sender, recipients = recipients)
    #msg.body, msg.html = _render(page, **args)
    #thr = Thread(target = _send_async_email, args = [msg])
    text, html = _render(page, **args)
    thr = Thread(target = _send_async_email, args = [subject, sender, recipients, text, html])
    thr.start()



#def _send_async_email(msg):
#    with app.app_context():
#        mail.send(msg)



# TODO - add sanitizing
def _send_async_email(subject, sender, recipients, text, html):
    if type(recipients) is not list:
        recipients = [ recipients ]

    # some clean up before actual send
    subject = jinjer.encode( subject )
    text = jinjer.encode( text )
    html = jinjer.encode( html.replace('  ', '').replace('\n', '') )

    _send_it(subject, sender, recipients, text, html, 0)



# http://stackoverflow.com/questions/882712/sending-html-email-in-python
def _send_it(subject, sender, recipients, text, html, tries):
    import cStringIO, mimetools, MimeWriter


    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)
    writer = MimeWriter.MimeWriter(out)


    # headers
    writer.addheader("From", sender)
    writer.addheader("To", ','.join(recipients))
    writer.addheader("Subject", subject)
    writer.addheader("X-Mailer", "SmailiMail [version 1.0]")
    writer.addheader("MIME-Version", "1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    # text
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'UTF-8')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()

    # html
    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/html", [("charset", 'UTF-8')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()

    # to string
    writer.lastpart()
    msg = out.getvalue()
    out.close()



    class PostFixThread(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.result = False
        def run(self):
            self.result = _call_postfix(sender, recipients, msg)
                

    thr = PostFixThread()
    thr.start()
    thr.join(MAIL_TIMEOUT)
    if thr.isAlive():
        Thread._Thread__stop(thr)
        thr.result = False

    if not thr.result and tries < 5:
        _send_it(subject, sender, recipients, text, html, tries + 1)

            

def _call_postfix(sender, recipients, msg):
    try:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=MAIL_TIMEOUT)
        server.sendmail(sender, recipients, msg)
        server.quit()
    except:
        try:
            server.quit()
        except:
            pass
        return False

    return True
