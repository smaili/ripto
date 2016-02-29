# System
import logging

# RIP
from config import LOG_FILE, LOG_LEVEL



app = None



def init():
    fh = logging.FileHandler(LOG_FILE)
    app.logger.addHandler(fh)
    app.logger.setLevel(LOG_LEVEL)



def info(msg):
    app.logger.info(msg)



def error(msg):
    app.logger.info(msg)



def exception(msg=''):
    logging.exception(msg)



def log_uwsgi(request, response):
    # https://github.com/unbit/uwsgi-docs/blob/master/LogFormat.rst
    # http://qph.is.quoracdn.net/main-qimg-83b508e02a70cab9ffcb9fb454adead4
    # http://qph.is.quoracdn.net/main-qimg-d2b92db82ed27aecc6bf5788d75e6a26
    # http://qph.is.quoracdn.net/main-qimg-fde4d84bf459d14aff0ef930e4f8c7fe
    # TODO - http://stackoverflow.com/questions/12523044/how-can-i-tail-a-log-file-in-python
    import socket, uwsgi
    try:
        hostname,alias,addresslist = socket.gethostbyaddr(request.remote_addr)
    except:
        hostname = 'Unknown'

    uwsgi.set_logvar('hostname', hostname)
