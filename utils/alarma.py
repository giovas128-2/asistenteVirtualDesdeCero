import datetime
import threading
import time
import re
from pygame import mixer

class Alarma:
    def __init__(self, talk, listen):
        self.alarmas = []              # Lista de diccionarios: {"hora": datetime.time, "nota": str}
        self.alarma_sonando = None     # Diccionario de la alarma actualmente sonando
        self.talk = talk
        self.listen = listen

    def programar(self, comando: str):
        """Programa una alarma a partir de un texto"""
        match = re.search(r'(\d{1,2})(?::(\d{2}))?', comando)
        if not match:
            self.talk("No entendí la hora. Ejemplo: 'pon una alarma a las 7:30 de la mañana'")
            return

        hora = int(match.group(1))
        minutos = int(match.group(2)) if match.group(2) else 0

        # Ajuste AM/PM
        if "tarde" in comando or "pm" in comando:
            if hora < 12:
                hora += 12
        elif "mañana" in comando or "am" in comando:
            if hora == 12:
                hora = 0

        alarma_time = datetime.time(hora, minutos)
        self.alarmas.append({"hora": alarma_time, "nota": ""})
        self.talk(f"Alarma puesta a las {alarma_time.strftime('%I:%M %p')}")
        threading.Thread(target=self._alarma_worker, args=(alarma_time,), daemon=True).start()

    def _alarma_worker(self, alarma_time):
        """Hilo que espera hasta que la hora coincida"""
        while True:
            ahora = datetime.datetime.now().strftime("%H:%M")
            if ahora == alarma_time.strftime("%H:%M"):
                self.alarma_sonando = next(a for a in self.alarmas if a["hora"] == alarma_time)
                self.talk("⏰ Hora de despertar! Di 'detener alarma' para apagarla.")
                mixer.init()
                mixer.music.load("alarma.mp3")
                mixer.music.play(-1)
                break
            time.sleep(10)

    def agregar_nota(self, comando: str):
        """Agrega una nota a una alarma específica"""
        match = re.search(r'(\d{1,2})(?::(\d{2}))?', comando)
        if not match:
            self.talk("No entendí la hora de la alarma")
            return

        hora = int(match.group(1))
        minutos = int(match.group(2)) if match.group(2) else 0
        if "tarde" in comando or "pm" in comando:
            if hora < 12:
                hora += 12
        elif "mañana" in comando or "am" in comando:
            if hora == 12:
                hora = 0

        alarma_time = datetime.time(hora, minutos)
        alarma_obj = next((a for a in self.alarmas if a["hora"] == alarma_time), None)
        if alarma_obj:
            self.talk("¿Qué quieres agregar como nota para esta alarma?")
            nota = self.listen()
            alarma_obj["nota"] = nota
            self.talk(f"Nota agregada a la alarma de las {alarma_time.strftime('%I:%M %p')}")
        else:
            self.talk("No encontré esa alarma")

    def detener(self):
        """Detiene la alarma y lee la nota si existe"""
        if self.alarma_sonando:
            mixer.music.stop()
            self.talk("Alarma detenida")
            if self.alarma_sonando["nota"]:
                self.talk("Tu nota para esta alarma es: " + self.alarma_sonando["nota"])
            self.alarma_sonando = None
        else:
            self.talk("No hay ninguna alarma sonando")

    def listar(self):
        """Muestra todas las alarmas activas"""
        if not self.alarmas:
            self.talk("No tienes alarmas programadas")
        else:
            alarmas_str = ", ".join([a["hora"].strftime("%I:%M %p") for a in self.alarmas])
            self.talk("Tienes las siguientes alarmas: " + alarmas_str)

    def eliminar(self, comando: str):
        """Elimina una alarma específica"""
        match = re.search(r'(\d{1,2})(?::(\d{2}))?', comando)
        if not match:
            self.talk("No entendí la hora de la alarma que quieres eliminar")
            return

        hora = int(match.group(1))
        minutos = int(match.group(2)) if match.group(2) else 0
        if "tarde" in comando or "pm" in comando:
            if hora < 12:
                hora += 12
        elif "mañana" in comando or "am" in comando:
            if hora == 12:
                hora = 0

        alarma_time = datetime.time(hora, minutos)
        alarma_obj = next((a for a in self.alarmas if a["hora"] == alarma_time), None)
        if alarma_obj:
            self.alarmas.remove(alarma_obj)
            self.talk(f"Alarma de las {alarma_time.strftime('%I:%M %p')} eliminada")
        else:
            self.talk("No encontré esa alarma")
    
    def actualizar_nota(self, comando: str):
        """Actualiza la nota de una alarma específica"""
        # Extraemos la hora de la alarma del comando
        match = re.search(r'(\d{1,2})(?::(\d{2}))?', comando)
        if not match:
            self.talk("No entendí la hora de la alarma para actualizar la nota.")
            return
        hora = int(match.group(1))
        minutos = int(match.group(2)) if match.group(2) else 0

        # Ajuste AM/PM
        if "tarde" in comando or "pm" in comando:
            if hora < 12:
                hora += 12
        elif "mañana" in comando or "am" in comando:
            if hora == 12:
                hora = 0

        alarma_time = datetime.time(hora, minutos)

        # Buscamos la alarma y actualizamos la nota
        for alarma in self.alarmas:
            if alarma["hora"] == alarma_time:
                self.talk("Dime la nueva nota para esta alarma:")
                nueva_nota = self.listen()
                alarma["nota"] = nueva_nota
                self.talk(f"Nota de la alarma de las {alarma_time.strftime('%I:%M %p')} actualizada.")
                return

        self.talk("No encontré ninguna alarma a esa hora.")


    def gestionar(self, comando: str):
        """Detecta acción según el comando"""
        if "pon" in comando or "configura" in comando:
            self.programar(comando)
        elif "qué alarmas" in comando or "mis alarmas" in comando:
            self.listar()
        elif "elimina todas" in comando:
            self.alarmas.clear()
            self.talk("Todas las alarmas han sido eliminadas")
        elif "elimina" in comando or "borrar alarma" in comando or "quitar alarma" in comando:
            self.eliminar(comando)
        elif "agrega nota" in comando or "nota en la alarma" in comando:
            self.agregar_nota(comando)
        elif "actualiza la nota" in comando or "modifica la nota" in comando:
            self.actualizar_nota(comando)
        elif "detener alarma" in comando or "apaga" in comando or "callate" in comando or "cayate" in comando:
            self.detener()
        else:
            self.talk("No entendí lo que quieres hacer con la alarma")
