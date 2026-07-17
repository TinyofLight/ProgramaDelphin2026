import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 125)

engine.say("Hola. Esta es una prueba de voz.")
print("hola")
engine.runAndWait()