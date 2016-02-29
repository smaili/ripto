# System
from datetime import date, timedelta

# Flask
from sqlalchemy import and_, asc, desc, func

# RIP
from config import RESULTS_COUNT
from models.memorial import Memorial
from models.media import Media





def init():
    # The process running Flask needs write access to this directory:
    #store = FilesystemStore(SESSION_DIR)
    #KVSessionExtension(store, app)
    pass




def most(filter_by, time_by, page_offset):
    results = Memorial.query.filter(Memorial.status == 3)

    if filter_by == 0:
        results.order_by(desc(Memorial.views))
    elif filter_by == 1:
        results = results.order_by(desc(Memorial.condolences))
    elif filter_by == 2:
        results = results.order_by(desc(Memorial.remembers))

    # we don't need a date constraint on 'all time'
    # if time_by in range(0, 4):
    if False:
        today = date.today()
        if time_by == 0:
            delta = today
        elif time_by == 1:
            delta = today - timedelta(days=1)
        elif time_by == 2:
            delta = today - timedelta(weeks=1)
        else:
            delta = today - timedelta(weeks=4)
        results = results.filter( Memorial.created >= delta )

    page_offset = page_offset * RESULTS_COUNT
    results = results.limit(RESULTS_COUNT + 1).offset(page_offset) # we grab the extra so we know whether there is more left after this query

    results = results.all() # use all so it returns as a list
    for memorial in results:
        memorial.media = Media.query.filter_by(memorial_id=memorial.id).first() # first() for now since each memorial will have just one picture

    return results



def query(query, page_offset):
    from models import db

    # TODO - figure out how to get it with one query + subquery instead of 2 separate queries
    #where = "status = 3 AND (name LIKE :query OR epitaph LIKE :query OR funeral_loc LIKE :query)"
    #results = db.session.execute("SELECT *, (SELECT COUNT(*) FROM memorials WHERE " + where + ") total FROM memorials WHERE " + where + "LIMIT :limit", { 'query': '%'+query+'%', 'limit': RESULTS_COUNT + 1 } ).fetchall()
    query = '%' + query + '%'
    query_filter = Memorial.name.like(query) | Memorial.epitaph.like(query) | Memorial.funeral_loc.like(query)
    page_offset = page_offset * RESULTS_COUNT
    results = Memorial.query.with_entities(Memorial.id, Memorial.name, Memorial.dob, Memorial.dod, Memorial.url).filter(Memorial.status == 3, query_filter).limit(RESULTS_COUNT + 1).offset(page_offset).all()

    if results and not page_offset:
        results[0].total = db.session.query(func.count('*')).select_from(Memorial).filter(Memorial.status == 3, query_filter).scalar()

    for memorial in results:
        memorial.media = Media.query.filter_by(memorial_id=memorial.id).first() # first() for now since each memorial will have just one picture

    return results



def created(user_id):
    results = Memorial.query.filter(Memorial.user_id == user_id, Memorial.status == 3).all()

    for memorial in results:
        memorial.media = Media.query.filter_by(memorial_id=memorial.id).first() # first() for now since each memorial will have just one picture

    return results


def remembered(user_id):
    from models.remembered import Remembered

    # TODO - use raw query -> SELECT * FROM memorials WHERE id IN (SELECT memorial_id FROM remembered WHERE user_id = <user_id>) AND status = 3;
    remembers = Remembered.query.with_entities(Remembered.memorial_id).filter(Remembered.user_id == user_id).all()
    results = []
    for remember in remembers:
        memorial = Memorial.query.filter(Memorial.id == remember.memorial_id, Memorial.status == 3).first()
        memorial.media = Media.query.filter_by(memorial_id=memorial.id).first() # first() for now since each memorial will have just one picture
        results.append(memorial)

    return results



"""
def memorials(section, query, filter_by, sort_by, last, user):
    # TODO - add a limit/pagination
    from models.memorial import Memorial
    from models.media import Media
    from models.viewed import Viewed

    if section == 'viewed':
        results = Memorial.query.join(Viewed, and_(Memorial.id == Viewed.memorial_id, Memorial.user_id != user.id))
    elif section == 'created':
        results = Memorial.query.filter_by(user_id=user.id)
    else:
        results = Memorial.query

    results = results.filter(Memorial.status == 3)

    if query:
        query = '%' + query + '%'
        if filter_by == 'name':
            f = Memorial.name.like(query)
        elif filter_by == 'born':
            f = Memorial.dob.like(query)
        elif filter_by == 'dead':
            f = Memorial.dod.like(query)
        elif filter_by == 'epitaph':
            f = Memorial.epitaph.like(query)
        elif filter_by == 'funeral':
            f = Memorial.funeral_place.like(query) | Memorial.funeral_loc.like(query)
        else:
            f = Memorial.name.like(query) | Memorial.dob.like(query) | Memorial.dod.like(query) | Memorial.epitaph.like(query) | Memorial.funeral_place.like(query) | Memorial.funeral_loc.like(query)

        results = results.filter(f)


    if section == 'viewed' and sort_by == '':
        results = results.order_by(desc(Viewed.modified))
    elif sort_by == 'name':
        results = results.order_by(asc(Memorial.name))
    else:
        results = results.order_by(desc(Memorial.created))


    results = results.all() # use all so it returns as a list
    for memorial in results:
        memorial.media = Media.query.filter_by(memorial_id=memorial.id).first() # first() for now since each memorial will have just one picture

    return results
"""
