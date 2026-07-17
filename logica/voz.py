import threading
import queue

import pyttsx3

from config import VOZ_VELOCIDAD


class MotorVoz:
    """
    Motor de texto a voz (TTS) que corre en un hilo separado.

    OpenCV necesita que el loop principal siga leyendo frames de la
    cámara sin interrupciones; pyttsx3 es bloqueante mientras habla,
    así que aquí se manda el texto a una cola y un hilo aparte se
    encarga de reproducirlo sin trabar la ventana de video.
    """

    def __init__(self, velocidad=VOZ_VELOCIDAD):
        self._cola = queue.Queue()
        self._velocidad = velocidad

        self._hilo = threading.Thread(target=self._procesar, daemon=True)
        self._hilo.start()


    # ----------------------------
    # Hilo de fondo: consume la cola y habla
    # ----------------------------
    def _procesar(self):
        # En Windows, pyttsx3 usa SAPI5 (COM) por debajo. Como este
        # método corre en un hilo aparte del principal, Windows no lo
        # tiene registrado para usar COM y el audio simplemente no
        # suena (sin marcar error). Lo registramos manualmente aquí.
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass  # no estamos en Windows, no hace falta

        motor = pyttsx3.init()
        motor.setProperty('rate', self._velocidad)

        while True:
            texto = self._cola.get()

            if texto is None:
                break

            motor.say(texto)
            motor.runAndWait()


    # ----------------------------
    # Encolar texto para decir
    # ----------------------------
    def decir(self, texto):
        if texto:
            self._cola.put(texto)


    # ----------------------------
    # Apagar el hilo (llamar al cerrar el programa)
    # ----------------------------
    def detener(self):
        self._cola.put(None)