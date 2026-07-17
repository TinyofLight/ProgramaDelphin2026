from audio.voz import Voz
import threading

class GestorVoz:

    def __init__(self, tiempo_estable=60):

        self.voz = Voz()

        self.tiempo_estable = tiempo_estable

        self.letra_actual = None

        self.frames = 0

        self.letra_hablada = None

        self.letras_movimiento = ["J", "K", "Z"]


    def actualizar(self, letra):


        # ----------------------------
        # No hay letra
        # ----------------------------

        if letra is None:

            self.letra_actual = None

            self.frames = 0

            self.letra_hablada = None

            return


        # ----------------------------
        # Letras con movimiento
        # ----------------------------

        if letra in self.letras_movimiento:

            if self.letra_hablada != letra:

                threading.Thread(
                    target=self.voz.hablar,
                    args=(f"La letra detectada es {letra}",),
                    daemon=True
                ).start()
                self.letra_hablada = letra

            return


        # ----------------------------
        # Cambió de letra
        # ----------------------------

        if letra != self.letra_actual:

            self.letra_actual = letra

            self.frames = 0

            return


        # ----------------------------
        # Sigue la misma letra
        # ----------------------------

        self.frames += 1


        # ----------------------------
        # Hablar
        # ----------------------------

        if self.frames >= self.tiempo_estable:

            if self.letra_hablada != letra:

                threading.Thread(
                    target=self.voz.hablar,
                    args=(f"La letra detectada es {letra}",),
                    daemon=True
                ).start()

                self.letra_hablada = letra