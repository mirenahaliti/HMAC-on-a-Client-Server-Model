"""
=============================================================
  HMAC Authentication Server - Siguria e të Dhënave
=============================================================

"""
import socket
import hmac
import hashlib
import json
import logging
import datetime
import os
import sys


LOG_FILE = "server_log.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("HMAC-Server")
SECRET_KEY = os.environ.get("HMAC_SECRET", "SuperSecretKey@67!").encode("utf-8")
HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 4096

def verify_hmac(message: str, received_hmac: str) -> bool:
    expected_hmac = hmac.new(
        SECRET_KEY,
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_hmac, received_hmac)

def handle_client(conn: socket.socket, addr: tuple) -> None:
    logger.info(f"Lidhje e re nga klienti: {addr}")
    print(f"\n{'─'*55}")
    print(f"  Klient i ri i lidhur: {addr[0]}:{addr[1]}")
    print(f"{'─'*55}")

    try:
        raw_data = conn.recv(BUFFER_SIZE)
        if not raw_data:
            logger.warning("Klienti u shkëput pa dërguar të dhëna.")
            return
        try:
            payload = json.loads(raw_data.decode("utf-8"))
        except json.JSONDecodeError:
            logger.error("Gabim: Formati i paketës është i pasaktë (jo JSON).")
            _send_response(conn, status="ERROR", detail="Paketa nuk është JSON e vlefshme.")
            return

        message  = payload.get("message", "")
        recv_hmac = payload.get("hmac", "")
        timestamp = payload.get("timestamp", "N/A")

        # ── Shfaqje në konsol ──────────────────────────────
        print(f"\n   Mesazh i marrë:")
        print(f"     Teksti   : {message}")
        print(f"     HMAC     : {recv_hmac[:16]}...{recv_hmac[-8:]}")
        print(f"     Koha     : {timestamp}")
        logger.info(f"Mesazh marrë | Teksti: '{message}' | HMAC: {recv_hmac[:20]}...")