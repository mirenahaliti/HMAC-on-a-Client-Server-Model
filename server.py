"""
=============================================================
  HMAC Authentication Server - Siguria e të Dhënave
=============================================================
Ky server pret mesazhe nga klientët, verifikon autenticitetin
dhe integritetin e tyre duke përdorur HMAC-SHA256.
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