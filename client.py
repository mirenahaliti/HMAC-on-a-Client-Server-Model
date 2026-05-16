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
