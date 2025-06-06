# REACT_IIS

# 💬 Supportportal – Fullstack-applikasjon med React, Node.js og SQLite

Dette prosjektet er en komplett webapplikasjon for håndtering av brukerstøttehenvendelser. Brukere kan sende inn problemer via et skjema, og administratorer kan se, oppdatere og løse henvendelsene. Systemet støtter også integrasjon med Active Directory via et Python-skript som oppretter brukere automatisk.

---

## 🧱 Teknologistack

- **Frontend:** React (Create React App)
- **Backend:** Node.js med Express
- **Database:** SQLite (lokal databasefil)
- **Ekstern integrasjon:** Python-skript for AD-brukeropprettelse

---

## 📸 Funksjoner

- Brukere kan sende inn tekniske problemer via et brukervennlig skjema
- Administratorer kan autentisere med brukernavn og passord for å se henvendelser
- Status på henvendelser kan oppdateres (markeres som løst/uløst)
- Automatisk brukeropprettelse i Active Directory via Python-skript

---

## 📂 Prosjektstruktur
REACT_IIS/
│
├── client/                 # React frontend
│   ├── public/
│   └── src/
│       └── Homepage.jsx    # Hovedkomponent
│
├── server/                 # Node.js backend
│   ├── server.js           # Express-server
│   ├── support.db          # SQLite database
│   └── create_ad_user.py   # Python-skript for AD-brukeropprettelse
│
└── README.md


## 🚀 Installasjon

### 1. Klon prosjektet

```bash
git clone https://github.com/ditt-brukernavn/supportportal.git
cd REACT_IIS

###2. Kjøre backend
cd server
node server.js


### 3. start frontend
cd ../client
npm start
