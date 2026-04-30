# Endringer i prosjektet — Workshop

Dette dokumentet beskriver alle endringer som er gjort på prosjektet siden startversjonen.

---

## 1. Nye filer (skal opprettes)

### Python-scripts (i `server/`)

| Fil | Funksjon |
|-----|---------|
| `get_ad_users.py` | Henter alle AD-brukere som JSON |
| `toggle_ad_user.py` | Aktiverer / deaktiverer AD-bruker |
| `reset_ad_password.py` | Tilbakestiller passord (krever LDAPS port 636) |
| `move_ad_user.py` | Flytter bruker til annen OU |

### React-sider (i `client/src/`)

| Fil | Funksjon |
|-----|---------|
| `dashboard/DashboardPage.jsx` | Statistikkort + siste 5 henvendelser |
| `profil/ProfilPage.jsx` | Adminprofil med avatar (initialer) og redigeringsskjema |
| `adbrukere/ADBrukerePage.jsx` | AD-brukerliste med søk, deaktiver, reset, flytt, slett |

---

## 2. Endringer i eksisterende filer

### `server/server.js`

**Nye endepunkter:**
- `DELETE /api/support/:id` — slett henvendelse
- `PUT /api/support/:id` — rediger henvendelse
- `GET /api/dashboard` — statistikk + siste 5 henvendelser
- `GET /api/profil` — hent admin-profil
- `PUT /api/profil` — oppdater admin-profil
- `GET /api/ad/brukere` — hent alle AD-brukere
- `PUT /api/ad/brukere/:username/toggle` — aktiver/deaktiver
- `PUT /api/ad/brukere/:username/passord` — reset passord
- `PUT /api/ad/brukere/:username/flytt` — flytt OU
- `DELETE /api/ad/brukere/:username` — slett AD-bruker

**Nye database-tabeller:**
- `profiler` — lagrer admin-profilinfo (navn, e-post, rolle)

**Ny hjelpefunksjon:**
- `kjorPython(scriptNavn, args, res, onSuccess)` — gjenbrukbar funksjon for å kalle Python-scripts

---

### `client/src/App.js`

**Endringer:**
- Importerer 3 nye sider (Dashboard, Profil, ADBrukere)
- Lagt til 3 nye ruter
- Flyttet `<NavMenu />` ut av `<Container>` så navbaren er full bredde
- Lagt til `<Footer />`-komponent som vises kun på hjemmesiden (`location.pathname === "/"`)

---

### `client/src/shared/NavMenu.jsx`

**Endringer:**
- Mørk navbar (`bg="dark" variant="dark"`)
- Wrappet innholdet i `<Container>` så det aligner med sideinnholdet
- Bruker `<Link>` (react-router) i stedet for `href` på alle lenker
- Admin-elementer flyttet inn i en `NavDropdown`
- "Min profil" lagt til høyre side

---

### `client/src/home/HomePage.jsx`

**Endringer:**
- Hero-seksjon med blå gradient og to call-to-action-knapper
- 3 kort som lenker til Support, AD-brukere og Dashboard

---

### `client/src/admin/AdminPage.jsx`

**Endringer:**
- `<Form onSubmit>` så Enter fungerer for innlogging
- Sentrert login-skjema med tittel og hjelpetekst
- Statistikk-badges øverst (Totalt / Løste / Uløste)
- Søkefelt — filtrerer på navn, e-post, problemtype
- Mørk tabell-header
- Badge på status og problemtype
- **Slett-knapp** med bekreftelsesmodal på hver rad
- "Oppdater"-knapp øverst

---

## 3. Viktige tekniske detaljer

### LDAPS (port 636)
For at passord-reset skal fungere må serveren bruke LDAPS:
```python
server = Server(AD_SERVER, port=636, use_ssl=True, get_info=ALL)
```

### Python venv-sti i server.js
```js
const PYTHON = "C:\\Users\\Administrator\\Documents\\REACT_ISS-main\\.venv\\Scripts\\python.exe";
```

### AD-konfigurasjon (i alle Python-scripts)
```python
AD_SERVER = 'GORA.Bjornholt.local'
AD_USER   = 'bjornholt\\administrator'
AD_PASS   = 'Admin123'
BASE_DN   = 'OU=TECH,OU=HR,OU=Bjornholt,DC=Bjornholt,DC=local'
```

---

## 4. Slik tar du i bruk endringene

### Steg 1 — Backend
```powershell
cd server
npm install
node server.js
```

### Steg 2 — Python venv
```powershell
cd ..
python -m venv .venv
.venv\Scripts\python.exe -m pip install ldap3
```

### Steg 3 — Frontend
```powershell
cd client
npm install
npm start
```

### Steg 4 — Test
1. Åpne `http://localhost:3000`
2. Naviger til **Admin** → **Henvendelser** og logg inn med `admin` / `admin123`
3. Naviger til **Admin** → **AD-brukere** for å se AD-listen
4. Naviger til **Dashboard** for statistikk
5. Naviger til **Min profil** for å redigere profilen

---

## 5. Endepunkt-oversikt

| Metode | Endepunkt | Beskrivelse |
|--------|-----------|-------------|
| POST | `/api/support` | Ny henvendelse |
| GET | `/api/support` | Hent alle (Basic auth) |
| PUT | `/api/support/:id` | Rediger henvendelse |
| PUT | `/api/support/:id/resolve` | Marker løst |
| DELETE | `/api/support/:id` | Slett henvendelse |
| POST | `/api/support/:id/ad` | Opprett AD-bruker |
| GET | `/api/ad/brukere` | Hent alle AD-brukere |
| PUT | `/api/ad/brukere/:u/toggle` | Aktiver/deaktiver |
| PUT | `/api/ad/brukere/:u/passord` | Reset passord |
| PUT | `/api/ad/brukere/:u/flytt` | Flytt OU |
| DELETE | `/api/ad/brukere/:u` | Slett AD-bruker |
| GET | `/api/dashboard` | Statistikk |
| GET | `/api/profil` | Hent profil |
| PUT | `/api/profil` | Oppdater profil |

---

## 6. Filstruktur etter endringer

```
React_IIS/
├── client/
│   └── src/
│       ├── adbrukere/
│       │   └── ADBrukerePage.jsx        ← NY
│       ├── admin/
│       │   └── AdminPage.jsx            ← OPPDATERT
│       ├── dashboard/
│       │   └── DashboardPage.jsx        ← NY
│       ├── home/
│       │   └── HomePage.jsx             ← OPPDATERT
│       ├── profil/
│       │   └── ProfilPage.jsx           ← NY
│       ├── shared/
│       │   └── NavMenu.jsx              ← OPPDATERT
│       ├── support/
│       │   └── SupportPage.jsx          (uendret)
│       └── App.js                       ← OPPDATERT
└── server/
    ├── server.js                        ← OPPDATERT
    ├── create_ad_user.py                (uendret)
    ├── get_ad_users.py                  ← NY
    ├── toggle_ad_user.py                ← NY
    ├── reset_ad_password.py             ← NY
    └── move_ad_user.py                  ← NY
```

---

## 7. Feilsøking

| Problem | Løsning |
|---------|---------|
| `ldap3 not found` | `.venv\Scripts\python.exe -m pip install ldap3` |
| Reset passord feiler | LDAPS port 636 må være åpen på DC |
| AD-brukere viser tom liste | Sjekk `BASE_DN` i Python-scripts |
| Enter logger ikke inn | Sjekk at `<Form onSubmit>` er på plass |
| Footer på alle sider | `location.pathname !== "/"` returnerer null |
| Navbar ikke full bredde | Navbar må ligge **utenfor** `<Container>` i App.js |
