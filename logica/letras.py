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

    pulgar_ext = extendido(pulgar_tip, pulgar_pip, muneca)
    indice_ext = extendido(indice_tip, indice_pip, muneca)
    mayor_ext = extendido(mayor_tip, mayor_pip, muneca)
    anular_ext = extendido(anular_tip, anular_pip, muneca)
    menique_ext = extendido(menique_tip, menique_pip, muneca)

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
    if (pulgar_ext and indice_ext
        and not extendido(mayor_tip, mayor_pip, muneca)
        and not extendido(anular_tip, anular_pip, muneca)
        and not extendido(menique_tip, menique_pip, muneca)
        and 60 <= angulo(pulgar_tip, muneca, indice_tip) <= 120):

        return "L"
    
    # ---------------- LETRA U ----------------
    if (not menique_ext
        and not anular_ext
        and mayor_ext
        and indice_ext
        and pulgar_tip[0] - mayor_tip[0] < 0    # Comprobar posicion del pulgar
        and indice_tip[0] - mayor_tip[0] > 20   # Comprobar que los dedos esten juntos
        and indice_tip[0] - mayor_tip[0]  < 50):

        return "U"
    

    # ---------------- LETRA V ----------------
    if (not menique_ext
        and not anular_ext
        and mayor_ext
        and indice_ext
        and pulgar_tip[0] - mayor_tip[0] < 0    # Comprobar posicion del pulgar
        and indice_tip[0] - mayor_tip[0] > 50): # Separacion de los dedos

        return "V"
        
    
    # ---------------- LETRA W ----------------
    if (not menique_ext
        and anular_ext
        and mayor_ext
        and indice_ext
        and pulgar_tip[0] - anular_pip[0] < 0  # Comprobar posicion del pulgar
        and indice_tip[0] - mayor_tip[0]  > 50  # comprobar separacion entre los dedos indice, mayor y anular
        and mayor_tip[0] - anular_tip[0] > 50):
        
        return "W"


    # ---------------- LETRA X ----------------
    if (indice_ext
        and not extendido(mayor_tip, mayor_pip, muneca)
        and not extendido(anular_tip, anular_pip, muneca)
        and not extendido(menique_tip, menique_pip, muneca)
        and 70 <= angulo(indice_tip, indice_pip, lm['indice_dip']) <= 140):

        return "X"


    # ---------------- LETRA Y ----------------
    if (menique_ext
        and not anular_ext
        and not mayor_ext
        and not indice_ext
        and pulgar_ext):
        
        return "Y"


    return None