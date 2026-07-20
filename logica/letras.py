from logica.geometria import distancia_x, distancia_y, distancia_euclidiana, extendido, angulo

from config import (
    DIST_C_MIN,
    DIST_C_MAX,
    DIF_PULGAR_MAYOR,
    DIST_PULGAR_INDICE_I,
    DIST_PULGAR_INDICE_K,
    DIST_PULGAR_MCP_L,
    DIST_PULGAR_INDICE_L,
    PULGAR_VERTICAL_L,
    DIST_PULGAR_MCP_P,
    MARGEN_PULGAR_P
)

# ----------------------------
# Clasificación de letras
# ----------------------------
def clasificar_letra(lm, muneca):
    indice_tip = lm['indice_tip']
    indice_pip = lm['indice_pip']
    indice_dip = lm['indice_dip']
    indice_mcp = lm['indice_mcp']

    mayor_tip  = lm['mayor_tip']
    mayor_pip  = lm['mayor_pip']
    mayor_dip  = lm['mayor_dip']
    mayor_mcp  = lm['mayor_mcp']

    anular_tip = lm['anular_tip']
    anular_pip = lm['anular_pip']
    anular_dip = lm['anular_dip']
    anular_mcp = lm['anular_mcp']

    menique_tip = lm['menique_tip']
    menique_pip = lm['menique_pip']
    menique_dip = lm['menique_dip']
    menique_mcp = lm['menique_mcp']

    pulgar_tip = lm['pulgar_tip']
    pulgar_pip = lm['pulgar_pip']

    pulgar_ext = extendido(pulgar_tip, pulgar_pip, muneca)
    indice_ext = extendido(indice_tip, indice_pip, muneca)
    mayor_ext = extendido(mayor_tip, mayor_pip, muneca)
    anular_ext = extendido(anular_tip, anular_pip, muneca)
    menique_ext = extendido(menique_tip, menique_pip, muneca)


    # ---------------- LETRA A ----------------
    if (not menique_ext
        and not anular_ext
        and not mayor_ext
        and not indice_ext
        and pulgar_ext):

        return "A"

    # ---------------- LETRA B ----------------
    if (menique_ext
        and anular_ext
        and mayor_ext
        and indice_ext
        and not pulgar_ext):
        
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
    

    # ---------------- LETRA E ----------------
    if (not menique_ext
        and not anular_ext
        and not mayor_ext
        and not indice_ext
        and not pulgar_ext
        and distancia_y(menique_tip, menique_mcp) > 0
        and distancia_y(anular_tip, anular_mcp) > 0
        and distancia_y(mayor_tip, mayor_mcp) > 0
        and distancia_y(indice_tip, indice_mcp)):

        return "E"


    # ---------------- LETRA F ----------------
    if (menique_ext
        and anular_ext
        and mayor_ext
        and not indice_ext 
        and abs(distancia_x(indice_pip, pulgar_tip)) < 50
        and abs(distancia_x(menique_tip, anular_pip)) < 60
        and abs(distancia_x(anular_tip, mayor_tip)) < 60):

        return "F"
    


    # ---------------- LETRA I ----------------
    if (
        menique_ext
        and not anular_ext
        and not mayor_ext
        and not indice_ext
        and distancia_euclidiana(pulgar_tip, indice_pip) < DIST_PULGAR_INDICE_I
    ):
    
        return "I"

    
    # ---------------- LETRA K ----------------
    if (
    
        indice_tip[1] > indice_pip[1]
    
        and mayor_tip[1] > mayor_pip[1]
    
        and anular_pip[1] > anular_tip[1]
    
        and menique_pip[1] > menique_tip[1]
    
        and pulgar_pip[1] < pulgar_tip[1]
    
        and distancia_euclidiana(
            pulgar_tip,
            indice_tip
        ) > DIST_PULGAR_INDICE_K
    
    ):
    
        return "K"

# ---------------- LETRA L ----------------
    if (
        distancia_y(indice_tip, indice_pip) < -40
        and distancia_y(mayor_tip, mayor_pip) > 20
        and distancia_y(anular_tip, anular_pip) > 20
        and distancia_y(menique_tip, menique_pip) > 20
        and abs(pulgar_tip[1] - pulgar_pip[1]) <  PULGAR_VERTICAL_L
        and distancia_euclidiana(pulgar_tip, lm["pulgar_mcp"]) > DIST_PULGAR_MCP_L
        and distancia_euclidiana(pulgar_tip, indice_tip) > DIST_PULGAR_INDICE_L
    ):
    
        return "L"
    
    #AP ---------------- LETRA M ----------------
    if (not indice_ext and not mayor_ext and not anular_ext and not menique_ext and not pulgar_ext
        and distancia_x(pulgar_tip, indice_tip) < 55
        and distancia_x(pulgar_tip, mayor_tip) < 55
        and distancia_x(pulgar_tip, anular_tip) < 55
        and distancia_x(pulgar_tip, menique_tip) < 55):
            
        return "M"    
    
    #AP ---------------- LETRA N ----------------
    if (not indice_ext and not mayor_ext and not anular_ext and not menique_ext and not pulgar_ext
        and distancia_x(pulgar_tip, indice_pip) < 45
        and distancia_x(pulgar_tip, mayor_pip) < 45
        and distancia_x(pulgar_tip, indice_tip) > 25
        and distancia_x(pulgar_tip, mayor_tip) > 25):
            
        return "N"

    #AP ---------------- LETRA O ----------------
    if (not indice_ext and not mayor_ext and not anular_ext and not menique_ext and not pulgar_ext
        and distancia_x(pulgar_tip, indice_tip) < 40
        and distancia_x(indice_tip, mayor_tip) < 35
        and distancia_x(mayor_tip, anular_tip) < 35):
            
        return "O"
    
    # ---------------- LETRA P ----------------

   
    if (
    
        indice_tip[1] < indice_pip[1]
    
        and mayor_tip[1] < mayor_pip[1]
    
        and anular_tip[1] > anular_pip[1]
    
        and menique_tip[1] > menique_pip[1]
    
        and pulgar_tip[1] < pulgar_pip[1]
    
        and distancia_euclidiana(
            pulgar_tip,
            lm["pulgar_mcp"]
        ) > DIST_PULGAR_MCP_P
    
        and min(indice_pip[0], mayor_pip[0]) - MARGEN_PULGAR_P
            < pulgar_tip[0] <
            max(indice_pip[0], mayor_pip[0]) + MARGEN_PULGAR_P
    
        and min(indice_pip[1], mayor_pip[1]) - MARGEN_PULGAR_P
            < pulgar_tip[1] <
            max(indice_pip[1], mayor_pip[1]) + MARGEN_PULGAR_P
    
    ):
    
        return "P"
    
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
    if (
        menique_ext
        and not anular_ext
        and not mayor_ext
        and not indice_ext
        and pulgar_ext
        and distancia_euclidiana(pulgar_tip, indice_tip) > 140
    ):
    
        return "Y"


    return None