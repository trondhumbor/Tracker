import datetime

from .. import db

class Peer(db.Model):
    __tablename__ = "peer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstSeen = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    lastSeen = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    peerId = db.Column(db.String(20), nullable=False)
    ip = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False)
    uploaded = db.Column(db.Integer)
    downloaded = db.Column(db.Integer)
    left = db.Column(db.Integer)
    event = db.Column(db.String)

    torrent_id = db.Column(db.Integer, db.ForeignKey("torrent.id"),
                            nullable=False)

    def __repr__(self) -> str:
        return repr({
            "id": self.id,
            "firstSeen": self.firstSeen,
            "lastSeen": self.lastSeen,
            "peerId": self.peerId,
            "ip": self.ip,
            "port": self.port,
            "uploaded": self.uploaded,
            "downloaded": self.downloaded,
            "left": self.left,
            "event": self.event
        })

