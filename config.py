# ----------------------------
# CONFIGURACIÓN DE CÁMARA
# ----------------------------

CAMERA_SOURCE = 0

IP = "192.168.0.231"
PORT = "8080"
VIDEO_URL = f"http://{IP}:{PORT}/videofeed"

CAMERA_MODE = "pc"  # "pc" o "cel"

FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080


# ----------------------------
# UMBRALES GENERALES
# ----------------------------

UMBRAL_EXT_DEDO = 10
UMBRAL_EXT_PULGAR = 5


# ----------------------------
# ÁNGULOS
# ----------------------------

ANGULO_GANCHO_MIN = 70
ANGULO_GANCHO_MAX = 140

ANGULO_L_MIN = 60
ANGULO_L_MAX = 120


# ----------------------------
# LETRA C
# ----------------------------

DIST_C_MIN = 100
DIST_C_MAX = 220


# ----------------------------
# LETRA D
# ----------------------------

DIF_PULGAR_MAYOR = 40



# ---------- I ----------
DIST_PULGAR_INDICE_I = 60


# ---------- J ----------
J_MAX_PUNTOS = 20
J_UMBRAL_BAJADA = 5
J_UMBRAL_SUBIDA = -8
J_UMBRAL_HORIZONTAL = 15
J_FRAMES_MOSTRAR = 20


# ---------- K ----------
DIST_PULGAR_INDICE_K = 50


# ---------- L ----------
DIST_PULGAR_MCP_L = 70
DIST_PULGAR_INDICE_L = 120
PULGAR_VERTICAL_L = 35


# ---------- P ----------
DIST_PULGAR_MCP_P = 70
MARGEN_PULGAR_P = 20


# ----------------------------
# ACUMULADOR DE PALABRA
# ----------------------------

# Frames que una letra debe mantenerse estable para confirmarse
ACUM_FRAMES_CONFIRMACION = 15

# Frames sin detectar ninguna letra para dar la palabra por terminada
ACUM_FRAMES_PAUSA = 40


# ----------------------------
# VOZ (TTS)
# ----------------------------

VOZ_VELOCIDAD = 150