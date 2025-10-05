import comtypes.client

class voces:
    def __init__(self):
        self.speaker = comtypes.client.CreateObject("SAPI.SpVoice")
        self.voces_disponibles = self._listar_voces()
    def _listar_voces(self):
        voces = []
        for i in range(self.speaker.GetVoices().Count):
            voz = self.speaker.GetVoices().Item(i)
            voces.append(voz.GetDescription())
        return voces
    def mostrar_voces(self):
        print("Voces instaladas en el sistema:")
        for idx, voz in enumerate(self.voces_disponibles, 1):
            print(f"{idx}. {voz}")
# ---------------------
# Ejecutar prueba
# ---------------------
if __name__ == "__main__":
    v = voces()
    v.mostrar_voces()
