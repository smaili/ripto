import os, subprocess, sys



if sys.platform == 'win32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
    pybabel = 'pybabel'


"""
Adds a new language
"""
def init(lang=None):
    if lang is None:
        from config import LANGUAGES
        lang = []
        for (lang_code, display, ldir, enabled) in LANGUAGES:
            lang_code = ''.join( [ c if i < 3 else c.upper() for i,c in enumerate(lang_code) ] ) # e.g., zh_cn -> zh_CN
            if lang_code != 'en' and not os.path.exists( 'translations/' + lang_code ):
                lang.append(lang_code)
    else:
        lang = [ lang ]

    if lang:
        os.system(pybabel + ' extract --no-wrap -F babels.cfg -k lazy_gettext -o messages.pot .')
        for lang_code in lang:
            os.system(pybabel + ' init -i messages.pot -d translations -l ' + lang_code)
        os.unlink('messages.pot')



"""
Compiles every po file into a binary mo file
"""
def compile(lang=None):
    os.system(pybabel + ' compile -d translations')



"""
Uppdates all po files with new texts from .py and .pyhtml files
"""
def update(lang=None):
    os.system(pybabel + ' extract --no-wrap -F babels.cfg -k lazy_gettext -o messages.pot .')
    os.system(pybabel + ' update --ignore-obsolete -i messages.pot -d translations')
    os.unlink('messages.pot')



if __name__=="__main__":
    try:
        action = sys.argv[1]
        lang = ( sys.argv[2] if len(sys.argv) > 2 else None )

        globals()[action](lang)

        subprocess.call(['sudo', 'chown', '-R', 'uwsgi:nginx', 'translations' ])

    except:
        print ""
        print "To use: python babels.py init|compile|update <language-code>"
        print ""
        import traceback
        traceback.print_exc()
