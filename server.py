import json
from flask import Flask, render_template, request, redirect, flash, url_for

# Limite de réservation
BOOKING_LIMIT = 12


def loadClubs():
    """Charge et renvoie la liste des clubs à partir du fichier 'clubs.json'."""
    
    with open('clubs.json') as c:
        # convertir json en objet python
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
    """Exception personnalisée pour gérer les erreurs liées aux emails."""
    
    def __init__(self, email, message="n'a pas été trouvé !"):
        self.email = email
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.email} {self.message}"


def get_email(email):
    """Récupère le club à partir de l'email."""
    
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
    la fonction showSummary traite une requête POST sur l'URL '/showSummary', 
    tente de trouver le club associé à l'email fourni dans le formulaire de la requête, 
    et renvoie la page de bienvenue pour ce club. Si elle ne trouve pas le club, 
    elle affiche un message d'erreur et redirige l'utilisateur vers la page d'index.
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
        json.dump({'clubs': clubs}, c, indent=4)

def saveCompetitions(competitions):
    """Sauvegarde la liste des compétitions dans le fichier 'competitions.json'."""
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)




@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    
    # On récupère la compétition, le club et le nombre de places demandées 
    # à partir des données du formulaire
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    club = [c for c in clubs if c['name'] == request.form['club']]
    placesRequired = int(request.form['places'])

    # Si la compétition ou le club n'existe pas, on renvoie un message d'erreur
    if not competition or not club:
        return "Club ou compétition non trouvé.", 404

    competition = competition[0]
    club = club[0]
    
    # Si le nombre de places demandées est inférieur à zéro
    if placesRequired <= 0:
        flash("Le nombre de places demandées doit être un nombre positif.")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    


    # Si le nombre de places disponibles est inférieur au nombre de place demandées
    if int(competition['numberOfPlaces']) < placesRequired:
        flash("Pas assez de places disponibles dans la compétition.")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    
    # Si le nombre de places demandées est supérieur à la limite 
    if placesRequired > BOOKING_LIMIT:
        flash(f"Vous ne pouvez pas réserver plus de {BOOKING_LIMIT} places.")
        return render_template("welcome.html", club=club, competitions=competitions), 400

    # Si le club a assez de points pour réserver le nombre de places demandées
    if int(club['points']) < placesRequired:
        flash("Pas assez de points pour réserver ce nombre de places.")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    


    # Si ok, on déduit le nombre de places demandées du nombre de places disponibles
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
    
    # Si ok, on déduit le même nombre de points du club
    club['points'] = str(int(club['points']) - placesRequired)

    # On sauvegarde les clubs et les compétitions mise à jour 
    saveClubs(clubs)
    saveCompetitions(competitions)

    # Message de succès
    flash('Super ! Réservation réussie!')
    return render_template('welcome.html', club=club, competitions=competitions), 200



@app.route('/logout')
def logout():
    """Déconnecte l'utilisateur et redirige vers la page d'index."""
    return redirect(url_for('index'))