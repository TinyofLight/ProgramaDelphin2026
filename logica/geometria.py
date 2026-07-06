from math import acos, degrees, hypot

# ----------------------------
# Distancia Euclidiana
# ----------------------------
def distancia_euclidiana(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5

#-----------------------------
# Distancia en x
#-----------------------------
def distancia_x(p1, p2):
    return (p2[0] - p1[0])

#-----------------------------
# Distancia en y
#-----------------------------
def distancia_y(p1, p2):
    return (p2[1] - p1[1])

# ----------------------------
# Extensión de dedo
# ----------------------------
def extendido(tip, pip, muneca, margen=10):
    return distancia_euclidiana(tip, muneca) > distancia_euclidiana(pip, muneca) + margen


# ----------------------------
# Ángulo entre 3 puntos
# ----------------------------
def angulo(a, vertice, b):
    v1 = (a[0] - vertice[0], a[1] - vertice[1])
    v2 = (b[0] - vertice[0], b[1] - vertice[1])

    mag1, mag2 = hypot(*v1), hypot(*v2)

    if mag1 == 0 or mag2 == 0:
        return 180.0

    cos_ang = (v1[0]*v2[0] + v1[1]*v2[1]) / (mag1 * mag2)
    cos_ang = max(-1.0, min(1.0, cos_ang))

    return degrees(acos(cos_ang))