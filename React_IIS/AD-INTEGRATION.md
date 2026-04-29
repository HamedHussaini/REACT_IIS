# Active Directory Integrasjon
## REACT_IIS — Backend til AD

---

## Oversikt

Når en støttehenvendelse er sendt inn, kan en admin klikke en knapp for å opprette en AD-bruker direkte fra nettappen. Flyten er:

```
React (AdminPage) → POST /api/support/:id/ad → Node (server.js) → Python (create_ad_user.py) → Active Directory
```

---

## Forutsetninger

- Windows Server med Active Directory Domain Services installert
- Domenekontroller kjører (f.eks. `WIN-E5HG3D1727L.bjornholt.local`)
- Python installert på serveren (`python --version` for å verifisere)
- Node.js installert på serveren

---

## Steg 1 — Finn AD-konfigurasjonsverdiene dine

Du trenger 4 verdier fra Active Directory-miljøet ditt:

### AD_SERVER
Det fulle vertsnavnet til domenekontrolleren din.

Kjør dette i PowerShell på DC-en:
```powershell
$env:COMPUTERNAME + "." + (Get-WmiObject Win32_ComputerSystem).Domain
```
Eksempel: `WIN-E5HG3D1727L.bjornholt.local`

### AD_USER
Adminkontoen som brukes til å opprette brukere. Format: `DOMENE\brukernavn`

Finn den i: **Server Manager → Verktøy → Active Directory Users and Computers → Users**

Eksempel: `bjornholt\administrator`

### AD_PASS
Passordet til adminkontoen ovenfor.

### BASE_DN
Den organisasjonsenheten (OU) der nye brukere opprettes.

**Alternativ A — GUI:**
1. Åpne **Active Directory Users and Computers**
2. Klikk **Vis → Avanserte funksjoner**
3. Høyreklikk OU-en (f.eks. `Brukere`) → **Egenskaper → Attributtredigering**
4. Kopier verdien for `distinguishedName`

**Alternativ B — PowerShell:**
```powershell
Get-ADOrganizationalUnit -Filter {Name -eq "Brukere"} | Select DistinguishedName
```

Eksempel: `OU=Brukere,DC=bjornholt,DC=local`

---

## Steg 2 — Opprett Python virtuelt miljø (venv)

Et virtuelt miljø er en isolert Python-installasjon for prosjektet ditt, slik at `ldap3` ikke kolliderer med andre Python-pakker på serveren.

Åpne PowerShell på serveren og kjør:

```powershell
# Naviger til prosjektmappen
cd C:\Users\Administrator\Documents\REACT_ISS-main

# Opprett det virtuelle miljøet
python -m venv .venv

# Installer ldap3-biblioteket i venv
.venv\Scripts\python.exe -m pip install ldap3

# Verifiser at det fungerte
.venv\Scripts\python.exe -c "import ldap3; print('ldap3 OK:', ldap3.__version__)"
```

Forventet utdata: `ldap3 OK: 2.9.1` (versjon kan variere)

---

## Steg 3 — Konfigurer create_ad_user.py

Åpne `server/create_ad_user.py` og fyll inn de riktige AD-verdiene fra Steg 1:

```python
AD_SERVER = 'WIN-E5HG3D1727L.bjornholt.local'
AD_USER   = 'bjornholt\\administrator'
AD_PASS   = 'DittAdminPassord'
BASE_DN   = 'OU=Brukere,DC=bjornholt,DC=local'
```

**Viktig:** Tilkoblingen må bruke LDAPS (port 636) for at passordendringer skal fungere.
Oppdater servertilkoblingslinjen:

```python
# Endre denne linjen:
server = Server(AD_SERVER, get_info=ALL)

# Til dette (LDAPS):
server = Server(AD_SERVER, port=636, use_ssl=True, get_info=ALL)
```

---

## Steg 4 — Konfigurer server.js

Åpne `server/server.js` og sjekk at Python-stien peker til venv-en din:

```js
const python = "C:\\Users\\Administrator\\Documents\\REACT_ISS-main\\.venv\\Scripts\\python.exe";
const script = path.join(__dirname, "create_ad_user.py");
```

Sjekk at:
- `python`-stien stemmer med der du opprettet venv i Steg 2
- `path` er importert øverst: `const path = require("path");`

---

## Steg 5 — Test Python-skriptet direkte

Før du tester gjennom Node, verifiser at skriptet fungerer på egenhånd:

```powershell
cd C:\Users\Administrator\Documents\REACT_ISS-main\server

.\..\venv\Scripts\python.exe create_ad_user.py --username testbruker1 --password Temp123!
```

Forventet utdata: `Bruker testbruker1 opprettet.`

Sjekk deretter i **Active Directory Users and Computers** at `testbruker1` vises i `Brukere`-OU-en.

---

## Steg 6 — Start backend

```powershell
cd C:\Users\Administrator\Documents\REACT_ISS-main\server
node server.js
```

Forventet utdata: `Server kjører på http://localhost:5000`

---

## Steg 7 — Test hele flyten via API

Bruk PowerShell til å sende en testforespørsel til AD-endepunktet:

```powershell
Invoke-RestMethod -Method POST `
  -Uri "http://localhost:5000/api/support/1/ad" `
  -ContentType "application/json" `
  -Body '{"username": "testbruker2", "name": "Test Bruker", "type": "elev"}'
```

Forventet svar:
```json
{ "message": "Bruker opprettet i AD", "output": "Bruker testbruker2 opprettet." }
```

---

## Steg 8 — Test fra React-adminpanelet

1. Start frontend: `cd client && npm start`
2. Logg inn som admin
3. Åpne en støttehenvendelse
4. Klikk **Opprett AD-bruker**
5. Sjekk Active Directory Users and Computers for den nye brukeren

---

## Feilsøking

| Feil | Årsak | Løsning |
|------|-------|---------|
| `No module named ldap3` | ldap3 ikke installert i venv | Gjør Steg 2 på nytt |
| `python.exe not found` | Feil sti i server.js | Sjekk at venv-stien stemmer med Steg 2 |
| `LDAP connection refused` | Feil AD_SERVER eller brannmur | Ping DC-en, sjekk port 389/636 |
| `unwillingToPerform` | Passordskriving krever LDAPS | Bytt til port 636 + `use_ssl=True` |
| `invalidCredentials` | Feil AD_USER eller AD_PASS | Verifiser innloggingsinfo fra Steg 1 |
| `noSuchObject` | BASE_DN OU finnes ikke | Opprett OU-en eller rett opp DN-en |
| `500 AD-feil` fra Node | Python-skriptet krasjet | Sjekk `stderr` i svaret |

---

## Filoversikt

| Fil | Formål |
|-----|--------|
| `server/server.js` | Express API — mottar forespørsel, kaller Python |
| `server/create_ad_user.py` | Kobler til AD via LDAP og oppretter brukeren |
| `.venv/` | Python virtuelt miljø med ldap3 installert |
