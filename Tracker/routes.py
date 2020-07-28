import datetime
from ipaddress import ip_address

from flask import request, make_response
from flask import current_app as app

from . import db, bencode
from .model import Peer, Torrent

@app.route("/announce")
def announce():
    args = request.args

    requiredKeys = ("info_hash", "peer_id", "port", "uploaded", "downloaded", "left")
    if not all(k in args for k in requiredKeys):
        txt = bencode.bencode({"failure reason": "Not enough query parameters provided"})
        response = make_response(txt, 400)
        response.mimetype = "text/plain"
        return response

    infoHash = args.get("info_hash")
    torr = Torrent.query.filter_by(infoHash=infoHash).first()
    if torr is None:
        response = make_response(bencode.bencode({"failure reason": "No such torrent"}), 404)
        response.mimetype = "text/plain"
        return response

    peerId = args.get("peer_id")
    ip = args.get("ip", request.remote_addr)
    port = args.get("port", type=int)
    uploaded = args.get("uploaded", type=int)
    downloaded = args.get("downloaded", type=int)
    left = args.get("left", type=int)
    event = args.get("event")

    peer = Peer.query.filter_by(peerId=peerId, ip=ip, port=port).first()
    if peer is None:
        # Peer not found
        peer = Peer(
            peerId=peerId,
            ip=ip, port=port,
            uploaded=uploaded, downloaded=downloaded, left=left, event=event
        )
        torr.peers.append(peer)
        db.session.add(peer)
        db.session.commit()
    else:
        # Peer found
        peer.lastSeen = datetime.datetime.utcnow()
        peer.uploaded = uploaded
        peer.downloaded = downloaded
        peer.left = left
        if event:
            peer.event = event
        db.session.commit()

    dct = {
        "interval": app.config["TRACKER_ANNOUNCE_INTERVAL"],
        "complete": sum((1 if p.left == 0 else 0) for p in torr.peers),
        "incomplete": sum((1 if p.left != 0 else 0) for p in torr.peers),
        "peers": b"".join(ip_address(p.ip).packed + p.port.to_bytes(2, "big") for p in torr.peers)
    }

    fullResponse = args.get("compact", 1, type=int) == 0
    if fullResponse:
        dct["peers"] = [
            {
                "peer id": peer.peerId,
                "ip": peer.ip,
                "port": peer.port
            } for peer in torr.peers
        ]

    response = make_response(bencode.bencode(dct), 200)
    response.mimetype = "text/plain"
    return response

@app.route("/scrape")
def scrape():
    args = request.args
    if not "info_hash" in args:
        txt = bencode.bencode({"failure reason": "Not enough query parameters provided"})
        response = make_response(txt, 400)
        response.mimetype = "text/plain"
        return response

    dct = {
        "files": {
        }
    }

    infoHashes = args.getlist("info_hash")
    for infoHash in infoHashes:
        torr = Torrent.query.filter_by(infoHash=infoHash).first()
        if torr is None:
            continue

        dct["files"][torr.infoHash] = {
            "complete": sum((1 if p.left == 0 else 0) for p in torr.peers),
            "downloaded": sum((1 if p.event == "complete" else 0) for p in torr.peers),
            "incomplete": sum((1 if p.left != 0 else 0) for p in torr.peers)
        }

    response = make_response(bencode.bencode(dct), 200)
    response.mimetype = "text/plain"
    return response
