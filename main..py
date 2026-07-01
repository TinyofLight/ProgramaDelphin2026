import cv2

from config import CAMERA_MODE, CAMERA_SOURCE, VIDEO_URL, FRAME_WIDTH, FRAME_HEIGHT
from vision.manos import DetectorManos
from logica.letras import clasificar_letra
from tracking.rastreador_z import RastreadorZ


# ----------------------------
# INICIALIZAR CÁMARA
# ----------------------------
if CAMERA_MODE == "pc":
    cap = cv2.VideoCapture(CAMERA_SOURCE)
else:
    cap = cv2.VideoCapture(VIDEO_URL)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)


# ----------------------------
# MÓDULOS
# ----------------------------
detector = DetectorManos()
rastreador_z = RastreadorZ()

frames_mostrar_z = 0


# ----------------------------
# LOOP PRINCIPAL
# ----------------------------
while cap.isOpened():

    success, frame = cap.read()
    if not success:
        continue

    h, w, _ = frame.shape


    # ----------------------------
    # DETECCIÓN DE MANOS
    # ----------------------------
    frame, results = detector.procesar(frame)


    letra_detectada = None


    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            detector.dibujar(frame, hand_landmarks)

            lm = detector.obtener_puntos(hand_landmarks, w, h)
            muneca = lm['indice_mcp']  # aproximación de muñeca


            # ----------------------------
            # LETRA Z (tracking)
            # ----------------------------
            indice_ext_z = True  # simplificado (puedes mejorar luego)

            modo_z_activo = (
                lm['indice_tip'][1] < lm['indice_pip'][1]
            )

            rastreador_z.actualizar(modo_z_activo, lm['indice_tip'])

            if rastreador_z.revisar_y_resetear():
                frames_mostrar_z = 20


            if frames_mostrar_z > 0:
                letra_detectada = "Z"
                frames_mostrar_z -= 1
            else:
                # ----------------------------
                # RESTO DE LETRAS
                # ----------------------------
                letra_detectada = clasificar_letra(lm, muneca)


            # ----------------------------
            # MOSTRAR LETRA
            # ----------------------------
            if letra_detectada:
                cv2.putText(
                    frame,
                    letra_detectada,
                    (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    3,
                    (0, 0, 255),
                    6
                )


    # ----------------------------
    # MOSTRAR FRAME
    # ----------------------------
    cv2.imshow("Programa Delphin 2026", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ----------------------------
# LIMPIEZA
# ----------------------------
cap.release()
cv2.destroyAllWindows()