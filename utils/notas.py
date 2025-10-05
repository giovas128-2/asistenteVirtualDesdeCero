import os
import subprocess as sub

class Notas:
    def __init__(self, talk, listen):
        self.talk = talk
        self.listen = listen

    def write(self):
        # Pregunta el nombre de la nota
        self.talk("¿Cómo quieres llamar esta nota?")
        nombre = self.listen().replace(" ", "_")  # cambia espacios por guiones bajos
        filename = f"{nombre}.txt"

        # Pregunta el contenido de la nota
        self.talk("¿Qué quieres escribir en la nota?")
        rec_write = self.listen()

        # Crear y guardar archivo
        with open(filename, "w", encoding="utf-8") as f:
            f.write(rec_write + os.linesep)

        self.talk(f"He escrito lo que me dictaste, puedes revisarlo en {filename}")
        sub.Popen(filename, shell=True)

    def abrir(self, comando):
        """
        Crea una nueva nota con nombre dictado por voz.
        Ejemplo:
        - 'anota tarea'
        - 'haz una nota'
        """
        self.write()
    
    def leer(self, comando):
        """
        Lee una nota existente y la dice en voz alta.
        Ejemplo:
        - 'enséñame la nota reputin'
        - 'lee la nota tarea_de_mates'
        """
        try:
            # Sacar nombre de la nota del comando
            partes = comando.split("nota", 1)
            if len(partes) < 2:
                self.talk("No entendí qué nota quieres que te muestre.")
                return

            nombre = partes[1].strip().replace(" ", "_")
            filename = f"{nombre}.txt"

            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    contenido = f.read().strip()
                    if contenido:
                        self.talk(f"La nota {nombre} dice: {contenido}")
                    else:
                        self.talk(f"La nota {nombre} está vacía.")
            else:
                self.talk(f"No encontré ninguna nota llamada {nombre}.")
        except Exception as e:
            self.talk(f"Ocurrió un error al leer la nota: {str(e)}")
    def agregar(self, comando):
        try:
            # Sacar nombre de la nota del comando
            partes = comando.split("nota", 1)
            if len(partes) < 2:
                self.talk("No entendí a qué nota quieres agregarle contenido.")
                return

            nombre = partes[1].strip().replace(" ", "_")
            filename = f"{nombre}.txt"

            if not os.path.exists(filename):
                self.talk(f"No encontré ninguna nota llamada {nombre}. ¿Quieres crearla?")
                respuesta = self.listen().lower()
                if "sí" in respuesta or "si" in respuesta:
                    self.write()
                elif "no" in respuesta:
                    self.talk("De acuerdo, no haré nada.")
                return
            # Pregunta qué se quiere agregar
            self.talk(f"¿Qué quieres agregar a la nota {nombre}?")
            nuevo_contenido = self.listen()

            # Agregar al final de la nota
            with open(filename, "a", encoding="utf-8") as f:
                f.write(nuevo_contenido + os.linesep)

            self.talk(f"He agregado lo que me dictaste a la nota {nombre}.")
            sub.Popen(filename, shell=True)

        except Exception as e:
            self.talk(f"Ocurrió un error al agregar la nota: {str(e)}")
