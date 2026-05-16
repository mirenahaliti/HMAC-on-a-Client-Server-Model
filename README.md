# HMAC-on-a-Client-Server-Model
### Siguria e të Dhënave — Projekti 3

--

## Përshkrim i Projektit

Ky projekt implementon një sistem komunikimi të sigurt mes klientit dhe serverit duke përdorur **HMAC-SHA256** (Hash-based Message Authentication Code).

### Çfarë ofron sistemi:
- **Autenticitet** — Konfirmon se mesazhi vjen nga burimi i saktë
- **Integritet** — Garanton se mesazhi nuk është modifikuar gjatë transmetimit
- **Rezistencë ndaj Timing Attacks** — Krahasim me `hmac.compare_digest()`
- **Logging** — Regjistron të gjitha veprimet kyçe

---

## Struktura e Projektit

```
hmac_project/
├── server.py        ← Serveri: verifikon HMAC-et e pranuara
├── client.py        ← Klienti: gjeneron dhe dërgon HMAC-et
├── server_log.txt   ← Krijohet automatikisht gjatë ekzekutimit
├── client_log.txt   ← Krijohet automatikisht gjatë ekzekutimit
└── README.md        ← Ky skedar
```

---

##  Kërkesat e Sistemit

| Kërkesë       | Detaj                              |
|---------------|------------------------------------|
| Python        | 3.7 ose më i lartë                 |
| Librari       | `hmac`, `hashlib`, `socket`, `json` (të gjitha standard) |
| OS            | Windows / macOS / Linux            |

> **Asnjë instalim i jashtëm nuk nevojitet.** Të gjitha librari janë pjesë e Python Standard Library.

---

## Si të ekzekutoni projektin

### Hapi 1 — Klononi / hapni direktorinë e projektit

```bash
cd hmac_project
```

### Hapi 2 — Nisni Serverin

Hapni një terminal të parë dhe ekzekutoni:

```bash
python server.py
```

Serveri do të fillojë të dëgjojë lidhje dhe do të shfaqë:

```
=======================================================
   HMAC Authentication Server
=======================================================
   Host    : 127.0.0.1
   Port    : 65432
   Log file: server_log.txt
=======================================================

    Serveri është aktiv dhe pret mesazhe...
```

### Hapi 3 — Nisni Klientin

Hapni një **terminal të dytë** (serveri duhet të mbetet aktiv) dhe ekzekutoni:

```bash
python client.py
```

---

## Formati i Input/Output

### Klienti — Input

```
     Shkruani mesazhin tuaj: Ky është një mesazh i sigurt.
```

- Shkruani çdo tekst dhe shtypni **Enter**
- Shkruani `exit` ose `quit` për të dalë

### Klienti — Output (mesazh i dërguar)

```
     Duke dërguar mesazhin me HMAC:
     Teksti : Ky është një mesazh i sigurt.
     HMAC   : a3f9c1b2e4d7...8f2a

  ─────────────────────────────────────────────────
     Përgjigja e serverit: SUKSES
     Detaj  : Mesazhi u verifikua me sukses. Integriteti dhe autenticiteti konfirmohet.
     Koha   : 2024-11-15T14:32:01.123456
  ─────────────────────────────────────────────────
```

### Serveri — Output (mesazh i marrë dhe verifikuar)

```
  ───────────────────────────────────────────────────────
  Klient i ri i lidhur: 127.0.0.1:54321
  ───────────────────────────────────────────────────────

     Mesazh i marrë:
     Teksti   : Ky është një mesazh i sigurt.
     HMAC     : a3f9c1b2e4d7...8f2a
     Koha     : 2024-11-15T14:32:01.000000

    Duke validuar HMAC...

    HMAC VALID — Mesazhi është autentik dhe i paprekur!
```

---

## Çelësi Sekret i Përbashkët

Çelësi default është i koduar në kod:

```python
SECRET_KEY = "SuperSecretKey@67!"
```

### Ndryshimi i çelësit (mënyra e sigurt):

Vendosni një **environment variable** para ekzekutimit:

**Linux / macOS:**
```bash
export HMAC_SECRET="ÇelësiJuajSekretIFortë!"
python server.py
# terminal tjetër:
export HMAC_SECRET="ÇelësiJuajSekretIFortë!"
python client.py
```

**Windows (PowerShell):**
```powershell
$env:HMAC_SECRET = "ÇelësiJuajSekretIFortë!"
python server.py
```

> **Kujdes:** Klienti dhe serveri **duhet të kenë të njëjtin çelës** ose verifikimi do të dështojë.

---

## Protokolli i Komunikimit

### Formati i Paketës (JSON)

**Klienti → Server:**
```json
{
  "message": "Teksti i mesazhit",
  "hmac": "a3f9c1b2e4d78f0123456789abcdef0123456789abcdef0123456789abcdef01",
  "timestamp": "2024-11-15T14:32:01.000000"
}
```

**Server → Klienti:**
```json
{
  "status": "OK",
  "detail": "Mesazhi u verifikua me sukses.",
  "server_time": "2024-11-15T14:32:01.123456"
}
```

### Kodet e Statusit

| Status  | Kuptimi                                        |
|---------|------------------------------------------------|
| `OK`    | HMAC valid — mesazhi është autentik            |
| `FAIL`  | HMAC invalid — mesazhi është modifikuar        |
| `ERROR` | Gabim protokolli (JSON i keq, fusha mungojnë)  |

---

## Si funksionon HMAC

```
HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))

ku:
  H    = SHA-256 (funksioni hash)
  K    = Çelësi sekret i përbashkët
  m    = Mesazhi
  ⊕    = XOR
  ||   = Konkatenacion
  ipad = 0x36 (i përsëritur)
  opad = 0x5C (i përsëritur)
```

**Rezultati:** 256 bit = 64 karaktere hexadecimal

---

## Masat e Sigurisë

| Masa                   | Implementimi                                    |
|------------------------|-------------------------------------------------|
| Timing attack          | `hmac.compare_digest()` për krahasim konstantë  |
| Çelësi sekret          | Environment variable (jo i koduar hard)         |
| Integritet             | SHA-256 — rezistent ndaj kolizioneve            |
| Validim inputi         | Kontroll i fushave para procesimit              |
| Timeout               | 10 sekonda per lidhje socket                   |

---

## Logging

Të dy aplikacionet regjistrojnë automatikisht në skedar:

| Skedar           | Përmbajtja                                      |
|------------------|-------------------------------------------------|
| `server_log.txt` | Lidhjet, HMAC-et e marra, rezultatet e verifikimit |
| `client_log.txt` | Mesazhet e dërguara, HMAC-et e gjeneruara, përgjigjet |

**Shembull log entry:**
```
2024-11-15 14:32:01,123  [INFO]  Mesazh marrë | Teksti: 'Hello' | HMAC: a3f9c1b2e4d7...
2024-11-15 14:32:01,124  [INFO]  VERIFIKIM I SUKSESSHËM: Mesazhi është autentik.
```

---

## Trajtimi i Gabimeve

| Gabimi                       | Trajtimi                                         |
|------------------------------|--------------------------------------------------|
| Serveri nuk është aktiv      | Mesazh gabimi, klienti vazhdon                   |
| Timeout i lidhjes            | Mesazh gabimi, klienti vazhdon                   |
| JSON i pavlefshëm            | Server kthen `ERROR`, klienti shfaq mesazh       |
| HMAC nuk përputhet           | Server kthen `FAIL`, klienti tregon dështimin    |
| Mesazh bosh                  | Klienti refuzon para dërgimit                    |

---

## Librari të Përdorura

| Librari    | Qëllimi                                          |
|------------|--------------------------------------------------|
| `hmac`     | Gjenerim dhe verifikim i HMAC                   |
| `hashlib`  | Algoritmi hash SHA-256                          |
| `socket`   | Komunikim TCP mes klientit dhe serverit         |
| `json`     | Serialiizim/deserializim i paketave             |
| `logging`  | Regjistrim i ngjarjeve                          |
| `os`       | Lexim i environment variables                   |
| `datetime` | Timestamp-et e mesazheve                        |

---

*Projekt akademik — Siguria e të Dhënave*
