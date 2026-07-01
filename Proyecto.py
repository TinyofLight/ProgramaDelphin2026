import cv2
import mediapipe as mp
from math import acos, degrees, hypot
from collections import deque
#IP + Port del servidor de la cámara IP de una aplicación de cámara IP (por ejemplo, IP Webcam en Android)
IP   = "192.xxx.x.xxx"
PORT = "8080"

UMBRAL_EXT_DEDO   = 10
UMBRAL_EXT_PULGAR = 5
ANGULO_GANCHO_MIN = 70
ANGULO_GANCHO_MAX = 140
ANGULO_L_MIN      = 60
ANGULO_L_MAX      = 120


def distanciaEuclidiana(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5


def extendido(tip, pip, muneca, margen=UMBRAL_EXT_DEDO):
    return distanciaEuclidiana(tip, muneca) > distanciaEuclidiana(pip, muneca) + margen


def angulo(a, vertice, b):
    v1 = (a[0] - vertice[0], a[1] - vertice[1])
    v2 = (b[0] - vertice[0], b[1] - vertice[1])
    mag1, mag2 = hypot(*v1), hypot(*v2)
    if mag1 == 0 or mag2 == 0:
        return 180.0
    cos_ang = (v1[0]*v2[0] + v1[1]*v2[1]) / (mag1 * mag2)
    cos_ang = max(-1.0, min(1.0, cos_ang))
    return degrees(acos(cos_ang))


def drawBoundingBox(imagen, hand_landmarks, image_width, image_height):
    x_min, y_min = image_width, image_height
    x_max, y_max = 0, 0
    for landmark in hand_landmarks.landmark:
        x = int(landmark.x * image_width)
        y = int(landmark.y * image_height)
        if x < x_min: x_min = x
        if y < y_min: y_min = y
        if x > x_max: x_max = x
        if y > y_max: y_max = y
    cv2.rectangle(imagen, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)


def clasificarLetra(lm, muneca):
    indice_tip = lm['indice_tip']; indice_pip = lm['indice_pip']
    indice_dip = lm['indice_dip']; indice_mcp = lm['indice_mcp']
    pulgar_tip = lm['pulgar_tip']
    mayor_tip  = lm['mayor_tip'];  mayor_pip  = lm['mayor_pip']
    anular_tip = lm['anular_tip']; anular_pip = lm['anular_pip']
    menique_tip = lm['menique_tip']; menique_pip = lm['menique_pip']

    indice_ext  = extendido(indice_tip, indice_pip, muneca)
    mayor_ext   = extendido(mayor_tip, mayor_pip, muneca)
    anular_ext  = extendido(anular_tip, anular_pip, muneca)
    menique_ext = extendido(menique_tip, menique_pip, muneca)
    pulgar_ext  = extendido(pulgar_tip, lm['pulgar_pip'], muneca, margen=UMBRAL_EXT_PULGAR)

    dist_4_8 = distanciaEuclidiana(pulgar_tip, indice_tip)

    #LETRA B
    if (indice_tip[1] < indice_pip[1]
            and mayor_tip[1] < mayor_pip[1]
            and anular_tip[1] < anular_pip[1]
            and menique_tip[1] < menique_pip[1]
            and (pulgar_tip[0] > indice_pip[0] or pulgar_tip[0] < indice_tip[0])):  # <--- Evalúa ambos lados
        return 'B'

    #LETRA C
    elif (indice_tip[1] > indice_pip[1]
            and mayor_tip[1] > mayor_pip[1]
            and anular_tip[1] > anular_pip[1]
            and menique_tip[1] > menique_pip[1]
            and (100 < dist_4_8 < 220)):  # Rango del arco
        return 'C'

    #LETRA D
    elif (indice_tip[1] < indice_pip[1]
            and mayor_tip[1] > mayor_pip[1]
            and anular_tip[1] > anular_pip[1]
            and menique_tip[1] > menique_pip[1]
            and abs(pulgar_tip[1] - mayor_tip[1]) < 40):
        return 'D'

    # Letra L
    elif (pulgar_ext and indice_ext and not mayor_ext and not anular_ext and not menique_ext
            and ANGULO_L_MIN <= angulo(pulgar_tip, muneca, indice_tip) <= ANGULO_L_MAX):
        return 'L'

    # Letra X
    elif (not mayor_ext and not anular_ext and not menique_ext and not indice_ext
            and ANGULO_GANCHO_MIN <= angulo(indice_mcp, indice_pip, indice_dip) <= ANGULO_GANCHO_MAX):
        return 'X'

    return None


# Letra Z (rastreo del trazo, no es una postura fija) 
class RastreadorZ:
    def __init__(self, max_puntos=40, frames_tolerancia=6, umbral_px=40):
        self.puntos = deque(maxlen=max_puntos)
        self.frames_sin_pose = 0
        self.frames_tolerancia = frames_tolerancia
        self.umbral_px = umbral_px

    def actualizar(self, modo_z_activo, punta_indice):
        if modo_z_activo:
            self.puntos.append(punta_indice)
            self.frames_sin_pose = 0
        else:
            self.frames_sin_pose += 1
            if self.frames_sin_pose > self.frames_tolerancia:
                self.puntos.clear()

    def revisar_y_resetear(self):
        if len(self.puntos) < 9:
            return False
        pts = list(self.puntos)
        n = len(pts)
        t1, t2, t3 = pts[:n // 3], pts[n // 3: 2 * n // 3], pts[2 * n // 3:]
        dx1 = t1[-1][0] - t1[0][0]
        dx2 = t2[-1][0] - t2[0][0]
        dy2 = t2[-1][1] - t2[0][1]
        dx3 = t3[-1][0] - t3[0][0]
        patron_z = (dx1 > self.umbral_px
                    and dx2 < -self.umbral_px * 0.5 and dy2 > 0
                    and dx3 > self.umbral_px)
        if patron_z:
            self.puntos.clear()
            return True
        return False


mp_drawing        = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands          = mp.solutions.hands
#setup de la cámara IP, para cambiar la resolución, modificar los valores de CAP_PROP_FRAME_WIDTH y CAP_PROP_FRAME_HEIGHT
cap = cv2.VideoCapture(f"http://{IP}:{PORT}/videofeed")
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

rastreador_z = RastreadorZ()
frames_mostrar_z = 0

with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        h, w, _ = image.shape

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                drawBoundingBox(image, hand_landmarks, w, h)

                def px(idx):
                    l = hand_landmarks.landmark[idx]
                    return (int(l.x * w), int(l.y * h))

                lm = {
                    'indice_tip': px(8),  'indice_pip': px(6),
                    'indice_dip': px(7),  'indice_mcp': px(5),
                    'pulgar_tip': px(4),  'pulgar_pip': px(2),
                    'mayor_tip':  px(12), 'mayor_pip':  px(10),
                    'anular_tip': px(16), 'anular_pip': px(14),
                    'menique_tip': px(20), 'menique_pip': px(18),
                }
                muneca = px(0)

                # Letra Z
                indice_ext_z  = extendido(lm['indice_tip'], lm['indice_pip'], muneca)
                mayor_ext_z   = extendido(lm['mayor_tip'], lm['mayor_pip'], muneca)
                anular_ext_z  = extendido(lm['anular_tip'], lm['anular_pip'], muneca)
                menique_ext_z = extendido(lm['menique_tip'], lm['menique_pip'], muneca)
                modo_z_activo = indice_ext_z and not mayor_ext_z and not anular_ext_z and not menique_ext_z

                rastreador_z.actualizar(modo_z_activo, lm['indice_tip'])
                if rastreador_z.revisar_y_resetear():
                    frames_mostrar_z = 20

                if frames_mostrar_z > 0:
                    letra = 'Z'
                    frames_mostrar_z -= 1
                else:
                    letra = clasificarLetra(lm, muneca)

                if letra:
                    cv2.putText(image, letra, (700, 150),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                3, (0, 0, 255), 6)

        cv2.imshow('Manos', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()