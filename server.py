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
def _send_response(conn: socket.socket, status: str, detail: str) -> None:
    """
    Dërgon përgjigjen JSON tek klienti.
    
    Parametrat:
        conn   -- Lidhja socket
        status -- "OK", "FAIL", ose "ERROR"
        detail -- Mesazhi i detajuar i statusit
    """
    response = json.dumps({
        "status": status,
        "detail": detail,
        "server_time": datetime.datetime.now().isoformat()
    })
    conn.sendall(response.encode("utf-8"))
    logger.info(f"Përgjigje dërguar → Status: {status} | {detail}")


def start_server() -> None:
    """
    Nis serverin dhe pret lidhje nga klientët.
    Trajton çdo lidhje në mënyrë sekuenciale.
    """
    print("=" * 55)
    print("   HMAC Authentication Server")
    print("   Siguria e të Dhënave")
    print("=" * 55)
    print(f"   Host    : {HOST}")
    print(f"   Port    : {PORT}")
    print(f"   Log file: {LOG_FILE}")
    print("=" * 55)

    logger.info(f"Serveri po niset në {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # SO_REUSEADDR: lejojmë ripërdorimin e portit pas mbylljes
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(5)

        print(f"\n Serveri është aktiv dhe pret mesazhe...\n")
        logger.info("Serveri filloi të dëgjojë lidhje.")

        try:
            while True:
                conn, addr = server_sock.accept()
                handle_client(conn, addr)
        except KeyboardInterrupt:
            print("\n\n Serveri u ndal nga përdoruesi (Ctrl+C).")
            logger.info("Serveri u ndal me Ctrl+C.")


if __name__ == "__main__":
    start_server()
