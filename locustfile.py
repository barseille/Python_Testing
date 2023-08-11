# from locust import HttpUser, task, between

# class GoodLift(HttpUser):
    
#     wait_time = between(1, 5)

#     competitions = ["Spring Festival", "Fall Classic"]
#     clubs = ["Simply Lift", "Iron Temple", "She Lifts"]

#     @task
#     def index(self):        
#         self.client.get("/")

#     @task
#     def show_summary(self):
#         for club_email in ["john@simplylift.co", "admin@irontemple.com", "kate@shelifts.co.uk"]:
#             self.client.post("/showSummary", data={'email': club_email})

#     @task
#     def book_competition(self):
#         for competition_name in self.competitions:
#             for club_name in self.clubs:
#                 self.client.get(f"/book/{competition_name.replace(' ', '%20')}/{club_name.replace(' ', '%20')}")

#     @task
#     def purchase_place(self):
#         for competition_name in self.competitions:
#             for club_name in self.clubs:
#                 self.client.post("/purchasePlaces", data={'competition': competition_name, 'club': club_name, 'places': '1'})

#     @task
#     def view_points_clubs(self):
#         self.client.get("/points_clubs")

#     @task
#     def logout(self):        
#         self.client.get("/logout")

from locust import HttpUser, task, between

class GoodLift(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):        
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={'email': 'admin@irontemple.com'})

    @task
    def book(self):
        self.client.get("/book/Spring%20Festival/Iron%20Temple")

    @task
    def purchase_place(self):
        self.client.post("/purchasePlaces", data={'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': '4' })

    @task
    def logout(self):        
        self.client.get("/logout")

