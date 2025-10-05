# 🤖 Asistente Virtual "Mauricio"

**Mauricio** es un asistente virtual desarrollado en **Python** que permite interactuar por voz con el sistema, ejecutar comandos, reproducir música, grabar audio, gestionar alarmas y mucho más.  
Su característica principal es que **responde únicamente cuando escucha su nombre**, gracias a la integración con **Picovoice Porcupine**, lo que lo hace rápido, eficiente y funcional incluso sin conexión a internet.

---

## 🧠 Descripción general

Mauricio ofrece una experiencia fluida de interacción por voz.  
Combina **reconocimiento de comandos**, **respuesta hablada**, **automatización del sistema** e **integración con Spotify**, todo dentro de una arquitectura modular.  

El asistente está diseñado para evolucionar hacia una **versión con interfaz gráfica (app)**, en la que cada usuario pueda ingresar su información personal y adaptar el comportamiento de Mauricio a sus necesidades.

---

## 🎙️ Reconocimiento por Wake Word (“Mauricio”)

Una de las características más distintivas de este proyecto es la detección de la palabra clave **“Mauricio”**, implementada mediante la plataforma **[Picovoice Porcupine](https://picovoice.ai/platform/porcupine/)**.

Gracias a esta tecnología, el asistente **permanece escuchando en segundo plano** y solo se activa cuando detecta su nombre, sin requerir conexión a internet.

### 🔧 Implementación técnica

- **Librería:** `pvporcupine`
- **Clave de acceso:** obtenida desde *Picovoice Console*
- **Archivo de palabra clave:** `wakewords/mauricio_en_windows_v3_0_0.ppn`
- **Plataforma:** Windows

Cuando Porcupine detecta el patrón de audio correspondiente a “Mauricio”, el asistente responde con voz (“Te escucho…”) y activa el reconocimiento de comandos.

Este sistema combina:
- 🧠 **Reconocimiento offline:** detección local de la wake word con Porcupine.  
- ☁️ **Reconocimiento online:** transcripción de comandos con Google Speech API.

---

## ⚙️ Funcionalidades principales

- 🎤 **Reconocimiento de voz:** escucha y transcribe comandos hablados en español (es-MX).  
- 🔊 **Síntesis de voz:** responde al usuario con voz natural mediante la clase `Voz`.  
- 🧠 **Procesamiento de comandos:** la clase `Mauricio` interpreta órdenes y ejecuta acciones.  
- 🎵 **Integración con Spotify:** controla reproducción, pausa, búsqueda de canciones y artistas.  
- 🕓 **Gestión de tiempo y alarmas:** crea recordatorios y alarmas usando `datetime` y `time`.  
- 🎧 **Grabación de voz:** graba y guarda archivos de audio `.wav` con `sounddevice` y `numpy`.  
- 💻 **Automatización del sistema:** abre programas o ejecuta comandos del sistema.  
- ⌨️ **Atajos de teclado:** permite detener grabaciones con combinaciones como `Alt + \``.  
- 🧵 **Ejecución en paralelo:** usa `threading` para escuchar, hablar y ejecutar acciones simultáneamente.

---

## 🧰 Librerías utilizadas

| Librería | Función principal |
|-----------|-------------------|
| `pvporcupine` | Detección local de la palabra clave “Mauricio” |
| `pyaudio`, `sounddevice` | Captura de audio desde el micrófono |
| `speech_recognition` | Reconocimiento de voz (Google Speech API) |
| `scipy.io.wavfile`, `numpy` | Procesamiento y guardado de grabaciones |
| `spotipy`, `SpotifyOAuth` | Control de la API de Spotify |
| `pygame.mixer` | Reproducción de audio local |
| `os`, `subprocess` | Ejecución de comandos del sistema |
| `keyboard` | Detección de combinaciones de teclas |
| `threading` | Multitarea para procesos simultáneos |
| `datetime`, `time` | Control de alarmas y temporizadores |
| `re`, `urllib.parse` | Procesamiento de texto y URLs |
| `comtypes.client` | Interacción con componentes COM de Windows |

---

## 🚀 Objetivo del proyecto

El objetivo de **Mauricio** es crear un asistente virtual **personalizable y extensible**, capaz de funcionar tanto en computadoras como en futuras versiones de aplicación.  
Combina **voz**, **automatización** y **conectividad** para brindar una experiencia de asistencia inteligente y adaptable al usuario.

---

## ⚡ Ejecución

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
2. Ejecuta el asistente:

python main.py

3. Di “Mauricio” para activarlo y comienza a interactuar 🎤
📌 Próximas mejoras
 - Interfaz visual para personalizar el asistente.
 - Integración con base de datos o DataStore para guardar configuraciones.
 - Sistema de aprendizaje básico (memoria de usuario).
 - Soporte multiplataforma (Windows / Android).
## 🧩 Arquitectura del proyecto

```plaintext
📁 Proyecto Mauricio
├── mauricio.py          # Lógica principal del asistente
├── voz.py               # Clase para la síntesis de voz
├── main.py              # Archivo principal con wake word y flujo de ejecución
├── utils/               # Módulos de soporte (alarma, hora, etc.)
├── wakewords/           # Modelos .ppn de Porcupine (palabra clave)
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación (este archivo)
```

💬 Créditos
Desarrollado por Giovas128
