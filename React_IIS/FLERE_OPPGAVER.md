# Flere tilleggsoppgaver — 120 min økter

Her er flere oppgaver elevene kan jobbe med. Hver økt er på 120 min og krever **ikke** Active Directory eller domenetilkobling — alt fungerer lokalt på en hvilken som helst PC.

Velg én økt per dag basert på hva elevene har lyst til å lære.

---

## Tidsplan (samme for hver økt)

| Tid | Aktivitet |
|-----|-----------|
| 0–10 min | Introduksjon |
| 10–20 min | Demonstrasjon |
| 20–100 min | Egen koding |
| 100–115 min | Test og feilsøking |
| 115–120 min | Oppsummering |

---

## Økt A — "Forbedre SupportPage" (120 min)

### Tema: Skjemaforbedringer og brukervennlighet

### Oppgave A1 — Tegnteller (20 min)
I `SupportPage.jsx`, vis "X/500 tegn" under beskrivelsesfeltet.

```jsx
<Form.Text className={form.description.length > 450 ? "text-danger" : "text-muted"}>
  {form.description.length}/500 tegn
</Form.Text>
```

### Oppgave A2 — Dropdown for problemtype (40 min)
Bytt ut tekstfeltet for "Problemtype" med en dropdown.

**Steg 1 — endre i SupportPage:**
```jsx
<Form.Group className="mb-3">
  <Form.Label>Problemtype</Form.Label>
  <Form.Select name="problem_type" value={form.problem_type} onChange={handleChange} required>
    <option value="">Velg problemtype...</option>
    <option value="Glemt passord">Glemt passord</option>
    <option value="Ny bruker">Ny bruker</option>
    <option value="Programvare">Programvare</option>
    <option value="Hardware">Hardware</option>
    <option value="Nettverk">Nettverk</option>
    <option value="Annet">Annet</option>
  </Form.Select>
</Form.Group>
```

### Oppgave A3 — Suksess-dialog (40 min)
Når en henvendelse er sendt inn, vis en stor grønn boks med en "Send ny"-knapp i stedet for kun en alert.

```jsx
{submitted ? (
  <Card className="text-center p-5 mt-3">
    <h3>✅ Takk for henvendelsen!</h3>
    <p>Vi tar kontakt med deg så snart som mulig.</p>
    <Button onClick={() => setSubmitted(false)}>Send ny henvendelse</Button>
  </Card>
) : (
  <Form>...</Form>
)}
```

---

## Økt B — "Forbedre Dashboard" (120 min)

### Tema: Vis mer informasjon og statistikk

### Oppgave B1 — Vis prosent løste (30 min)
Legg til et nytt kort som viser prosent løste henvendelser.

```jsx
const prosent = data.totalt > 0
  ? Math.round((data.loste / data.totalt) * 100)
  : 0;
```

```jsx
<Col md={3}>
  <Card className="text-center border-info shadow-sm">
    <Card.Body>
      <Card.Title>Løsningsrate</Card.Title>
      <h1 className="display-4 text-info">{prosent}%</h1>
      <Card.Text>Av alle henvendelser</Card.Text>
    </Card.Body>
  </Card>
</Col>
```

### Oppgave B2 — Henvendelser denne uken (45 min)
Lag et nytt kort som viser hvor mange henvendelser som har kommet inn denne uken.

**Backend (server.js):** Legg til i `/api/dashboard`-endepunktet:
```js
db.get(
  `SELECT COUNT(*) AS denneUken FROM support_requests
   WHERE created_at >= datetime('now', '-7 days')`,
  (err, row) => { /* ... */ }
);
```

**Frontend:** Vis det i dashboard som et nytt kort.

### Oppgave B3 — Topp 3 problemtyper (45 min)
Vis hvilke 3 problemtyper som er mest vanlige.

**Backend:**
```js
db.all(
  `SELECT problem_type, COUNT(*) AS antall
   FROM support_requests
   GROUP BY problem_type
   ORDER BY antall DESC LIMIT 3`,
  (err, rows) => { /* ... */ }
);
```

**Frontend:**
```jsx
<Card>
  <Card.Header>Topp 3 problemtyper</Card.Header>
  <Card.Body>
    {data.toppTyper?.map((t, i) => (
      <div key={i} className="d-flex justify-content-between mb-2">
        <span>{i + 1}. {t.problem_type}</span>
        <Badge bg="primary">{t.antall}</Badge>
      </div>
    ))}
  </Card.Body>
</Card>
```

---

## Økt C — "Rediger henvendelser" (120 min)

### Tema: Full CRUD-funksjonalitet på AdminPage

### Oppgave C1 — Rediger-knapp + modal (60 min)
Legg til en "Rediger"-knapp på hver rad i `AdminPage`. Knappen åpner en modal med skjemaet forhåndsutfylt.

```jsx
const [visRedigerModal, setVisRedigerModal] = useState(false);
const [redigert, setRedigert] = useState(null);

const apneRedigerModal = (item) => {
  setRedigert({ ...item });
  setVisRedigerModal(true);
};

// I tabellen:
<Button size="sm" variant="outline-info" onClick={() => apneRedigerModal(item)}>
  Rediger
</Button>

// Nederst i komponenten:
<Modal show={visRedigerModal} onHide={() => setVisRedigerModal(false)} centered>
  <Modal.Header closeButton>
    <Modal.Title>Rediger henvendelse</Modal.Title>
  </Modal.Header>
  <Modal.Body>
    <Form.Group className="mb-3">
      <Form.Label>Navn</Form.Label>
      <Form.Control
        value={redigert?.name || ""}
        onChange={(e) => setRedigert({ ...redigert, name: e.target.value })}
      />
    </Form.Group>
    {/* Lag tilsvarende for email, problem_type, description */}
  </Modal.Body>
  <Modal.Footer>
    <Button variant="secondary" onClick={() => setVisRedigerModal(false)}>Avbryt</Button>
    <Button variant="primary" onClick={lagreEndringer}>Lagre</Button>
  </Modal.Footer>
</Modal>
```

### Oppgave C2 — Send PUT til backend (60 min)
Lagre endringene i databasen via PUT-endepunktet (som finnes i server.js).

```jsx
const lagreEndringer = async () => {
  const res = await fetch(`http://localhost:5000/api/support/${redigert.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(redigert),
  });

  if (res.ok) {
    setData(prev => prev.map(d => d.id === redigert.id ? redigert : d));
    setVisRedigerModal(false);
    setMelding("Henvendelse oppdatert!");
  }
};
```

---

## Økt D — "Sortering på tabell" (120 min)

### Tema: Klikkbare kolonner og sortering

### Oppgave D1 — Sorter på navn (40 min)
Klikk på "Navn"-overskriften for å sortere alfabetisk.

```jsx
const [sortBy, setSortBy] = useState(null);
const [sortOrder, setSortOrder] = useState("asc");

const sorter = (felt) => {
  if (sortBy === felt) {
    setSortOrder(sortOrder === "asc" ? "desc" : "asc");
  } else {
    setSortBy(felt);
    setSortOrder("asc");
  }
};

const sortert = sortBy ? [...filtrert].sort((a, b) => {
  if (sortOrder === "asc") return a[sortBy] > b[sortBy] ? 1 : -1;
  return a[sortBy] < b[sortBy] ? 1 : -1;
}) : filtrert;
```

```jsx
<th style={{ cursor: "pointer" }} onClick={() => sorter("name")}>
  Navn {sortBy === "name" && (sortOrder === "asc" ? "▲" : "▼")}
</th>
```

### Oppgave D2 — Sorter på flere felt (40 min)
Gjør det samme for "E-post", "Type" og "Dato".

### Oppgave D3 — Visuell tilbakemelding (40 min)
Når en kolonne er aktiv, vis den med fet skrift eller annen bakgrunnsfarge.

```jsx
<th
  style={{ cursor: "pointer", backgroundColor: sortBy === "name" ? "#0d6efd" : "" }}
  onClick={() => sorter("name")}
>
  Navn {sortBy === "name" && (sortOrder === "asc" ? "▲" : "▼")}
</th>
```

---

## Økt E — "Validering på skjema" (120 min)

### Tema: Brukervennlig feilhåndtering

### Oppgave E1 — Inline-validering (60 min)
I `SupportPage.jsx`, sjekk hvert felt mens brukeren skriver:

- **Navn** — minst 3 tegn
- **E-post** — må inneholde @ og .
- **Beskrivelse** — minst 20 tegn

```jsx
const erGyldig = {
  name: form.name.length >= 3,
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email),
  description: form.description.length >= 20,
};

<Form.Control
  name="name"
  value={form.name}
  onChange={handleChange}
  isValid={form.name.length > 0 && erGyldig.name}
  isInvalid={form.name.length > 0 && !erGyldig.name}
/>
<Form.Control.Feedback type="invalid">
  Navn må være minst 3 tegn
</Form.Control.Feedback>
```

### Oppgave E2 — Send-knapp deaktivert (30 min)
Knappen skal være deaktivert hvis noe er ugyldig:

```jsx
<Button
  type="submit"
  disabled={!Object.values(erGyldig).every(v => v)}
>
  Send henvendelse
</Button>
```

### Oppgave E3 — Vis sammendrag av feil (30 min)
Vis en boks øverst som lister opp alle feil:

```jsx
{Object.values(erGyldig).some(v => !v) && (
  <Alert variant="warning">
    <strong>Vennligst rett opp:</strong>
    <ul className="mb-0">
      {!erGyldig.name && <li>Navn må være minst 3 tegn</li>}
      {!erGyldig.email && <li>E-post må være gyldig</li>}
      {!erGyldig.description && <li>Beskrivelse må være minst 20 tegn</li>}
    </ul>
  </Alert>
)}
```

---

## Økt F — "Toast-notifikasjoner" (120 min)

### Tema: Bytt ut Alert med Toast

### Oppgave F1 — Lag en gjenbrukbar Toast-komponent (60 min)
Lag en ny fil `client/src/shared/ToastMelding.jsx`:

```jsx
import React from "react";
import { Toast, ToastContainer } from "react-bootstrap";

export default function ToastMelding({ vis, melding, type, onClose }) {
  return (
    <ToastContainer position="top-end" className="p-3" style={{ zIndex: 9999 }}>
      <Toast show={vis} onClose={onClose} delay={3000} autohide bg={type}>
        <Toast.Header>
          <strong className="me-auto">
            {type === "success" ? "✅ Suksess" : type === "danger" ? "❌ Feil" : "ℹ️ Info"}
          </strong>
        </Toast.Header>
        <Toast.Body className="text-white">{melding}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}
```

### Oppgave F2 — Bruk i AdminPage (60 min)
Bytt ut alle `setMelding("...")` med toast:

```jsx
const [toast, setToast] = useState({ vis: false, melding: "", type: "success" });

const visToast = (melding, type = "success") => {
  setToast({ vis: true, melding, type });
};

// Bruk:
visToast("Henvendelse slettet!", "success");
visToast("Noe gikk galt", "danger");

// Render nederst:
<ToastMelding
  vis={toast.vis}
  melding={toast.melding}
  type={toast.type}
  onClose={() => setToast({ ...toast, vis: false })}
/>
```

---

## Økt G — "Detaljside for henvendelse" (120 min)

### Tema: React Router og dynamiske ruter

### Oppgave G1 — Lag DetaljPage (60 min)
Lag en ny fil `client/src/admin/DetaljPage.jsx` som viser én henvendelse i full størrelse.

```jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Container, Card, Button, Badge } from "react-bootstrap";

export default function DetaljPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [henvendelse, setHenvendelse] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/api/support/${id}`)
      .then(res => res.json())
      .then(setHenvendelse);
  }, [id]);

  if (!henvendelse) return <Container>Laster...</Container>;

  return (
    <Container className="mt-4">
      <Button variant="link" onClick={() => navigate(-1)}>← Tilbake</Button>
      <Card className="mt-3">
        <Card.Header>
          <h3>{henvendelse.name}</h3>
          <Badge bg="info">{henvendelse.problem_type}</Badge>
        </Card.Header>
        <Card.Body>
          <p><strong>E-post:</strong> {henvendelse.email}</p>
          <p><strong>Beskrivelse:</strong></p>
          <p>{henvendelse.description}</p>
          <hr />
          <small className="text-muted">
            Mottatt: {new Date(henvendelse.created_at).toLocaleString("nb-NO")}
          </small>
        </Card.Body>
      </Card>
    </Container>
  );
}
```

### Oppgave G2 — Legg til ny rute (30 min)
I `App.js`:
```jsx
import DetaljPage from './admin/DetaljPage';
<Route path="/henvendelse/:id" element={<DetaljPage />} />
```

### Oppgave G3 — "Vis detaljer"-knapp (30 min)
I `AdminPage`, legg til en knapp som navigerer til detaljsiden:

```jsx
import { useNavigate } from "react-router-dom";
const navigate = useNavigate();

<Button size="sm" onClick={() => navigate(`/henvendelse/${item.id}`)}>
  Detaljer
</Button>
```

**Backend-tip:** Du må også legge til `GET /api/support/:id` i server.js for å hente én henvendelse:
```js
app.get("/api/support/:id", (req, res) => {
  db.get(`SELECT * FROM support_requests WHERE id = ?`, [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: "DB-feil" });
    res.json(row);
  });
});
```

