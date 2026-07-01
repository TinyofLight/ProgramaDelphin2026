import cv2
import mediapipe as mp


class DetectorManos:
    def __init__(self, model_complexity=1,
                 min_detection_confidence=0.7,
                 min_tracking_confidence=0.7,
                 max_num_hands=2):

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            max_num_hands=max_num_hands
        )


    # ----------------------------
    # Procesar frame
    # ----------------------------
    def procesar(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False

        results = self.hands.process(frame_rgb)

        frame_rgb.flags.writeable = True
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        return frame_bgr, results


    # ----------------------------
    # Dibujar manos
    # ----------------------------
    def dibujar(self, frame, hand_landmarks):
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_styles.get_default_hand_landmarks_style(),
            self.mp_styles.get_default_hand_connections_style()
        )


    # ----------------------------
    # Convertir landmarks a pixeles
    # ----------------------------
    def obtener_puntos(self, hand_landmarks, w, h):
        def px(idx):
            lm = hand_landmarks.landmark[idx]
            return (int(lm.x * w), int(lm.y * h))

        return {
            'indice_tip': px(8),
            'indice_pip': px(6),
            'indice_dip': px(7),
            'indice_mcp': px(5),

            'pulgar_tip': px(4),
            'pulgar_pip': px(2),

            'mayor_tip': px(12),
            'mayor_pip': px(10),

            'anular_tip': px(16),
            'anular_pip': px(14),

            'menique_tip': px(20),
            'menique_pip': px(18),
        }