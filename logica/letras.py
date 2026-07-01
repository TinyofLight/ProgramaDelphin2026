from logica.geometria import distancia_euclidiana, extendido, angulo


# ----------------------------
# Clasificación de letras
# ----------------------------
def clasificar_letra(lm, muneca):
    indice_tip = lm['indice_tip']
    indice_pip = lm['indice_pip']

    mayor_tip  = lm['mayor_tip']
    mayor_pip  = lm['mayor_pip']

    anular_tip = lm['anular_tip']
    anular_pip = lm['anular_pip']

    menique_tip = lm['menique_tip']
    menique_pip = lm['menique_pip']

    pulgar_tip = lm['pulgar_tip']
    pulgar_pip = lm['pulgar_pip']


    # ---------------- LETRA B ----------------
    if (indice_tip[1] < indice_pip[1]
        and mayor_tip[1] < mayor_pip[1]
        and anular_tip[1] < anular_pip[1]
        and menique_tip[1] < menique_pip[1]):

        return "B"


    # ---------------- LETRA C ----------------
    dist = distancia_euclidiana(pulgar_tip, indice_tip)

    if (indice_tip[1] > indice_pip[1]
        and mayor_tip[1] > mayor_pip[1]
        and anular_tip[1] > anular_pip[1]
        and menique_tip[1] > menique_pip[1]
        and 100 < dist < 220):

        return "C"


    # ---------------- LETRA D ----------------
    if (indice_tip[1] < indice_pip[1]
        and mayor_tip[1] > mayor_pip[1]
        and anular_tip[1] > anular_pip[1]
        and menique_tip[1] > menique_pip[1]
        and abs(pulgar_tip[1] - mayor_tip[1]) < 40):

        return "D"


    # ---------------- LETRA L ----------------
    indice_ext = extendido(indice_tip, indice_pip, muneca)
    pulgar_ext = extendido(pulgar_tip, pulgar_pip, muneca)

    if (pulgar_ext and indice_ext
        and not extendido(mayor_tip, mayor_pip, muneca)
        and not extendido(anular_tip, anular_pip, muneca)
        and not extendido(menique_tip, menique_pip, muneca)
        and 60 <= angulo(pulgar_tip, muneca, indice_tip) <= 120):

        return "L"


    # ---------------- LETRA X ----------------
    indice_ext = extendido(indice_tip, indice_pip, muneca)

    if (indice_ext
        and not extendido(mayor_tip, mayor_pip, muneca)
        and not extendido(anular_tip, anular_pip, muneca)
        and not extendido(menique_tip, menique_pip, muneca)
        and 70 <= angulo(indice_tip, indice_pip, lm['indice_dip']) <= 140):

        return "X"


    return None