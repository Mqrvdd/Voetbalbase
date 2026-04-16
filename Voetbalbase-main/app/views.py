from functools import wraps
import bcrypt

from flask import Blueprint, render_template, redirect, session, url_for, flash, request

from . import db
from .models import User, Speler, Club, Contract
from .forms import RegisterForm, LoginForm, SpelerForm, ClubForm, ContractForm

bp = Blueprint("main", __name__)

POSITIES = [
    "Doelman",
    "Centrale verdediger",
    "Linker verdediger",
    "Rechter verdediger",
    "Wingback links",
    "Wingback rechts",
    "Verdedigende middenvelder",
    "Centrale middenvelder",
    "Aanvallende middenvelder",
    "Linksbuiten",
    "Rechtsbuiten",
    "Spits",
    "Schaduwspits"
]


def is_ingelogd():
    return "user_id" in session


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not is_ingelogd():
            flash("Log eerst in om deze actie uit te voeren.", "warning")
            return redirect(url_for("main.login"))
        return view_func(*args, **kwargs)
    return wrapped_view


@bp.route("/")
def home():
    return render_template("home.html", ingelogd=is_ingelogd())


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        bestaand = User.query.filter_by(email=form.email.data).first()
        if bestaand:
            flash("Dit e-mailadres bestaat al.", "danger")
            return render_template("register.html", form=form, ingelogd=is_ingelogd())

        hashed_password = bcrypt.hashpw(
            form.password.data.encode("utf-8"),
            bcrypt.gensalt()
        )

        user = User(email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account aangemaakt! Je kunt nu inloggen.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form, ingelogd=is_ingelogd())


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.checkpw(
            form.password.data.encode("utf-8"),
            user.password_hash
        ):
            session["user_id"] = user.id
            flash("Je bent ingelogd.", "success")
            return redirect(url_for("main.home"))

        flash("Ongeldige inloggegevens.", "danger")

    return render_template("login.html", form=form, ingelogd=is_ingelogd())


@bp.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("main.home"))


@bp.route("/spelers")
def spelers():
    zoekterm = request.args.get("q", "")

    if zoekterm:
        spelers = Speler.query.filter(
            Speler.naam.ilike(f"%{zoekterm}%")
        ).order_by(Speler.naam.asc()).all()
    else:
        spelers = Speler.query.order_by(Speler.naam.asc()).all()

    return render_template(
        "spelers.html",
        spelers=spelers,
        ingelogd=is_ingelogd(),
        zoekterm=zoekterm
    )


@bp.route("/spelers/toevoegen", methods=["GET", "POST"])
@login_required
def speler_toevoegen():
    form = SpelerForm()

    if form.validate_on_submit():
        speler = Speler(
            naam=form.naam.data,
            leeftijd=form.leeftijd.data,
            nationaliteit=form.nationaliteit.data
        )
        db.session.add(speler)
        db.session.commit()
        flash("Speler toegevoegd.", "success")
        return redirect(url_for("main.spelers"))

    return render_template(
        "speler_form.html",
        form=form,
        titel="Speler toevoegen",
        ingelogd=is_ingelogd()
    )


@bp.route("/spelers/bewerken/<int:speler_id>", methods=["GET", "POST"])
@login_required
def speler_bewerken(speler_id):
    speler = Speler.query.get_or_404(speler_id)
    form = SpelerForm(obj=speler)

    if form.validate_on_submit():
        speler.naam = form.naam.data
        speler.leeftijd = form.leeftijd.data
        speler.nationaliteit = form.nationaliteit.data
        db.session.commit()
        flash("Speler bijgewerkt.", "success")
        return redirect(url_for("main.spelers"))

    return render_template(
        "speler_form.html",
        form=form,
        titel="Speler bewerken",
        ingelogd=is_ingelogd()
    )


@bp.route("/spelers/verwijderen/<int:speler_id>", methods=["POST"])
@login_required
def speler_verwijderen(speler_id):
    speler = Speler.query.get_or_404(speler_id)
    db.session.delete(speler)
    db.session.commit()
    flash("Speler verwijderd.", "info")
    return redirect(url_for("main.spelers"))


@bp.route("/clubs")
def clubs():
    clubs = Club.query.order_by(Club.naam.asc()).all()
    return render_template("clubs.html", clubs=clubs, ingelogd=is_ingelogd())


@bp.route("/clubs/toevoegen", methods=["GET", "POST"])
@login_required
def club_toevoegen():
    form = ClubForm()

    if form.validate_on_submit():
        bestaand = Club.query.filter_by(naam=form.naam.data).first()
        if bestaand:
            flash("Deze club bestaat al.", "danger")
            return render_template(
                "club_form.html",
                form=form,
                titel="Club toevoegen",
                ingelogd=is_ingelogd()
            )

        club = Club(
            naam=form.naam.data,
            land=form.land.data
        )
        db.session.add(club)
        db.session.commit()
        flash("Club toegevoegd.", "success")
        return redirect(url_for("main.clubs"))

    return render_template(
        "club_form.html",
        form=form,
        titel="Club toevoegen",
        ingelogd=is_ingelogd()
    )


@bp.route("/clubs/bewerken/<int:club_id>", methods=["GET", "POST"])
@login_required
def club_bewerken(club_id):
    club = Club.query.get_or_404(club_id)
    form = ClubForm(obj=club)

    if form.validate_on_submit():
        club.naam = form.naam.data
        club.land = form.land.data
        db.session.commit()
        flash("Club bijgewerkt.", "success")
        return redirect(url_for("main.clubs"))

    return render_template(
        "club_form.html",
        form=form,
        titel="Club bewerken",
        ingelogd=is_ingelogd()
    )


@bp.route("/clubs/verwijderen/<int:club_id>", methods=["POST"])
@login_required
def club_verwijderen(club_id):
    club = Club.query.get_or_404(club_id)
    db.session.delete(club)
    db.session.commit()
    flash("Club verwijderd.", "info")
    return redirect(url_for("main.clubs"))


@bp.route("/contracten")
def contracten():
    contracten = Contract.query.order_by(Contract.id.desc()).all()
    clubs = Club.query.order_by(Club.naam.asc()).all()
    filter_club = request.args.get("club", "")

    if filter_club:
        contracten = Contract.query.join(Club).filter(
            Club.naam == filter_club
        ).order_by(Contract.id.desc()).all()

    return render_template(
        "contracten.html",
        contracten=contracten,
        clubs=clubs,
        filter_club=filter_club,
        ingelogd=is_ingelogd()
    )


@bp.route("/contracten/toevoegen", methods=["GET", "POST"])
@login_required
def contract_toevoegen():
    form = ContractForm()

    spelers = Speler.query.order_by(Speler.naam.asc()).all()
    clubs = Club.query.order_by(Club.naam.asc()).all()

    if form.validate_on_submit():
        speler = Speler.query.filter_by(naam=form.speler_naam.data).first()
        club = Club.query.filter_by(naam=form.club_naam.data).first()

        if not speler:
            flash("De gekozen speler bestaat niet.", "danger")
            return render_template(
                "contract_form.html",
                form=form,
                titel="Contract toevoegen",
                spelers=spelers,
                clubs=clubs,
                posities=POSITIES,
                ingelogd=is_ingelogd()
            )

        if not club:
            flash("De gekozen club bestaat niet.", "danger")
            return render_template(
                "contract_form.html",
                form=form,
                titel="Contract toevoegen",
                spelers=spelers,
                clubs=clubs,
                posities=POSITIES,
                ingelogd=is_ingelogd()
            )

        bestaand = Contract.query.filter_by(
            speler_id=speler.id,
            club_id=club.id
        ).first()

        if bestaand:
            flash("Deze speler is al gekoppeld aan deze club.", "danger")
            return render_template(
                "contract_form.html",
                form=form,
                titel="Contract toevoegen",
                spelers=spelers,
                clubs=clubs,
                posities=POSITIES,
                ingelogd=is_ingelogd()
            )

        contract = Contract(
            speler_id=speler.id,
            club_id=club.id,
            positie=form.positie.data,
            rugnummer=form.rugnummer.data
        )
        db.session.add(contract)
        db.session.commit()
        flash("Contract toegevoegd.", "success")
        return redirect(url_for("main.contracten"))

    return render_template(
        "contract_form.html",
        form=form,
        titel="Contract toevoegen",
        spelers=spelers,
        clubs=clubs,
        posities=POSITIES,
        ingelogd=is_ingelogd()
    )


@bp.route("/contracten/bewerken/<int:contract_id>", methods=["GET", "POST"])
@login_required
def contract_bewerken(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    form = ContractForm()

    spelers = Speler.query.order_by(Speler.naam.asc()).all()
    clubs = Club.query.order_by(Club.naam.asc()).all()

    if request.method == "GET":
        form.speler_naam.data = contract.speler.naam
        form.club_naam.data = contract.club.naam
        form.positie.data = contract.positie
        form.rugnummer.data = contract.rugnummer

    if form.validate_on_submit():
        speler = Speler.query.filter_by(naam=form.speler_naam.data).first()
        club = Club.query.filter_by(naam=form.club_naam.data).first()

        if not speler:
            flash("De gekozen speler bestaat niet.", "danger")
            return render_template(
                "contract_form.html",
                form=form,
                titel="Contract bewerken",
                spelers=spelers,
                clubs=clubs,
                posities=POSITIES,
                ingelogd=is_ingelogd()
            )

        if not club:
            flash("De gekozen club bestaat niet.", "danger")
            return render_template(
                "contract_form.html",
                form=form,
                titel="Contract bewerken",
                spelers=spelers,
                clubs=clubs,
                posities=POSITIES,
                ingelogd=is_ingelogd()
            )

        bestaand = Contract.query.filter(
            Contract.speler_id == speler.id,
            Contract.club_id == club.id,
            Contract.id != contract.id
        ).first()

        if bestaand:
            flash("Deze speler is al gekoppeld aan deze club.", "danger")
            return render_template(
                "contract_form.html",
                form=form,
                titel="Contract bewerken",
                spelers=spelers,
                clubs=clubs,
                posities=POSITIES,
                ingelogd=is_ingelogd()
            )

        contract.speler_id = speler.id
        contract.club_id = club.id
        contract.positie = form.positie.data
        contract.rugnummer = form.rugnummer.data
        db.session.commit()
        flash("Contract bijgewerkt.", "success")
        return redirect(url_for("main.contracten"))

    return render_template(
        "contract_form.html",
        form=form,
        titel="Contract bewerken",
        spelers=spelers,
        clubs=clubs,
        posities=POSITIES,
        ingelogd=is_ingelogd()
    )


@bp.route("/contracten/verwijderen/<int:contract_id>", methods=["POST"])
@login_required
def contract_verwijderen(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    db.session.delete(contract)
    db.session.commit()
    flash("Contract verwijderd.", "info")
    return redirect(url_for("main.contracten"))