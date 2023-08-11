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
        raise ValueError("L'email ne peut pas être une chaîne vide.")
    
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
    except EmailError as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Affiche les informations sur la réservation des places à une compétition sur la page welcome.html
    et met à jour le nombre de places et de points si la réservation est réussie.
    Si aucunes erreur est levée.
    """
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required_str = request.form['places']
    now = datetime.now()

    # Trouver la compétition et le club correspondants
    competition, club = None, None
    for c in competitions:
        if c['name'] == competition_name:
            competition = c
            break
    for c in clubs:
        if c['name'] == club_name:
            club = c
            break

    # Vérifier si la compétition et le club existent
    if competition is None or club is None or places_required_str == '':
        flash("Club ou compétition non trouvé.")
        return render_template('welcome.html', club=club, competitions=competitions, now=now), 404

    places_required = int(places_required_str)

    # Vérifications supplémentaires
    if places_required <= 0:
        flash("Le nombre de places demandées doit être un nombre positif.")
        
    elif int(competition['numberOfPlaces']) < places_required:
        flash("Pas assez de places disponibles dans la compétition.")
        
    elif places_required > BOOKING_LIMIT:
        flash(f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places.")
        
    elif int(club['points']) < places_required:
        flash("Pas assez de points pour réserver ce nombre de places.")
        
    else:
        # Si tout est OK, mise à jour des places et des points
        competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)
        club['points'] = str(int(club['points']) - places_required)
        flash('Super ! Réservation réussie!')
        return render_template('welcome.html', club=club, competitions=competitions, now=now), 200

    # Si une des vérifications a échoué
    return render_template('welcome.html', club=club, competitions=competitions, now=now), 400


# @app.route('/purchasePlaces', methods=['POST'])
# def purchasePlaces():
#     """
#     Affiche les informations sur la réservation des places à une compétition sur la page welcome.html
#     et met à jour le nombre de places et de points si la réservation est réussie.
#     Si aucunes erreur est levée.
#     """
    
#     competition = None
#     for c in competitions:
#         if c['name'] == request.form['competition']:
#             competition = c
#             break

#     club = None
#     for c in clubs:
#         if c['name'] == request.form['club']:
#             club = c
#             break

#     if competition is None or club is None:
#         return "Club ou compétition non trouvé.", 404

#     placesRequired_str = request.form['places']
#     if placesRequired_str == '':
#         flash("Veuillez entrer un nombre de places valide.")
#         return render_template('welcome.html', club=club, competitions=competitions, now=datetime.now()), 400

#     placesRequired = int(placesRequired_str)  
#     now = datetime.now()

#     # Si le nombre de places demandées est inférieur à zéro
#     if placesRequired <= 0:
#         flash("Le nombre de places demandées doit être un nombre positif.")
#         return render_template('welcome.html', club=club, competitions=competitions, now=now), 400

#     # Si le nombre de places disponibles est inférieur au nombre de place demandées
#     if int(competition['numberOfPlaces']) < placesRequired:
#         flash("Pas assez de places disponibles dans la compétition.")
#         return render_template('welcome.html', club=club, competitions=competitions, now=now), 400

#     # Si le nombre de places demandées est supérieur à la limite
#     if placesRequired > BOOKING_LIMIT:
#         flash(f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places.")
#         return render_template("welcome.html", club=club, competitions=competitions, now=now), 400

#     # Si le club n'a pas assez de points pour réserver le nombre de places demandées
#     if int(club['points']) < placesRequired:
#         flash("Pas assez de points pour réserver ce nombre de places.")
#         return render_template('welcome.html', club=club, competitions=competitions, now=now), 400

#     # Si ok, on déduit le nombre de places demandées du nombre de places disponibles
#     competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)

#     # Si ok, on déduit le même nombre de points du club
#     club['points'] = str(int(club['points']) - placesRequired)

#     # Message de succès
#     flash('Super ! Réservation réussie!')
#     return render_template('welcome.html', club=club, competitions=competitions, now=datetime.now()), 200


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Page de formulaire de réservation des places
    """
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
    
    # if foundClub and foundCompetition:
    #     competition_date = foundCompetition['date']
    #     if competition_date < now:
    #         flash("Cette compétition a déjà eu lieu. Réservation impossible.")
    #         return render_template('welcome.html', club=foundClub, competitions=competitions, now=now)
    #     return render_template('booking.html', club=foundClub, competition=foundCompetition)
    # else:
    #     flash("Erreur - veuillez réessayer")
    #     return render_template('welcome.html', club=foundClub, competitions=competitions, now=now)
    
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Erreur - veuillez réessayer")
        return render_template('welcome.html', club=foundClub, competitions=competitions, now=datetime.now())

@app.route('/points_clubs', methods=['GET'])
def points_clubs():
    return render_template('points_clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    """Déconnecte l'utilisateur et redirige vers la page d'index."""
    return redirect(url_for('index'))