"""
RIPto
-----------------
A place to remember

Links
`````
* `website <http://ripto.com>`_
"""


# http://hg.flowblok.id.au/enscribe/src/
# http://flask.pocoo.org/docs/patterns/packages/
# https://github.com/miguelgrinberg/microblog/tree/v0.14
# https://github.com/imwilsonxu/fbone



from setuptools import setup, find_packages

setup(
    name='RIPto',
    version='1.0',
    description='A place to remember',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Michael Smaili',
    author_email='smaili86@gmail.com',
    url='http://ripto.com',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    install_requires=[
        'flask>=1.0', # pip install Flask, pip install -U Flask
        'Flask-Login', # pip install flask-login
        'Flask-KVSession', # pip install Flask-KVSession
        'Flask-SQLAlchemy', # pip install flask-sqlalchemy
        'sqlalchemy>=0.7', # pip install sqlalchemy
        'mysql-python', # pip install mysql-python
        'flask-mail', # pip install flask-mail
        'Flask-Babel', # pip install Flask-Babel
        'Flask-Assets' # pip install Flask-Assets
    ]
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
