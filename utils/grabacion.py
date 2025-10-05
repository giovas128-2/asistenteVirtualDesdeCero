import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import keyboard
import threading
import datetime
import os
import numpy as np

class Grabacion:
    def __init__(self, talk, listen):
        self.talk = talk
        self.listen = listen
        self.fs = 44100  # frecuencia de muestreo
        self.is_recording = False
        self.audio = []
        self.folder = "grabaciones"

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def grabar(self, comando=None):
        self.talk("Iniciando grabación. Presiona Alt + ` para detener.")
        self.is_recording = True
        self.audio = []

        def record():
            while self.is_recording:
                data = sd.rec(int(2 * self.fs), samplerate=self.fs, channels=1, dtype='int16')
                sd.wait()
                self.audio.extend(data)

        hilo = threading.Thread(target=record)
        hilo.start()

        # Esperar a que se presione Alt + `
        keyboard.wait('alt+`')
        self.is_recording = False
        hilo.join()

        # Guardar archivo temporalmente con nombre por defecto
        default_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(self.folder, f"{default_name}.wav")
        write(path, self.fs, np.array(self.audio))

        self.talk("Grabación detenida.")
        self.talk("¿Qué nombre le quieres poner a la grabación?")
        nombre = self.listen()

        # Si el usuario no dice nada, usa el nombre por defecto
        if not nombre or nombre.strip() == "":
            nombre = default_name

        # Limpiar el nombre para evitar errores en el archivo
        nombre = nombre.replace(" ", "_").replace("/", "-").replace("\\", "-")
        nuevo_path = os.path.join(self.folder, f"{nombre}.wav")
        os.rename(path, nuevo_path)

        self.talk(f"La grabación se ha guardado como {nombre}.wav")
        print(f"[✅ Guardado] {nuevo_path}")

        # Transcribir audio a texto
        self.transcribir(nuevo_path)

    def transcribir(self, audio_path):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        try:
            texto = recognizer.recognize_google(audio_data, language="es-MX")

            # Guardar transcripción en archivo .txt con el mismo nombre
            txt_path = audio_path.replace(".wav", ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(texto)

        except sr.UnknownValueError:
            self.talk("No se entendió claramente lo que dijiste.")
        except Exception as e:
            print("❌ Error al transcribir:", e)
