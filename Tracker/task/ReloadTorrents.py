import hashlib
import os
from urllib.parse import unquote_plus, quote_plus

from Tracker import bencode, db, scheduler
from Tracker.model import Torrent

def reloadTorrents():
    app = scheduler.app
    with app.app_context():
        app.logger.info("Background task: reloading torrents")
        folder = app.config["TRACKER_TORRENT_FOLDER"]
        for metainfo in os.listdir(folder):
            file = os.path.join(folder, metainfo)
            if not file.endswith(".torrent"):
                continue

            with open(file, "rb") as f:
                dct = bencode.bdecode(f.read())[b"info"]

                sha = hashlib.sha1()
                sha.update(bencode.bencode(dct))
                infoHash = unquote_plus(quote_plus(sha.digest()))

                torrent = Torrent.query.filter_by(infoHash=infoHash).first()
                if torrent is None:
                    torrent = Torrent(infoHash=infoHash)

                    db.session.add(torrent)
                    db.session.commit()
