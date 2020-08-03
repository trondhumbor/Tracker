import datetime

from Tracker import db, scheduler
from Tracker.model import Peer

def removeStalePeers():
    app = scheduler.app
    with app.app_context():
        app.logger.info("Background task: removing stale peers")
        longestAcceptableAbsence = 3 * app.config["TRACKER_ANNOUNCE_INTERVAL"]
        for peer in Peer.query.all():
            delta = (datetime.datetime.utcnow() - peer.lastSeen).total_seconds()
            if delta > longestAcceptableAbsence:
                db.session.delete(peer)
        db.session.commit()
