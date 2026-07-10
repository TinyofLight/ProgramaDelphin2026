class RastreadorK:

    def __init__(self):

        self.frames = 0

    def actualizar(self, es_k):

        if es_k:
            self.frames = 25

    def obtener_letra(self):

        if self.frames > 0:
            self.frames -= 1
            return "K"

        return None