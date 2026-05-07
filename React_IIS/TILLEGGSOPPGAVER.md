# Tilleggsoppgaver — 1 dags økt (120 min)

Disse oppgavene kan gjøres på en hvilken som helst PC — du trenger **ikke** Active Directory eller domenetilkobling. Alt foregår i React og SQLite-databasen lokalt.

---

## Tidsplan (120 min)

| Tid | Aktivitet |
|-----|-----------|
| 0–10 min | Introduksjon — hva skal vi gjøre i dag |
| 10–20 min | Demonstrasjon av sluttresultatet |
| 20–100 min | Koding (eleven jobber selv) |
| 100–115 min | Test og feilsøking |
| 115–120 min | Oppsummering — vis hva du laget |

---

## Dagens tema: "Gjør AdminPage bedre"

I dag skal du forbedre `AdminPage.jsx` med 3 nye funksjoner. Du jobber **kun** med frontend (React) og kan teste alt lokalt uten AD.

---

## Oppgave 1 — Norsk dato (20 min)

### Mål
Lære hvordan vi formaterer datoer.

### Hva du skal gjøre
I `AdminPage.jsx` finner du datoen i tabellen. Bytt ut det stygge formatet med norsk dato.

**Før:** `2026-05-07T14:30:00`
**Etter:** `7. mai 2026 kl. 14:30`

### Hint
Bytt ut denne linjen:
```jsx
<td>{new Date(item.created_at).toLocaleDateString("nb-NO")}</td>
```

med:
```jsx
<td>
  {new Date(item.created_at).toLocaleString("nb-NO", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  })}
</td>
```

Test: gå til `AdminPage` og sjekk at datoene nå vises på norsk.

---

## Oppgave 2 — Filter på status (40 min)

### Mål
Lære å filtrere arrays og bruke React state.

### Hva du skal gjøre
Legg til 3 knapper over tabellen i `AdminPage.jsx`:
- **Alle** — viser alle henvendelser
- **Kun løste** — viser bare de som er løst
- **Kun uløste** — viser bare de som IKKE er løst

Når du klikker en knapp, skal tabellen oppdatere seg umiddelbart.

### Steg

**1. Legg til state øverst i komponenten:**
```jsx
const [statusFilter, setStatusFilter] = useState("alle");
```

**2. Oppdater `filtrert`-arrayen:**
```jsx
const filtrert = data.filter(item => {
  const matcherSok = item.name.toLowerCase().includes(sok.toLowerCase()) ||
                     item.email.toLowerCase().includes(sok.toLowerCase());

  const matcherStatus =
    statusFilter === "alle" ||
    (statusFilter === "loste" && item.is_resolved) ||
    (statusFilter === "uloste" && !item.is_resolved);

  return matcherSok && matcherStatus;
});
```

**3. Legg til knappene over tabellen:**
```jsx
<div className="mb-3">
  <Button
    variant={statusFilter === "alle" ? "primary" : "outline-primary"}
    onClick={() => setStatusFilter("alle")}
    className="me-2"
  >
    Alle
  </Button>
  <Button
    variant={statusFilter === "loste" ? "success" : "outline-success"}
    onClick={() => setStatusFilter("loste")}
    className="me-2"
  >
    Kun løste
  </Button>
  <Button
    variant={statusFilter === "uloste" ? "danger" : "outline-danger"}
    onClick={() => setStatusFilter("uloste")}
  >
    Kun uløste
  </Button>
</div>
```

### Test
1. Send inn 2-3 henvendelser fra `SupportPage`
2. Marker en av dem som løst
3. Sjekk at filterknappene fungerer

---

## Oppgave 3 — Last ned CSV (40 min)

### Mål
Lære å generere filer i nettleseren.

### Hva du skal gjøre
Legg til en knapp **"Last ned CSV"** i `AdminPage.jsx`. Når du klikker den, lastes en CSV-fil med alle henvendelsene ned. Filen kan åpnes i Excel.

### Steg

**1. Lag en funksjon i AdminPage:**
```jsx
const lastNedCSV = () => {
  const headers = ["Navn", "E-post", "Type", "Beskrivelse", "Status", "Dato"];

  const rader = data.map(d => [
    d.name,
    d.email,
    d.problem_type,
    d.description.replace(/;/g, ","),  // bytt ut ; så CSV ikke ødelegges
    d.is_resolved ? "Løst" : "Uløst",
    new Date(d.created_at).toLocaleDateString("nb-NO")
  ]);

  const csv = [headers, ...rader]
    .map(r => r.join(";"))
    .join("\n");

  const blob = new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `henvendelser_${new Date().toISOString().slice(0,10)}.csv`;
  a.click();
};
```

**2. Legg til knappen øverst på siden:**
```jsx
<Button variant="outline-success" onClick={lastNedCSV}>
  📥 Last ned CSV
</Button>
```

### Test
1. Klikk knappen
2. Åpne filen som lastes ned i Excel
3. Sjekk at alle kolonner ser riktige ut og at norske tegn (æ ø å) vises korrekt

---

## Bonus (hvis du blir ferdig tidlig)

### Bonus 1 — Tegnteller
I `SupportPage.jsx`, vis "X/500 tegn" under beskrivelsesfeltet:
```jsx
<Form.Text>{form.description.length}/500 tegn</Form.Text>
```

### Bonus 2 — Bekreftelse før innsending
I `SupportPage.jsx`, vis en bekreftelsesdialog (`window.confirm`) før skjemaet sendes inn:
```jsx
const handleSubmit = async (e) => {
  e.preventDefault();
  if (!window.confirm("Er du sikker på at du vil sende denne henvendelsen?")) return;
  // ... resten av koden
};
```

### Bonus 3 — Tøm filter-knapp
Legg til en knapp som nullstiller alle filtere på én gang:
```jsx
<Button variant="link" onClick={() => { setSok(""); setStatusFilter("alle"); }}>
  Tøm alle filtere
</Button>
```

---

## Hva du skal kunne ved slutten av økten

✅ Forstå hvordan React state fungerer (`useState`)
✅ Filtrere en array basert på flere betingelser
✅ Formatere datoer på norsk
✅ Generere og laste ned filer i nettleseren
✅ Lage knapper som endrer hva som vises på skjermen

---

## Tips

- **Test ofte** — etter hver liten endring, refresh nettleseren
- **Bruk `console.log`** for å sjekke hva variabler inneholder
- **Les feilmeldinger** — de forteller deg hvor problemet er
- **Spør hvis du står fast** — men prøv 10 minutter selv først

---


