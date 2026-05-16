"""
=============================================================
  HMAC Authentication Client - Siguria e të Dhënave
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

# ─────────────────────────────────────────────
#  KONFIGURIMI I LOGGING-UT
# ─────────────────────────────────────────────
LOG_FILE = "client_log.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("HMAC-Client")

# ─────────────────────────────────────────────
#  ÇELËSI I PËRBASHKËT (pre-shared secret key)
#  Duhet të jetë IDENTIK me atë të serverit.
#  Në prodhim lexohet nga environment variable.
# ─────────────────────────────────────────────
SECRET_KEY = os.environ.get("HMAC_SECRET", "SuperSecretKey@67!").encode("utf-8")

# Konfigurime rrjeti
HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 4096

def generate_hmac(message: str) -> str:
    """
    Gjeneron HMAC-SHA256 për mesazhin e dhënë.
    
    Algoritmi:
        HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
        ku H = SHA-256, K = çelësi sekret, m = mesazhi
    
    Parametrat:
        message -- Teksti i mesazhit që do të dërgohet
    
    Kthon:
        HMAC si varg hexadecimal (64 karaktere)
    """
    mac = hmac.new(
        SECRET_KEY,
        message.encode("utf-8"),
        hashlib.sha256
    )
    return mac.hexdigest()

def send_message(message: str) -> dict:
    """
    Dërgon mesazhin me HMAC-in te serveri dhe merr përgjigjen.
    
    Parametrat:
        message -- Teksti i mesazhit
    
    Kthen:
        Fjalorin JSON të përgjigjes nga serveri
    
    Shkakton:
        ConnectionRefusedError nëse serveri nuk është aktiv
        TimeoutError nëse lidhja skadon
        Exception për gabime të tjera rrjeti
    """
    # ── Gjenerimi i HMAC-it ──────────────────────────────
    logger.info(f"Duke gjeneruar HMAC për mesazhin: '{message}'")
    mac_value = generate_hmac(message)
    logger.info(f"HMAC gjeneruar: {mac_value[:20]}...")

    # ── Ndërtimi i paketës JSON ──────────────────────────
    payload = json.dumps({
        "message": message,
        "hmac": mac_value,
        "timestamp": datetime.datetime.now().isoformat()
    })

    # ── Shfaqja në konsol ────────────────────────────────
    print(f"\n   Duke dërguar mesazhin me HMAC:")
    print(f"     Teksti : {message}")
    print(f"     HMAC   : {mac_value[:16]}...{mac_value[-8:]}")
    logger.info(f"Paketa gati | Dërgim te {HOST}:{PORT}")