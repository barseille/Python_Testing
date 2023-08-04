import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    """Charge et renvoie la liste des clubs à partir du fichier 'clubs.json'."""
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """Charge et renvoie la liste des compétitions à partir du fichier 'competitions.json'."""
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    """Retourne la page d'index."""
    return render_template('index.html')


class EmailError(Exception):
    """Exception levée pour les erreurs dans le module club."""
    def __init__(self, email, message="n'a pas été trouvé !"):
        self.email = email
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.email} {self.message}"


def get_email(email):
    """Récupère le club à partir de l'email."""
    if not email:
        raise ValueError("L'email ne peut pas être une chaîne vide.")
    for club in clubs:
        if club['email'] == email:
            return club
    raise EmailError(email)




@app.route('/showSummary',methods=['POST'])
def showSummary():
    """
    Traite la requête POST de la page d'index.
    Trouve le club à partir de l'email dans les données du formulaire 
    et rend la page de bienvenue pour ce club.
    """
    try:
        club = get_email(request.form['email'])
        return render_template('welcome.html',club=club,competitions=competitions)
    except EmailError as e:
        flash(str(e))
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    """
    Gère la réservation d'une compétition.
    Trouve le club et la compétition à partir des paramètres de l'URL et rend la page de réservation.
    """
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)



def saveClubs(clubs):
    """Sauvegarde la liste des clubs dans le fichier 'clubs.json'."""
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c)

def saveCompetitions(competitions):
    """Sauvegarde la liste des compétitions dans le fichier 'competitions.json'."""
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps)




@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    club = [c for c in clubs if c['name'] == request.form['club']]
    placesRequired = int(request.form['places'])

    if not competition or not club:
        return "Club ou compétition non trouvé.", 404

    competition = competition[0]
    club = club[0]

    if placesRequired <= 0:
        flash("Le nombre de places demandées doit être un nombre positif.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    if int(competition['numberOfPlaces']) < placesRequired:
        flash("Pas assez de places disponibles dans la compétition.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    if int(club['points']) < placesRequired:
        flash("Pas assez de points pour réserver ce nombre de places.")
        return render_template('welcome.html', club=club, competitions=competitions), 400

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired

    saveClubs(clubs)
    saveCompetitions(competitions)

    flash('Super ! Réservation réussie!')
    return render_template('welcome.html', club=club, competitions=competitions), 200



@app.route('/logout')
def logout():
    """Déconnecte l'utilisateur et redirige vers la page d'index."""
    return redirect(url_for('index'))