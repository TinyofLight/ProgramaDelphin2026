from collections import deque


class RastreadorZ:
    def __init__(self, max_puntos=40, frames_tolerancia=6, umbral_px=40):
        self.puntos = deque(maxlen=max_puntos)
        self.frames_sin_pose = 0
        self.frames_tolerancia = frames_tolerancia
        self.umbral_px = umbral_px


    # ----------------------------
    # Actualizar trayectoria
    # ----------------------------
    def actualizar(self, modo_z_activo, punta_indice):
        if modo_z_activo:
            self.puntos.append(punta_indice)
            self.frames_sin_pose = 0
        else:
            self.frames_sin_pose += 1
            if self.frames_sin_pose > self.frames_tolerancia:
                self.puntos.clear()


    # ----------------------------
    # Detectar patrón Z
    # ----------------------------
    def revisar_y_resetear(self):
        if len(self.puntos) < 9:
            return False

        pts = list(self.puntos)
        n = len(pts)

        t1 = pts[:n // 3]
        t2 = pts[n // 3: 2 * n // 3]
        t3 = pts[2 * n // 3:]

        dx1 = t1[-1][0] - t1[0][0]
        dx2 = t2[-1][0] - t2[0][0]
        dy2 = t2[-1][1] - t2[0][1]
        dx3 = t3[-1][0] - t3[0][0]

        patron_z = (
            dx1 > self.umbral_px and
            dx2 < -self.umbral_px * 0.5 and
            dy2 > 0 and
            dx3 > self.umbral_px
        )

        if patron_z:
            self.puntos.clear()
            return True

        return False