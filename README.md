# ⚽ VoetbalBase

---

## Functionaliteit

* Registreren / inloggen
* Spelers CRUD + zoeken
* Clubs CRUD (incl. vooraf ingevulde clubs)
* Contracten CRUD (koppeling speler ↔ club)
* Filteren op club
* Beveiliging via login_required

---

## Tech

* Python / Flask
* Flask-SQLAlchemy
* Flask-WTF
* Flask-Migrate
* bcrypt
* SQLite
* Bootstrap

---

## Installatie

```bash
pip install -r requirements.txt
```

---

## Runnen

```bash
python app.py
```

App draait op:

```
http://127.0.0.1:5000
```

---

## Database

* SQLite (`database.db`)
* Wordt automatisch aangemaakt
* Seed met clubs bij eerste start

---

## Structuur

```
VoetbalBase/
│
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── spelers.html
│   │   ├── speler_form.html
│   │   ├── clubs.html
│   │   ├── club_form.html
│   │   ├── contracten.html
│   │   ├── contract_form.html
│   │   ├── login.html
│   │   └── register.html
│   │
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
```



