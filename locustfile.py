from locust import HttpUser, task, between

class GoodLift(HttpUser):
    """
    Classe représentant un utilisateur simulé pour tester la performance de l'application GoodLift.
    Les tâches définies dans cette classe simulent différentes interactions avec l'application,
    telles que la navigation vers la page d'accueil, la connexion, la réservation de compétitions,
    l'achat de places et la déconnexion.
    """
    
    # Définit le temps d'attente entre les tâches pour cet utilisateur (entre 1 et 5 secondes)
    wait_time = between(1, 5)

    @task
    def index(self):
        # Simule une requête GET à la page d'accueil
        self.client.get("/")

    @task
    def show_summary(self):
        # Simule une requête POST à "/showSummary" avec un e-mail valide
        # Cela correspond à la connexion du club "Iron Temple".
        self.client.post("/showSummary", data={'email': 'admin@irontemple.com'})

    @task
    def book(self):
        # Simule une requête GET pour réserver une compétition spécifique pour un club spécifique
        # Ici, la compétition est "Spring Festival" (25 places) et le club est "Iron Temple" (4 points).
        self.client.get("/book/Spring%20Festival/Iron%20Temple")

    @task
    def purchase_place(self):
        # Simule une requête POST pour acheter des places pour une compétition
        # Utilise des valeurs valides pour 'competition', 'club' et 'places' qui correspondent à vos données JSON
        self.client.post("/purchasePlaces", data={'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': '1' })

    @task
    def logout(self):
        # Simule une requête GET pour se déconnecter
        self.client.get("/logout")




