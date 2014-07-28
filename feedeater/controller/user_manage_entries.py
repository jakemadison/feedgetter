from feedeater.database.models import UserFeeds, Entry, UserEntry
from feedeater import db

db_session = db.session


def mark_entry_read(entryid, userid):

    """ check for existence of user_feed_entry for user/entryid combo
     if exists, make unread = False
     if doesn't exist, make new record with unread=False"""

    print 'marking as read',
    print entryid, userid

    current_state = db_session.query(UserEntry).filter(UserFeeds.userid == userid,
                                                   UserEntry.entryid == entryid,
                                                   UserEntry.userfeedid == UserFeeds.id).first()

    if current_state is None:
        print "no userEntry found, adding a new one..."

        entry = db_session.query(Entry).filter(Entry.id == entryid).first()
        uf_id = db_session.query(UserFeeds).filter(UserFeeds.userid == userid,
                                                   UserFeeds.feedid == entry.feed_id).first().id

        new_user_entry = UserEntry(entryid, userid, userfeedid=uf_id, starred=False, unread=False)
        db_session.add(new_user_entry)
        db_session.commit()
        return True

    print 'does exist, updating'
    qry = db_session.query(UserEntry).filter(UserEntry.id == current_state.id)

    qry.update({"unread": False})
    db_session.commit()

    return
