#full opensource by trhacknon
import streamlit as st
import os
import serial
import serial.tools.list_ports
import zipfile
from io import BytesIO

st.set_page_config(
    page_title="Valise Diagnostic Auto Pi Zero 2W",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection de meta tags pour SEO + réseaux sociaux
meta_tags = """
<meta name="description" content="Valise diagnostic auto DIY - Raspberry Pi Zéro 2W, ESP32, Lecteur OBD2, avec firmwares, images et outils.">
<meta property="og:title" content="Valise Diagnostic Auto DIY"/>
<meta property="og:description" content="Diagnostic automobile Ford/Peugeot avec Raspberry Pi Zero 2W & ESP32."/>
<meta property="og:image" content="https://smarthomescene.com/wp-content/uploads/2024/10/diy-status-screen-controller-lilygo-t-display-s3-amoled-featured-image.jpg"/>
<meta property="og:type" content="website"/>
<meta property="og:url" content="https://tutobd.streamlit.app/"/>

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Valise Diagnostic Auto DIY">
<meta name="twitter:description" content="OBD2, Pi Zero 2W, ESP32, firmware, outils.">
<meta name="twitter:image" content="https://smarthomescene.com/wp-content/uploads/2024/10/diy-status-screen-controller-lilygo-t-display-s3-amoled-featured-image.jpg">
"""

st.markdown(f"<head>{meta_tags}</head>", unsafe_allow_html=True)
st.markdown("""
<style>
/* Style type application mobile */
.block-container {
    padding-top: 1rem;
}
header, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

menu = ["Accueil", "Composants", "Firmware & Librairies", "Instructions", 
        "Scripts & Téléchargement", "Astuces & Evolutions", "Flash Firmware"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- Flash Firmware ---
if choice == "Flash Firmware":
    st.header("⚡ Flash Firmware / Microcontrôleur")
    st.markdown("""
Vous pouvez flasher directement les firmwares existants pour ESP32 ou tout autre microcontrôleur compatible.

**Fonctionnalités :**
- Choix du firmware (GVRET, ESP32 CAN, autres projets open-source)
- Instructions pas à pas
- Téléchargement automatique du firmware
- Sélection du port série
- Flashage sécurisé avec `esptool.py` (ESP32) ou équivalent
    """)

    # Sélection du firmware
    firmware_options = {
        "GVRET ESP32 (CAN Bus)": "https://github.com/collin80/GVRET/releases/latest/download/gvret-esp32.bin",
        "ESP32 OBD-II basique": "https://github.com/user/esp32-obd-firmware/releases/latest/download/esp32-obd.bin"
    }
    firmware_choice = st.selectbox("Choisir le firmware à flasher", list(firmware_options.keys()))
    st.markdown(f"**Lien du firmware :** [Télécharger]({firmware_options[firmware_choice]})")

    # Sélection du port série
    import serial.tools.list_ports
    ports = [p.device for p in serial.tools.list_ports.comports()]
    selected_port = st.selectbox("Sélectionner le port série", ports)

    # Commande de flashage
    st.markdown("""
⚠️ **Attention :** Assurez-vous que l'appareil est en mode bootloader avant de flasher.  
Le flashage écrase le firmware existant.
    """)

    if st.button("Flasher le firmware"):
        import subprocess
        try:
            firmware_url = firmware_options[firmware_choice]
            firmware_file = firmware_url.split("/")[-1]

            # Télécharger le firmware
            st.info("Téléchargement du firmware...")
            import requests
            r = requests.get(firmware_url)
            with open(firmware_file, "wb") as f:
                f.write(r.content)
            st.success("Firmware téléchargé avec succès !")

            # Flashage ESP32
            cmd = f"esptool.py --chip esp32 --port {selected_port} write_flash -z 0x1000 {firmware_file}"
            st.info(f"Commande de flashage exécutée : {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            st.success("Firmware flashé avec succès !")
        except Exception as e:
            st.error(f"Erreur pendant le flashage : {e}")
# --- Accueil ---
if choice == "Accueil":
    st.title("💻 Valise Diagnostic Auto DIY - Raspberry Pi Zero 2W / ESP32-S3")
    st.subheader("Projet pour Ford Fiesta & Peugeot 406 Phase 2")
    st.markdown("""
Ce projet permet de créer une **valise diagnostic automobile DIY** compatible avec des véhicules récents (Ford Fiesta) et anciens (Peugeot 406 Phase 2 essence).

**Objectifs :**
- Lire les codes défaut moteur, transmission, ABS (si supporté)
- Afficher et stocker les données moteur en temps réel
- Avoir un système évolutif et personnalisable
- Option : multi-voitures, interface web, affichage sur écran OLED/TFT
    """)

    # Affichage côte à côte des matériels
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://www.jeffgeerling.com/sites/default/files/images/jonathan-clark-pico-zero-2w-full.jpeg", caption="Raspberry Pi Zero 2W", use_column_width=True)
    with col2:
        st.image("https://www.espressif.com/sites/default/files/dev-board/ESP32-C6-DevKitC-1_L.png", caption="ESP32-C6", use_column_width=True)
    with col3:
        st.image("https://lilygo.cc/cdn/shop/products/Lilygo-T-display_5.jpg?v=1657873834", caption="ESP32-S3 t-display", use_column_width=True)

    st.markdown("""
💡 Ce projet est pensé pour être **évolutif** : tu peux commencer avec le Pi Zero 2W et passer plus tard à un ESP32-S3 T-Display pour une valise compacte et autonome.
""")
# --- Composants ---
elif choice == "Composants":
    st.header("🛠 Composants nécessaires")
    components = [
        {"Nom": "Raspberry Pi Zero 2 W", "Prix": "≈15,48 €", "Lien": "https://www.mouser.fr/ProductDetail/Raspberry-Pi/SC1146?qs=ST9lo4GX8V3CWSVbdflDaA%3D%3D"},
        {"Nom": "Adaptateur OBD-II USB / Bluetooth (ELM327)", "Prix": "≈10-15 €", "Lien": "https://www.amazon.fr/s?k=elm327+usb"},
        {"Nom": "Convertisseur DC/DC 12V → 5V USB", "Prix": "≈7-10 €", "Lien": "https://www.amazon.fr/USB-Convertisseur-Adaptateur-Regulateur-Transformateur/dp/B0FBQXK46N"},
        {"Nom": "Écran TFT / OLED (optionnel)", "Prix": "≈10-20 €", "Lien": "https://www.amazon.fr/s?k=raspberry+pi+oled+tft"},
        {"Nom": "Kit Raspberry Pi Zero 2 W complet (optionnel)", "Prix": "≈56,99 €", "Lien": "https://www.amazon.fr/GeeekPi-Raspberry-Starter-Preloaded-Heatsink/dp/B0B7MR7XWT"},
        {"Nom": "Câbles Dupont / Alimentation voiture", "Prix": "≈5-10 €", "Lien": "https://www.amazon.fr/s?k=cables+dupont+raspberry+pi"}
    ]
    for comp in components:
        st.markdown(f"- **{comp['Nom']}** - {comp['Prix']} [Lien]({comp['Lien']})")

    st.markdown("💶 **Budget total estimé : 50-70 € pour un kit complet minimum**")

# --- Firmware & Librairies ---
elif choice == "Firmware & Librairies":
    st.header("📦 Firmware et Librairies existants")
    st.markdown("""
- **Python-OBD** : [GitHub python-OBD](https://github.com/brendan-w/python-OBD)  
  Permet de lire les données OBD-II via ELM327 sur Raspberry Pi.
- **GVRET / ESP32** : [GitHub GVRET](https://github.com/collin80/GVRET)  
  Firmware open-source pour ESP32 CAN bus (option si tu veux faire une valise compacte ESP32).
- **Applications mobiles de test** : Torque, OBD Auto Doctor, Forscan (pour Ford)
""")
    st.markdown("⚠️ Vérifier la compatibilité de l'adaptateur OBD avant d'acheter")

# --- Instructions ---
elif choice == "Instructions":
    st.header("📝 Instructions pas à pas")
    steps = [
        "1. Installer Raspberry OS sur la micro-SD du Pi Zero 2W.",
        "2. Mettre à jour le système: `sudo apt update && sudo apt upgrade`.",
        "3. Installer Python et pip: `sudo apt install python3-pip`.",
        "4. Installer la librairie python-OBD: `pip3 install obd`.",
        "5. Brancher l'adaptateur OBD-II (USB ou Bluetooth) et vérifier le port.",
        "6. Tester la connexion avec le script Python fourni ci-dessous.",
        "7. (Optionnel) Ajouter un écran OLED/TFT pour affichage direct.",
        "8. (Optionnel) Créer une interface Web simple avec Flask ou Streamlit pour consulter les données depuis smartphone/PC.",
        "9. Configurer le démarrage automatique si tu veux que la valise s'allume à l'allumage du véhicule."
    ]
    for step in steps:
        st.markdown(f"- {step}")

# --- Scripts & Téléchargement ---
elif choice == "Scripts & Téléchargement":
    st.header("💻 Scripts Python de base")
    st.code("""
import obd
import time

connection = obd.OBD()  # auto-detect adaptateur

cmds = [obd.commands.RPM, obd.commands.SPEED, obd.commands.COOLANT_TEMP, obd.commands.ELM_VOLTAGE]

try:
    while True:
        for cmd in cmds:
            res = connection.query(cmd)
            if not res.is_null():
                print(f"{cmd.name}: {res.value} {res.unit}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt par utilisateur")
    connection.close()
""", language="python")

    # Option pour télécharger un ZIP complet avec script + README
    st.subheader("Télécharger le package complet")
    # Création d'un ZIP en mémoire
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("script_obd.py", """
import obd, time
connection = obd.OBD()
cmds = [obd.commands.RPM, obd.commands.SPEED, obd.commands.COOLANT_TEMP]
while True:
    for cmd in cmds:
        res = connection.query(cmd)
        if not res.is_null():
            print(f"{cmd.name}: {res.value} {res.unit}")
    time.sleep(1)
""")
        zip_file.writestr("README.md", "# Valise Diagnostic Pi Zero\nInstructions et script Python pour lire les données OBD-II.")

    st.download_button(
        label="Télécharger le package ZIP",
        data=zip_buffer.getvalue(),
        file_name="valise_diagnostic_pi_zero.zip",
        mime="application/zip"
    )

# --- Astuces & Evolutions ---
elif choice == "Astuces & Evolutions":
    st.header("💡 Conseils & Evolutions possibles")
    st.markdown("""
- Vérifier la qualité de l'adaptateur ELM327 pour éviter les problèmes.  
- Certaines voitures n’exposent pas tous les PIDs OBD-II.  
- Ajouter GPS et capteurs externes pour log de trajets.  
- Interface web interactive pour consultation depuis smartphone.  
- Multi-voitures : Peugeot 406 Phase 2 (K-Line) + Ford Fiesta (CAN).  
- Enregistrer les données sur CSV ou SQLite pour analyse post-trajet.  
- Ajouter alertes email ou notifications pour valeurs critiques.  
- Interface embarquée sur écran TFT / OLED pour valise autonome.
""")
    st.success("✅ Projet complet et évolutif prêt à être testé !")
