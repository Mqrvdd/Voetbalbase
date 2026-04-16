# ⚽ VoetbalBase

VoetbalBase is een webapplicatie voor het beheren en bekijken van spelers, clubs en contracten.

De applicatie kent twee rollen:
- Gebruikers → kunnen registreren, inloggen en data bekijken
- Admin → beheert alle data via een aparte admin-omgeving

---

## Functionaliteit

Gebruikers:
- Registreren met e-mail en wachtwoord (incl. wachtwoord bevestiging)
- Inloggen en uitloggen
- Spelers bekijken
- Clubs bekijken
- Contracten bekijken
- Zoeken op spelernaam
- Filteren op nationaliteit

Admin:
- Inloggen via aparte URL (/admin/login)
- Dashboard met totalen
- Gebruikers beheren (CRUD)
- Spelers beheren (CRUD)
- Clubs beheren (CRUD)
- Contracten beheren (CRUD)

Algemeen:
- Wachtwoorden gehasht met bcrypt
- CSRF-bescherming via Flask-WTF
- SQLite database (automatisch aangemaakt)
- Seed met standaard clubs + admin
- Moderne UI met Bootstrap 5
- Responsief design

---

## Vereisten

- Python 3.8 of hoger
- pip

---

## Installatie

1. Ga naar de projectmap:
cd Voetbalbase

2. Maak een virtuele omgeving:
python -m venv venv

3. Activeer de omgeving:

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

4. Installeer dependencies:
pip install -r requirements.txt

5. Start de applicatie:
python app.py

De applicatie draait op:
http://127.0.0.1:5000

---

## Rollen & Toegang

Gebruiker:
- /register
- /login

Kan:
- data bekijken
- zoeken en filteren

Kan niet:
- data aanpassen

Admin:

Login via:
http://127.0.0.1:5000/admin/login

Standaard admin account:
E-mail: admin@voetbalbase.nl
Wachtwoord: Admin123!

Admin heeft toegang tot:
- /admin
- /admin/users
- /admin/spelers
- /admin/clubs
- /admin/contracten

---

## Gebruik

Registreren:
1. Ga naar /register
2. Vul e-mail in
3. Vul wachtwoord in
4. Herhaal wachtwoord
5. Klik op registreren

Inloggen gebruiker:
1. Ga naar /login
2. Log in
3. Je komt op het overzicht

Inloggen admin:
1. Ga naar /admin/login
2. Log in
3. Je komt op het dashboard

---

## Beheerfunctionaliteit

Gebruikers:
- Aanmaken
- Bewerken
- Verwijderen
- Adminrechten toekennen

Spelers:
- Aanmaken
- Bewerken
- Verwijderen

Clubs:
- Aanmaken
- Bewerken
- Verwijderen

Contracten:
- Speler koppelen aan club
- Positie vastleggen
- Rugnummer instellen
- Bewerken en verwijderen

---

## Zoeken & Filtering

Op de spelerspagina:
- Zoeken op naam
- Filteren op nationaliteit

---

## Configuratie

Database: SQLite (database.db)
Poort: 5000
Debug: Aan
Seed: Clubs + admin

---

## Technologie Stack

- Python
- Flask
- SQLAlchemy
- Flask-WTF
- Flask-Migrate
- WTForms
- bcrypt
- Bootstrap 5
- Jinja2
- SQLite

---

## Security

- Wachtwoorden gehasht met bcrypt
- CSRF-protectie actief
- Sessies beveiligd met secret key
- SQLAlchemy voorkomt SQL injection
- Admin routes afgeschermd

---

## Database

- SQLite (database.db)
- Wordt automatisch aangemaakt
- Wordt gevuld met:
  - standaard clubs
  - admin account

---

## Structuur

VoetbalBase/
│
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── landing.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── admin_login.html
│   │   ├── home.html
│   │   ├── spelers.html
│   │   ├── speler_detail.html
│   │   ├── clubs.html
│   │   ├── contracten.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_users.html
│   │   ├── admin_user_form.html
│   │   ├── admin_spelers.html
│   │   ├── admin_speler_form.html
│   │   ├── admin_clubs.html
│   │   ├── admin_club_form.html
│   │   ├── admin_contracten.html
│   │   └── admin_contract_form.html
│
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   └── views.py
│
├── app.py
├── config.py
├── database.db
├── requirements.txt
└── README.md

---

## Licentie

MIT License