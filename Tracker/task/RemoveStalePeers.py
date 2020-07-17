import datetime

from Tracker import db, scheduler
from Tracker.model import Peer

def removeStalePeers():
    app = scheduler.app
    with app.app_context():
        app.logger.info("Background task: removing stale peers")
        for peer in Peer.query.all():
            delta = datetime.datetime.now() - peer.lastSeen
            if delta > 3*app.config["TRACKER_ANNOUNCE_INTERVAL"]:
                db.session.delete(peer)
        db.session.commit()
