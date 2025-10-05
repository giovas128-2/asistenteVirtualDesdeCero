import comtypes.client
import threading

class Voz:
    def __init__(self, max_hilos=5):
        self.speaker = comtypes.client.CreateObject("SAPI.SpVoice")
        self.hilos_activos = []
        self.max_hilos = max_hilos
        self.lock = threading.Lock()  # Evita conflictos entre hilos

        # Seleccionamos la voz Sabina en español
        for i in range(self.speaker.GetVoices().Count):
            voz = self.speaker.GetVoices().Item(i)
            if "Sabina" in voz.GetDescription():  # nombre exacto de la voz
                self.speaker.Voice = voz
                break

    def hablar(self, texto):
        """Habla interrumpiendo la voz actual si es necesario"""
        if not texto.strip():
            return

        # Interrumpir voz actual
        with self.lock:
            try:
                self.speaker.Speak("", 3)  # Interrumpe la voz actual
            except Exception:
                pass

        # Limitar cantidad de hilos
        self._limitar_hilos()

        # Crear nuevo hilo para la voz
        hilo = threading.Thread(target=self._decir, args=(texto,), daemon=True)
        hilo.start()
        self.hilos_activos.append(hilo)

    def _decir(self, texto):
        with self.lock:
            self.speaker.Speak(texto)

    def _limitar_hilos(self):
        """Mantiene solo hilos activos y elimina los muertos"""
        for hilo in self.hilos_activos[:]:
            if not hilo.is_alive():
                self.hilos_activos.remove(hilo)
        # Espera si hay demasiados hilos activos
        while len(self.hilos_activos) >= self.max_hilos:
            for hilo in self.hilos_activos[:]:
                if not hilo.is_alive():
                    self.hilos_activos.remove(hilo)
            threading.Event().wait(0.1)
