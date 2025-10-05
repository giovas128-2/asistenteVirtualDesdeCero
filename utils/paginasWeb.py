import subprocess as sub
import os
import webbrowser

sites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "github": "https://www.github.com",
    "stackoverflow": "https://stackoverflow.com",
    "hip hop": "https://www.github.com",
    "spotify": "https://www.spotify.com",
}

apps = {
    "spotify": r"C:\Users\Giovas128\AppData\Roaming\Spotify\Spotify.exe",
    "arduino": r"C:\Users\Giovas128\AppData\Local\Programs\Arduino IDE\Arduino IDE.exe",
    "mysql workbench": r"C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe",
    "sql server": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft SQL Server Tools 21\SQL Server Management Studio 21.lnk",
    "vscode": r"C:\Users\Giovas128\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
    "android studio": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Android Studio\Android Studio.lnk",
    "word": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk",
    "excel": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk",
    "powerpoint": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk",
    "whatsapp": {"type": "store", "uri": "whatsapp:"},  # App de Microsoft Store
}
class PaginasWeb:
    def __init__(self, talk):
        self.talk = talk
    def abrir(self, comando):
        comando_lower = comando.lower()
        # Primero intenta abrir apps
        for app_name, info in apps.items():
            if app_name in comando_lower:
                # App de Microsoft Store
                if isinstance(info, dict) and info.get("type") == "store":
                    os.system(f'start {info["uri"]}')
                    self.talk(f"Abriendo {app_name} desde Microsoft Store")
                    return
                # App normal (.exe o .lnk)
                elif os.path.exists(info):
                    os.startfile(info)
                    self.talk(f"Abriendo {app_name}")
                    return
                else:
                    # fallback a web si existe
                    if app_name in sites:
                        webbrowser.open(sites[app_name])
                        self.talk(f"No encontré la app {app_name}, abriendo versión web")
                        return
                    else:
                        self.talk(f"No encontré {app_name}")
                        return
        # Si no es app, intenta abrir página web
        for site_name, url in sites.items():
            if site_name in comando_lower:
                try:
                    sub.call(f'start chrome.exe {url}', shell=True)
                except:
                    webbrowser.open(url)
                self.talk(f"Abriendo {site_name}")
                return
        self.talk("No reconocí la página web o app que quieres abrir")