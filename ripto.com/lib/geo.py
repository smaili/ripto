# System
import json, urllib2

# Flask
import flask

# RIP
from config import LOG_FILE, LOG_LEVEL, GEO_SERVICES

# https://news.ycombinator.com/item?id=6759220

request = None


def init():
    pass



def country_code():
    data = _get_data()
    if data:
        # NOTE - keys must be in same order as GEO_SERVICES list
        possible_keys = [ 'country_code', 'countryCode', 'country'  ]
        for key in possible_keys:
            if key in data:
                return data[key]

    return False


def _get_data():
    if not hasattr(flask.g, 'geodata'):
        ip = request.remote_addr
        for service in GEO_SERVICES:
            url = service % ip
            try:
                data = json.load( _curl(url) )
                break
            except:
                pass
        flask.g.geodata = data or ''

    return flask.g.geodata


def _curl(url):
    return urllib2.urlopen( url, timeout=.5 ) # half a second timeout
