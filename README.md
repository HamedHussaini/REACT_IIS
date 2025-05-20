# REACT_ISS

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
supportportal/
├── client/ # React-frontend
│ └── src/
│ └── Homepage.jsx # Startsiden
├── server/ # Node.js-backend
│ ├── server.js # Hovedserverfil
│ ├── support.db # SQLite databasefil (opprettes automatisk)
│ └── create_ad_user.py # Python-skript for AD-brukere
└── README.md

## 🚀 Installasjon

### 1. Klon prosjektet

```bash
git clone https://github.com/ditt-brukernavn/supportportal.git
cd supportportal

###2. Installer backend

```bash
cd server
npm install
node server.js

### 3. Installer og start frontend
```bash
cd ../client
npm install
npm start
