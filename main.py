import threading
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
from mauricio import Mauricio
from voz import Voz  # Nueva clase de voz

# -------------------------------
# Configuración inicial
# -------------------------------
ACCESS_KEY = "Nsmlee8wjRWzhc2o7Br2z73H+IJuQMr7KfRA84rnv145IF9G8cCnng=="
KEYWORD_PATH = r"wakewords\mauricio_en_windows_v3_0_0.ppn"

listener = sr.Recognizer()
voz_mauricio = Voz()  # Instancia de voz

# -------------------------------
# Función para escuchar comando
# -------------------------------
def listen():
    rec = ""
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)
            listener.pause_threshold = 1.5
            listener.energy_threshold = 300
            print("🎤 Escuchando...")
            audio = listener.listen(source, timeout=5)
            rec = listener.recognize_google(audio, language='es-MX').lower()
            print("Reconocido:", rec)
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
    except sr.RequestError:
        print("Error con el servicio de Google.")
    return rec

# -------------------------------
# Wake Word con Porcupine
# # -------------------------------
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[KEYWORD_PATH]
)
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

# -------------------------------
# Arranque del asistente
# -------------------------------
asistente = Mauricio(voz_mauricio.hablar, listen)
voz_mauricio.hablar("Hola, en qué puedo ayudarte?")

while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
    result = porcupine.process(pcm_unpacked)

    if result >= 0:  # Detectó la palabra "Mauricio"
        voz_mauricio.hablar("Te escucho...")
        comando = listen()
        if comando:
            asistente.ejecutar_comando(comando)
