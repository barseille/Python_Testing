

from locust import HttpUser, task, between

class GoodLift(HttpUser):
    # Définit le temps d'attente entre les tâches pour cet utilisateur (entre 1 et 5 secondes)
    wait_time = between(1, 5)

    @task
    def index(self):
        # Simule une requête GET à la page d'accueil
        self.client.get("/")

    @task
    def show_summary(self):
        # Simule une requête POST à "/showSummary" avec un e-mail valide
        # Cela correspond à la connexion d'un utilisateur
        self.client.post("/showSummary", data={'email': 'admin@irontemple.com'})

    @task
    def book(self):
        # Simule une requête GET pour réserver une compétition spécifique pour un club spécifique
        # Ici, la compétition est "Spring Festival" et le club est "Iron Temple"
        self.client.get("/book/Spring%20Festival/Iron%20Temple")

    @task
    def purchase_place(self):
        # Simule une requête POST pour acheter des places pour une compétition
        # Utilise des valeurs valides pour 'competition', 'club' et 'places' qui correspondent à vos données JSON
        self.client.post("/purchasePlaces", data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '1' })

    @task
    def logout(self):
        # Simule une requête GET pour se déconnecter
        self.client.get("/logout")




# from locust import HttpUser, task, between

# class GoodLift(HttpUser):
#     host = "http://127.0.0.1:5000"
#     wait_time = between(1, 5)

#     @task
#     def index(self):        
#         self.client.get("/")

#     @task
#     def show_summary(self):
#         self.client.post("/showSummary", data={'email': 'john@simplylift.co'})

#     @task
#     def book(self):
#         self.client.get("/book/Spring%20Festival/Simply%20Lift")

#     @task
#     def purchase_place(self):
#         self.client.post("/purchasePlaces", data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '4' })

#     @task
#     def logout(self):        
#         self.client.get("/logout")
