# -*- coding: utf-8 -*-




#----------------------------------------
# Domain
#----------------------------------------
SERVER_NAME = 'rip.to'



#----------------------------------------
# DB
#----------------------------------------
db_host = 'localhost'
db_user = 'root'
db_pass = '0380BEA27363E56C37F0BFDA438F429080848051'
db_name = 'rt'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % ( db_user, db_pass, db_host, db_name )
