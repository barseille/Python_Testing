import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

# Limite de réservation
BOOKING_LIMIT = 12

app = Flask(__name__)
app.secret_key = 'something_special'


def loadClubs():
    """Charge et renvoie la liste des clubs à partir du fichier 'clubs.json'."""
    
    with open('clubs.json') as c:
        # convertir json en objet python
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """
    Charge et renvoie la liste des compétitions à partir du fichier 'competitions.json'.
    Convertit également les dates en objets datetime.
    """
    
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        # Convertir les dates en objets datetime
        for comp in listOfCompetitions:
            comp['date'] = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
        return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """Retourne la page d'index (connexion par email)"""
    return render_template('index.html')


class EmailError(Exception):
    """Exception personnalisée pour gérer les erreurs liées aux emails."""
    
    def __init__(self, email, message="n'a pas été trouvé !"):
        self.email = email
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.email} {self.message}"


def get_email(email):
    """
    Récupère le club à partir de l'email.
    Lève une EmailError si l'email n'est pas trouvé dans la liste des clubs.
    """
    
    # Si l'adresse email est vide
    if not email:
        raise ValueError("Veuillez entrer un email valide.")
    
    # On parcourt la liste des clubs
    for club in clubs:
        
        # Si l'email du club est égale à l'email fournie
        if club['email'] == email:
            return club
        
    # Si l'email n'est pas dans la base de données
    raise EmailError(email)


@app.route('/showSummary',methods=['POST'])
def showSummary():
    """
    Page welcome.html après connexion par l'email via la page index.html, 
    on affiche :
    - le nombre de point disponible du club
    - la liste des compétitions avec lien de réservation
    Si l'email non trouvé, redirection vers la page d'index avec un message d'erreur
    """

    try:
        club = get_email(request.form['email'])
        return render_template('welcome.html',club=club,competitions=competitions, now=datetime.now())
    
    except (EmailError, ValueError) as e: 
        flash(str(e))
        return redirect(url_for('index')) 


def validate_purchase(competition, club, places_required):
    if places_required <= 0:
        return "Le nombre de places demandées doit être un nombre positif."
    elif int(competition['numberOfPlaces']) < places_required:
        return "Pas assez de places disponibles dans la compétition."
    elif places_required > BOOKING_LIMIT:
        return f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places."
    elif int(club['points']) < places_required:
        return "Pas assez de points pour réserver ce nombre de places."
    return None


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required_str = request.form['places']
    now = datetime.now()

    competition, club = None, None
    for c in competitions:
        if c['name'] == competition_name:
            competition = c
            break
    for c in clubs:
        if c['name'] == club_name:
            club = c
            break

    if competition is None or club is None or places_required_str == '':
        flash("Erreur. Veuillez saisir un nombre de places valides.")
        return render_template('welcome.html', club=club, competitions=competitions, now=now), 404

    places_required = int(places_required_str)
    error_message = validate_purchase(competition, club, places_required)
    if error_message:
        flash(error_message)
        return render_template('welcome.html', club=club, competitions=competitions, now=now), 400

    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)
    club['points'] = str(int(club['points']) - places_required)
    flash('Super ! Réservation réussie!')
    return render_template('welcome.html', club=club, competitions=competitions, now=now), 200

@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Page de formulaire de réservation des places.
    Les paramètres 'competition' et 'club' sont extraits de l'URL et utilisés pour trouver
    la compétition et le club correspondants.
    Renvoie la page de réservation si la compétition et le club existent et que la compétition n'a pas encore eu lieu.
    Renvoie la page d'accueil avec un message d'erreur dans les autres cas.
    """

    foundClub = None
    for c in clubs:
        if c['name'] == club:
            foundClub = c
            break

    foundCompetition = None
    for c in competitions:
        if c['name'] == competition:
            foundCompetition = c
            break

    now = datetime.now()

    if foundClub is None or foundCompetition is None:
        flash("Erreur - Club ou compétition non trouvés, veuillez réessayer")
        return render_template('welcome.html', club=foundClub, competitions=competitions, now=datetime.now()), 404

    limit = min(int(foundClub['points']), BOOKING_LIMIT)
    return render_template('booking.html', club=foundClub, competition=foundCompetition, limit=limit)


@app.route('/points_clubs', methods=['GET'])
def points_clubs():
    return render_template('points_clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    """Déconnecte l'utilisateur et redirige vers la page d'index."""
    return redirect(url_for('index'))