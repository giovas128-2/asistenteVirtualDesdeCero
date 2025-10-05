import datetime

class Hora:
    def __init__(self, talk):
        self.talk = talk
    def decir_hora(self):
        hora = datetime.datetime.now().strftime("%I:%M %p")
        self.talk(f"Son las {hora}")
