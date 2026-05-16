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
SECRET_KEY = os.environ.get("HMAC_SECRET", "SuperSecretKey@67!").encode("utf-8")

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

    def display_response(response: dict) -> None:
    """
    Shfaq përgjigjen e serverit në formë të lexueshme.
    
    Parametrat:
        response -- Fjalori JSON i marrë nga serveri
    """
    status = response.get("status", "UNKNOWN")
    detail = response.get("detail", "")
    srv_time = response.get("server_time", "")

    print(f"\n  {'─'*49}")
    if status == "OK":
        print(f" Përgjigja e serverit: SUKSES")
    elif status == "FAIL":
        print(f" Përgjigja e serverit: DËSHTIM")
    else:
        print(f" Përgjigja e serverit: GABIM")

    print(f"     Detaj  : {detail}")
    if srv_time:
        print(f"     Koha   : {srv_time}")
    print(f"  {'─'*49}")

    logger.info(f"Përgjigje marrë → Status: {status} | {detail}")


def run_client() -> None:
    """
    Cikli kryesor i ndërfaqes me përdoruesin.
    Lejon dërgimin e mesazheve të shumta deri sa
    përdoruesi zgjedh të dalë.
    """
    print("=" * 55)
    print("   HMAC Authentication Client")
    print("   Siguria e të Dhënave — Projekt Akademik")
    print("=" * 55)
    print(f"   Server  : {HOST}:{PORT}")
    print(f"   Hash    : SHA-256")
    print(f"   Log file: {LOG_FILE}")
    print("=" * 55)
    print("  Shkruani 'exit' ose 'quit' për të dalë.\n")

    logger.info("Klienti u nis.")

    while True:
        try:
            # ── Input nga përdoruesi ─────────────────────
            print()
            message = input(" Shkruani mesazhin tuaj: ").strip()

            if message.lower() in ("exit", "quit", ""):
                if message == "":
                    print("  Mesazhi nuk mund të jetë bosh. Provoni sërish.")
                    continue
                print("\n  Po mbyllim klientin. Mirupafshim!")
                logger.info("Klienti u ndal nga përdoruesi.")
                break

            # ── Dërgimi i mesazhit ───────────────────────
            logger.info(f"Përdoruesi dërgon mesazhin: '{message}'")
            response = send_message(message)
            display_response(response)

        except ConnectionRefusedError:
            print(f"\n  GABIM: Nuk mund të lidhem me serverin në {HOST}:{PORT}.")
            print(f"     Sigurohuni që serveri është aktiv dhe provoni sërish.")
            logger.error(f"Lidhja u refuzua. Serveri nuk është aktiv në {HOST}:{PORT}.")

        except TimeoutError:
            print(f"\n  GABIM: Lidhja me serverin skadoi (timeout).")
            logger.error("Lidhja skadoi (timeout).")

        except json.JSONDecodeError:
            print(f"\n  GABIM: Përgjigja e serverit nuk është e vlefshme.")
            logger.error("Përgjigja e serverit nuk mund të parsohej si JSON.")

        except KeyboardInterrupt:
            print("\n\n  Klienti u ndal me Ctrl+C.")
            logger.info("Klienti u ndal me Ctrl+C.")
            break

        except Exception as exc:
            print(f"\n  Gabim i papritur: {exc}")
            logger.error(f"Gabim i papritur: {exc}")


if __name__ == "__main__":
    run_client()