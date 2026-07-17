import pyttsx3
import pythoncom


class Voz:

    def __init__(self):

        self.velocidad = 125
        self.volumen = 1.0

    def hablar(self, texto):

        pythoncom.CoInitialize()

        engine = None

        try:

            if hasattr(pyttsx3, "_activeEngines"):
                pyttsx3._activeEngines.clear()

            engine = pyttsx3.init(driverName="sapi5")

            engine.setProperty("rate", self.velocidad)
            engine.setProperty("volume", self.volumen)

            print("HABLANDO:", texto)

            engine.say(texto)
            engine.runAndWait()

        finally:

            if engine is not None:
                del engine

            pythoncom.CoUninitialize()