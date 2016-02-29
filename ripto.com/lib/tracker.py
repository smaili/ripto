# Flask
from flask import g, request

# RIP
#from config import SESSION_DIR






def init():
    # The process running Flask needs write access to this directory:
    #store = FilesystemStore(SESSION_DIR)
    #KVSessionExtension(store, app)
    pass





def viewed_memorial(memorial):
    from models.viewed import Viewed
    user_id = g.user.id
    ip_addr = request.remote_addr
    memorial_id = memorial.id
    Viewed.viewed_memorial(user_id, ip_addr, memorial_id)




def remembered_memorial(memorial):
    from models.remembered import Remembered
    user_id = g.user.id
    memorial_id = memorial.id
    Remembered.remembered_memorial(user_id, memorial_id)

def has_remembered(memorial):
    from models.remembered import Remembered
    return not g.user.is_anonymous() and Remembered.query.filter_by(user_id=g.user.id, memorial_id=memorial.id, status=Remembered.status_types()['remembered']).first()




def liked_comment(comment, action):
    from models.liked import Liked
    user_id = g.user.id
    comment_id = comment.id
    Liked.liked_comment(user_id, comment_id, action)

def has_liked(comment):
    from models.liked import Liked
    return not g.user.is_anonymous() and Liked.query.filter_by(user_id=g.user.id, comment_id=comment.id, status=Liked.status_types()['like']).first()

def has_disliked(comment):
    from models.liked import Liked
    return not g.user.is_anonymous() and Liked.query.filter_by(user_id=g.user.id, comment_id=comment.id, status=Liked.status_types()['dislike']).first()
