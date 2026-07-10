from collections import deque

from config import (
    J_MAX_PUNTOS,
    J_UMBRAL_BAJADA,
    J_UMBRAL_SUBIDA,
    J_FRAMES_MOSTRAR,
    J_UMBRAL_HORIZONTAL
)

class RastreadorJ:

    def __init__(
    self,
        max_puntos=J_MAX_PUNTOS,
        umbral_bajada=J_UMBRAL_BAJADA,
        umbral_subida=J_UMBRAL_SUBIDA,
        umbral_horizontal=J_UMBRAL_HORIZONTAL,
        frames_mostrar=J_FRAMES_MOSTRAR,
        frames_tolerancia=6
    ):

        self.trayectoria = deque(maxlen=max_puntos)

        self.estado = "inicio"

        self.umbral_bajada = umbral_bajada
        self.umbral_subida = umbral_subida
        self.umbral_horizontal = umbral_horizontal

        self.frames_mostrar = frames_mostrar
        self.frames_restantes = 0
        self.frames_sin_pose = 0
        self.frames_tolerancia = frames_tolerancia


    # ---------------------------------
    # Actualizar trayectoria
    # ---------------------------------

    def actualizar(self, modo_j, punto):

        if not modo_j:

            self.frames_sin_pose += 1
        
            if self.frames_sin_pose > self.frames_tolerancia:
        
                self.trayectoria.clear()
                self.estado = "inicio"
        
            return
        
        self.frames_sin_pose = 0

        self.trayectoria.append(punto)

        if len(self.trayectoria) < 10:
            return

        dy = self.trayectoria[-1][1] - self.trayectoria[-2][1]
        


        if self.estado == "inicio":

            if dy > self.umbral_bajada:
                self.estado = "bajando"


        elif self.estado == "bajando":

            if dy < self.umbral_subida:
                self.estado = "subiendo"


        elif self.estado == "subiendo":

            if abs(self.trayectoria[-1][0] - self.trayectoria[-5][0]) > self.umbral_horizontal:

                self.frames_restantes = self.frames_mostrar

                self.trayectoria.clear()
                self.estado = "inicio"


    # ---------------------------------
    # Mostrar letra J
    # ---------------------------------

    def obtener_letra(self):

        if self.frames_restantes > 0:

            self.frames_restantes -= 1
            return "J"

        return None