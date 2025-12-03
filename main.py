# full opensource by trhacknon
import streamlit as st
import os
import serial
import serial.tools.list_ports
import zipfile
from io import BytesIO
import requests
import subprocess



st.set_page_config(
    page_title="Valise Diagnostic Auto Pi Zero 2W",
    page_icon="/public/favicon.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Footer design trhacknon ---
st.markdown("""
<style>
/* Footer sticky en bas, style hacker trhacknon */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #101622;  /* fond sombre */
    color: #0ff;                /* texte fluo cyan */
    text-align: center;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    padding: 0.5rem 0;
    border-top: 2px solid #0ff; /* bordure fluo */
    z-index: 1000;
}

/* liens fluo avec hover */
.footer a {
    color: #0ff;
    text-decoration: none;
    font-weight: bold;
}
.footer a:hover {
    color: #f0f;  /* violet fluo au survol */
    text-shadow: 0 0 5px #f0f;
}
</style>

<div class="footer">
    💻 Full open-source by <a href="https://github.com/trhacknon" target="_blank">trhacknon</a> | 🚀 PWA ready & offline mode
</div>
""", unsafe_allow_html=True)

# --- META + MANIFEST ---
st.markdown("""
<link rel="manifest" href="/public/manifest.json">
<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/public/pwabuilder-sw.js')
        .then(reg => console.log("SW registered", reg))
        .catch(err => console.warn("SW registration failed", err));
}
</script>
<link rel="icon" href="/public/favicon.jpg">
""", unsafe_allow_html=True)

# --- META TAGS SEO + SOCIAL ---
meta_tags = """
<meta name="description" content="Valise diagnostic auto DIY - Raspberry Pi Zéro 2W, ESP32, Lecteur OBD2, avec firmwares, images et outils.">
<meta property="og:title" content="Valise Diagnostic Auto DIY"/>
<meta property="og:description" content="Diagnostic automobile Ford/Peugeot avec Raspberry Pi Zero 2W & ESP32."/>
<meta property="og:image" content="/public/favicon.jpg"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://tutobd.streamlit.app/"/>

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Valise Diagnostic Auto DIY">
<meta name="twitter:description" content="OBD2, Pi Zero 2W, ESP32, firmware, outils.">
<meta name="twitter:image" content="/public/favicon.jpg">
"""

# Injection head
st.markdown(f"<head>{meta_tags}</head>", unsafe_allow_html=True)

# Manifest + Service Worker
st.markdown("""
<meta name="theme-color" content="#101622">
<meta property="og:title" content="OBD Smartphone App">
<meta property="og:description" content="Diagnostique OBD pour smartphone + PWA + offline mode">
<meta property="og:image" content="/public/favicon.jpg">
<meta property="og:type" content="website">
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("""
    <div style="text-align:center; font-size:28px;">
        😈
    </div>
        Diy diag device by TRHACKNON
    <div style="text-align:center; font-size:28px;">
        😈
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
        <img src="https://f.top4top.io/p_3624iyyqs0.gif" alt="Logo" style="height:40px;">
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Navigation</h3>", unsafe_allow_html=True)

# Design mobile
st.markdown("""
<style>
.block-container { padding-top: 1rem; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- MENU ---
menu = ["Accueil", "Composants", "Firmware & Librairies", "Instructions", 
        "Scripts & Téléchargement", "Astuces & Evolutions", "Flash Firmware"]
choice = st.sidebar.selectbox("Navigation", menu)

# -------------------------------
#  SECTIONS
# -------------------------------

# -------- ACCUEIL -------------
if choice == "Accueil":
    st.title("💻 Valise Diagnostic Auto DIY - Raspberry Pi Zero 2W / ESP32-S3")
    st.subheader("Projet pour Ford Fiesta & Peugeot 406 Phase 2")

    st.markdown("""
<div style="text-align:center;">
    <img src="https://f.top4top.io/p_3624iyyqs0.gif" alt="Trhacknon Animation" style="max-width:80%; border: 2px solid #39ff14; border-radius:10px;">
</div>
""", unsafe_allow_html=True)
    
    st.markdown("""
Ce projet permet de créer une **valise diagnostic automobile DIY** compatible avec des véhicules récents et anciens.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://www.jeffgeerling.com/sites/default/files/images/jonathan-clark-pico-zero-2w-full.jpeg", caption="Raspberry Pi Zero 2W", width='stretch')
    with col2:
        st.image("https://www.espressif.com/sites/default/files/dev-board/ESP32-C6-DevKitC-1_L.png", caption="ESP32-C6", width='stretch')
    with col3:
        st.image("https://lilygo.cc/cdn/shop/products/Lilygo-T-display_5.jpg?v=1657873834", caption="ESP32-S3 T-Display", width='stretch')

# -------- COMPOSANTS ----------
elif choice == "Composants":
    st.header("🛠 Composants nécessaires")
    
    components = [
        {
            "Nom": "Raspberry Pi Zero 2 W",
            "Prix": "≈15,48 €",
            "Lien": "https://www.mouser.fr/ProductDetail/Raspberry-Pi/SC1146",
            "Image": "https://www.jeffgeerling.com/sites/default/files/images/jonathan-clark-pico-zero-2w-full.jpeg"
        },
        {
            "Nom": "Adaptateur OBD-II USB / Bluetooth (ELM327)",
            "Prix": "≈10-15 €",
            "Lien": "https://www.amazon.fr/s?k=elm327+usb",
            "Image": "https://m.media-amazon.com/images/I/51R8JW892UL._AC_UF1000,1000_QL80_FMwebp_.jpg"
        },
        {
            "Nom": "Convertisseur DC/DC 12V → 5V USB",
            "Prix": "≈7-10 €",
            "Lien": "https://www.amazon.fr/dp/B0FBQXK46N",
            "Image": "https://m.media-amazon.com/images/I/618wOGPAnJL._AC_UF1000,1000_QL80_FMwebp_.jpg"
        },
        {
            "Nom": "Écran TFT / OLED",
            "Prix": "≈10-20 €",
            "Lien": "https://www.amazon.fr/s?k=raspberry+pi+oled+tft",
            "Image": "https://m.media-amazon.com/images/I/81eTcRMsaEL._AC_UF1000,1000_QL80_FMwebp_.jpg"
        }
    ]
    
    # Affiche texte descriptif
    for c in components:
        st.markdown(f"- **{c['Nom']}** – {c['Prix']} – [Lien]({c['Lien']})")
    
    # Affiche images côte à côte
    cols = st.columns(len(components))
    for i, c in enumerate(components):
        with cols[i]:
            st.image(c["Image"], caption=c["Nom"], width='stretch')        
# -------- FIRMWARE ------------
elif choice == "Firmware & Librairies":
    st.header("📦 Firmware existants")
    st.markdown("""
- **Python-OBD** : https://github.com/brendan-w/python-OBD  
- **GVRET ESP32** : https://github.com/collin80/GVRET  
    """)

# -------- INSTRUCTIONS --------
elif choice == "Instructions":
    st.header("📝 Instructions pas à pas")
    st.markdown("""
1. Installer OS sur Pi  
2. Installer python-OBD  
3. Brancher OBD-II  
4. Lire données moteur  
    """)

# -------- SCRIPTS -------------
elif choice == "Scripts & Téléchargement":
    st.header("💻 Scripts Python de base")
    st.code("""
import obd, time
connection = obd.OBD()
cmds = [obd.commands.RPM, obd.commands.SPEED]
while True:
    for cmd in cmds:
        print(connection.query(cmd))
    time.sleep(1)
""")

# -------- ASTUCES -------------
elif choice == "Astuces & Evolutions":
    st.header("💡 Conseils")
    st.markdown("""
- Ajouter écran  
- Multi-voitures  
- GPS / data logging  
    """)

# -------- FLASH FIRMWARE -------
elif choice == "Flash Firmware":
    st.header("⚡ Flash Firmware ESP32")

    firmware_options = {
        "GVRET ESP32 (CAN Bus)": "https://github.com/collin80/GVRET/releases/latest/download/gvret-esp32.bin",
        "ESP32 OBD-II basique": "https://example.com/esp32-obd.bin"
    }

    choice_fw = st.selectbox("Choisir firmware", list(firmware_options.keys()))
    st.write("Lien :", firmware_options[choice_fw])

    ports = [p.device for p in serial.tools.list_ports.comports()]
    selected_port = st.selectbox("Port série", ports)

    if st.button("Flasher"):
        try:
            url = firmware_options[choice_fw]
            fname = url.split("/")[-1]
            r = requests.get(url)
            open(fname, "wb").write(r.content)

            cmd = f"esptool.py --chip esp32 --port {selected_port} write_flash -z 0x1000 {fname}"
            subprocess.run(cmd, shell=True)
            st.success("Flash réussi !")

        except Exception as e:
            st.error(e)
