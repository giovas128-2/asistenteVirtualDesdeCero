import os 
files = {
    "documentos": os.path.join(os.path.expanduser("~"), "Documents"),
    "descargas": os.path.join(os.path.expanduser("~"), "Downloads"),
    "escritorio": os.path.join(os.path.expanduser("~"), "Desktop"),
    "imágenes": os.path.join(os.path.expanduser("~"), "Pictures"),
    "música": os.path.join(os.path.expanduser("~"), "Music"),
    "videos": os.path.join(os.path.expanduser("~"), "Videos"),
}



class archivos:
    def __init__(self, talk):
        self.talk = talk
    
    def abrir(self, comando):
        """
        Abre una carpeta común en el explorador de archivos.
        Ejemplos:
        - 'abre la carpeta documentos'
        - 'abre descargas'
        """
        for key in files:
            if key in comando:
                path = files[key]
                if os.path.exists(path):
                    os.startfile(path)
                    self.talk(f"Abriendo {key}")
                else:
                    self.talk(f"No encontré la carpeta {key} en tu computadora")
                return
        self.talk("No reconocí la carpeta que quieres abrir")