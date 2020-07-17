from .. import db

class Torrent(db.Model):
    __tablename__ = "torrent"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    infoHash = db.Column(db.Text, nullable=False, unique=True)
    peers = db.relationship("Peer", backref="peer", lazy=True)

    def __repr__(self) -> str:
        return repr({
            "id": self.id,
            "infoHash": self.infoHash,
            "peers": self.peers
        })