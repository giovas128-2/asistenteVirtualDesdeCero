import wikipedia

class Buscador:
    def __init__(self, talk):
        self.talk = talk
        wikipedia.set_lang("es")

    def buscar(self, comando: str):
        """Busca un tema en Wikipedia"""
        # limpiar comando
        for palabra in ["busca", "buscame", "investiga", "investiga sobre", "dime sobre", "qué es", "dime qué es"]:
            comando = comando.replace(palabra, "").strip()

        if not comando:
            self.talk("Dime qué quieres que busque")
            return

        try:
            resumen = wikipedia.summary(comando, sentences=2)
            print(f"{comando}: {resumen}")
            self.talk(resumen[:400])  # limitar la lectura
        except Exception:
            self.talk(f"No encontré información sobre {comando}")
