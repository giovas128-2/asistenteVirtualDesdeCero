import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pygame import mixer
import subprocess
import urllib.parse
import time
import os

class Musica:
    def __init__(self, talk):
        self.talk = talk
        mixer.init()
        self.sonando_local = False

        # Rutas de accesos directos
        self.chrome_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
        self.spotify_path = r"C:\Users\Giovas128\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Spotify.lnk"

        # Configuración Spotify Web API
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="431ae67782c74973a7d97df0aa28d354",
            client_secret="31e225a8fd394e128d75bc178eded86b",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-modify-playback-state user-read-playback-state"
        ))

        self.ultimo_track_uri = None
        self.ultimo_device_id = None
    def reproducir(self, comando: str):
        # Limpiar palabras clave
        for palabra in ["reproduce", "toca", "pon", "quiero escuchar"]:
            comando = comando.lower().replace(palabra, "").strip()

        if not comando:
            self.talk("Dime qué canción quieres escuchar")
            return

        # --- Caso especial: reproducir "Mis me gusta" ---
        if "mis me gusta" in comando or comando == "me gusta":
            try:
                devices = self.sp.devices()
                if not devices['devices']:
                    # Abrir Spotify si no hay dispositivo
                    subprocess.Popen([self.spotify_path], shell=True)
                    time.sleep(5)
                    devices = self.sp.devices()

                if devices['devices']:
                    device_id = devices['devices'][0]['id']
                    self.ultimo_device_id = device_id
                    liked_songs_uri = "spotify:collection:tracks"
                    self.sp.start_playback(device_id=device_id, context_uri=liked_songs_uri)
                    self.talk("Reproduciendo tus canciones que te gustan en Spotify")
                    return
                else:
                    self.talk("No encontré ningún dispositivo activo en Spotify")
                    return
            except Exception as e:
                print("Error al reproducir 'Mis me gusta':", e)
                self.talk("Ocurrió un error al abrir tus canciones que te gustan")
                return

        # --- Caso 1: Archivo local ---
        if comando.endswith(".mp3") or comando.endswith(".wav"):
            if os.path.exists(comando):
                mixer.music.load(comando)
                mixer.music.play()
                self.sonando_local = True
                self.talk(f"Reproduciendo {comando}")
                return
            else:
                self.talk("No encontré el archivo de música en tu computadora")
                return
        try:
            resultado_artista = self.sp.search(q=comando, type="artist", limit=1)
            if resultado_artista['artists']['items']:
                artista = resultado_artista['artists']['items'][0]
                artista_uri = artista['uri']
                devices = self.sp.devices()
                if not devices['devices']:
                    subprocess.Popen([self.spotify_path], shell=True)
                    time.sleep(5)
                    devices = self.sp.devices()
                if devices['devices']:
                    device_id = devices['devices'][0]['id']
                    self.ultimo_device_id = device_id
                    self.sp.start_playback(device_id=device_id, context_uri=artista_uri)
                    self.talk(f"Reproduciendo canciones de {artista['name']} en Spotify")
                    return
        except Exception as e:
            print("Error al reproducir artista:", e)
        # --- Caso 2: Spotify Web API ---
        try:
            resultado = self.sp.search(q=comando, type="track", limit=1)
            if resultado['tracks']['items']:
                track_uri = resultado['tracks']['items'][0]['uri']
                devices = self.sp.devices()
                if devices['devices']:
                    device_id = devices['devices'][0]['id']
                    self.ultimo_track_uri = track_uri
                    self.ultimo_device_id = device_id
                    self.sp.start_playback(device_id=device_id, uris=[track_uri])
                    self.talk(f"Reproduciendo {comando} en Spotify")
                    return
                else:
                    # Abrir Spotify si no hay dispositivo activo
                    subprocess.Popen([self.spotify_path], shell=True)
                    time.sleep(5)
                    devices = self.sp.devices()
                    if devices['devices']:
                        device_id = devices['devices'][0]['id']
                        self.ultimo_track_uri = track_uri
                        self.ultimo_device_id = device_id
                        self.sp.start_playback(device_id=device_id, uris=[track_uri])
                        self.talk(f"Reproduciendo {comando} en Spotify")
                        return
                    else:
                        self.talk("No pude detectar ningún dispositivo activo en Spotify")
            else:
                self.talk("No encontré la canción en Spotify")
        except Exception as e:
            print("Error Spotify API:", e)
            self.talk("Ocurrió un error con Spotify")

        # --- Caso 3: YouTube con Chrome ---
        try:
            query = urllib.parse.quote(comando)
            url_youtube = f"https://www.youtube.com/results?search_query={query}"
            self.talk(f"Buscando {comando} en YouTube")
            subprocess.Popen([self.chrome_path, url_youtube], shell=True)
        except Exception as e:
            print("Error al abrir YouTube con Chrome:", e)
            self.talk(f"No pude reproducir {comando}")

    # --- FUNCIONES DE CONTROL ---
    def detener(self):
        """Pausa la reproducción"""
        try:
            if self.ultimo_device_id:
                self.sp.pause_playback(device_id=self.ultimo_device_id)
                self.talk("La música se detuvo")
            elif self.sonando_local and mixer.music.get_busy():
                mixer.music.pause()
                self.talk("La música local se detuvo")
            else:
                self.talk("No hay música reproduciéndose")
        except Exception as e:
            print("Error al detener:", e)

    def reanudar(self):
        """Reanuda la reproducción"""
        try:
            if self.ultimo_device_id and self.ultimo_track_uri:
                self.sp.start_playback(device_id=self.ultimo_device_id, uris=[self.ultimo_track_uri])
                self.talk("Reanudando la música")
            elif self.sonando_local:
                mixer.music.unpause()
                self.talk("Reanudando la música local")
            else:
                self.talk("No hay música para reanudar")
        except Exception as e:
            print("Error al reanudar:", e)

    def siguiente(self):
        """Siguiente canción en Spotify"""
        try:
            if self.ultimo_device_id:
                self.sp.next_track(device_id=self.ultimo_device_id)
                self.talk("Pasando a la siguiente canción")
            else:
                self.talk("No hay música de Spotify activa para avanzar")
        except Exception as e:
            print("Error al pasar a la siguiente:", e)

    def anterior(self):
        """Retroceder canción en Spotify"""
        try:
            if self.ultimo_device_id:
                self.sp.previous_track(device_id=self.ultimo_device_id)
                self.talk("Volviendo a la canción anterior")
            else:
                self.talk("No hay música de Spotify activa para retroceder")
        except Exception as e:
            print("Error al retroceder:", e)
