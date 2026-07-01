# ----------------------------
# CONFIGURACIÓN DE CÁMARA
# ----------------------------

# 👉 CÁMARA DE LA PC (por defecto)
# 0 = cámara integrada / webcam
CAMERA_SOURCE = 0


# 👉 CÁMARA IP (opcional)
IP = "192.xxx.x.xxx"
PORT = "8080"
VIDEO_URL = f"http://{IP}:{PORT}/videofeed"


# ----------------------------
# MODO DE CÁMARA ACTIVO
# ----------------------------

# Usa "pc" o "ip"
CAMERA_MODE = "pc"

# Si quieres usar IP, cambia a:
# CAMERA_MODE = "ip"


# ----------------------------
# RESOLUCIÓN (opcional)
# ----------------------------
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080


# ----------------------------
# UMBRALES GESTOS
# ----------------------------
UMBRAL_EXT_DEDO = 10
UMBRAL_EXT_PULGAR = 5

ANGULO_GANCHO_MIN = 70
ANGULO_GANCHO_MAX = 140

ANGULO_L_MIN = 60
ANGULO_L_MAX = 120


# ----------------------------
# LETRA C (distancia)
# ----------------------------
DIST_C_MIN = 100
DIST_C_MAX = 220


# ----------------------------
# LETRA D (alineación pulgar)
# ----------------------------
DIF_PULGAR_MAYOR = 40