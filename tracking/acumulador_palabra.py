from config import (
    ACUM_FRAMES_CONFIRMACION,
    ACUM_FRAMES_PAUSA
)


class AcumuladorPalabra:
    """
    Acumula letras detectadas para formar una palabra.

    - Una letra solo se "confirma" si se mantiene estable durante
      ACUM_FRAMES_CONFIRMACION frames seguidos (evita ruido/parpadeos).
    - No repite la misma letra dos veces seguidas (para no llenar
      la palabra de "AAAA" si mantienes la seña quieta).
    - Si no se detecta ninguna letra durante ACUM_FRAMES_PAUSA frames
      (ej. quitas la mano de cuadro), considera la palabra terminada,
      la regresa y reinicia el acumulador.
    """

    def __init__(
        self,
        frames_confirmacion=ACUM_FRAMES_CONFIRMACION,
        frames_pausa=ACUM_FRAMES_PAUSA
    ):
        self.frames_confirmacion = frames_confirmacion
        self.frames_pausa = frames_pausa

        self.letra_actual = None
        self.frames_letra_actual = 0

        self.ultima_letra_confirmada = None
        self.palabra = []

        self.frames_sin_letra = 0


    # ----------------------------
    # Actualizar con la letra del frame actual
    # ----------------------------
    def actualizar(self, letra_detectada):
        """
        Devuelve la palabra completa (str) si se acaba de cerrar
        por pausa, o None si sigue en construcción.
        """

        if letra_detectada is None:

            self.frames_sin_letra += 1
            self.letra_actual = None
            self.frames_letra_actual = 0

            if self.frames_sin_letra == self.frames_pausa and self.palabra:

                palabra_final = "".join(self.palabra)

                self.palabra = []
                self.ultima_letra_confirmada = None

                return palabra_final

            return None

        self.frames_sin_letra = 0

        if letra_detectada == self.letra_actual:
            self.frames_letra_actual += 1
        else:
            self.letra_actual = letra_detectada
            self.frames_letra_actual = 1

        if (
            self.frames_letra_actual == self.frames_confirmacion
            and letra_detectada != self.ultima_letra_confirmada
        ):
            self.palabra.append(letra_detectada)
            self.ultima_letra_confirmada = letra_detectada

        return None


    # ----------------------------
    # Palabra en construcción (para mostrar en pantalla)
    # ----------------------------
    def obtener_palabra_actual(self):
        return "".join(self.palabra)


    # ----------------------------
    # Reiniciar manualmente (ej. tecla de "borrar")
    # ----------------------------
    def reiniciar(self):
        self.letra_actual = None
        self.frames_letra_actual = 0
        self.ultima_letra_confirmada = None
        self.palabra = []
        self.frames_sin_letra = 0