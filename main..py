import cv2

from config import CAMERA_MODE, CAMERA_SOURCE, VIDEO_URL, FRAME_WIDTH, FRAME_HEIGHT,DIST_PULGAR_INDICE_I
from vision.manos import DetectorManos
from logica.letras import clasificar_letra
from tracking.rastreador_z import RastreadorZ
from tracking.rastreador_j import RastreadorJ
from logica.geometria import distancia_euclidiana, extendido
from tracking.rastreador_k import RastreadorK
from audio.gestor_voz import GestorVoz

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
rastreador_j = RastreadorJ()
rastreador_k = RastreadorK()
gestor_voz = GestorVoz()

frames_mostrar_z = 0


# ----------------------------
# LOOP PRINCIPAL
# ----------------------------
while cap.isOpened():

    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
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
            muneca = lm['muneca']  # aproximación de muñeca
            
            pulgar_ext = extendido(
                lm["pulgar_tip"],
                lm["pulgar_pip"],
                muneca
            )
            
            indice_ext = extendido(
                lm["indice_tip"],
                lm["indice_pip"],
                muneca
            )
            
            mayor_ext = extendido(
                lm["mayor_tip"],
                lm["mayor_pip"],
                muneca
            )
            
            anular_ext = extendido(
                lm["anular_tip"],
                lm["anular_pip"],
                muneca
            )
            
            menique_ext = extendido(
                lm["menique_tip"],
                lm["menique_pip"],
                muneca
            )

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


            # ----------------------------
            # MOSTRAR Z
            # ----------------------------
            if frames_mostrar_z > 0:
            
                letra_detectada = "Z"
                frames_mostrar_z -= 1
            
            else:
            
                # ----------------------------
                # ¿Está haciendo la posición de la I?
                # ----------------------------
            
                modo_j = (
                    menique_ext
                    and not indice_ext
                    and not mayor_ext
                    and not anular_ext
                    
                    and distancia_euclidiana(lm["pulgar_tip"], lm["indice_pip"]) < DIST_PULGAR_INDICE_I
                )
                rastreador_j.actualizar(
                    modo_j,
                    lm["menique_tip"]
                )
            
                letra_detectada = rastreador_j.obtener_letra()
            
                if letra_detectada is None:
            
                    letra_detectada = clasificar_letra(
                        lm,
                        muneca
                    )
                
                # ----------------------------
                # RASTREADOR K
                # ----------------------------
                rastreador_k.actualizar(letra_detectada == "K")
                
                k = rastreador_k.obtener_letra()
                
                if k is not None:
                    letra_detectada = k

            # ----------------------------
            # VOZ
            # ----------------------------
            
            gestor_voz.actualizar(letra_detectada)
            
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