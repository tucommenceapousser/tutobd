# diagnostic_valise_complete.py
import streamlit as st
import os
import zipfile
from io import BytesIO

st.set_page_config(
    page_title="Valise Diagnostic Auto Pi Zero 2W",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar menu
menu = ["Accueil", "Composants", "Firmware & Librairies", "Instructions", "Scripts & Téléchargement", "Astuces & Evolutions"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- Accueil ---
if choice == "Accueil":
    st.title("💻 Valise Diagnostic Auto DIY - Raspberry Pi Zero 2W")
    st.subheader("Projet pour Ford Fiesta & Peugeot 406 Phase 2")
    st.markdown("""
Ce projet permet de créer une **valise diagnostic automobile DIY** à base de Raspberry Pi Zero 2W,
compatible avec des voitures récentes (Ford Fiesta) et anciennes (Peugeot 406 Phase 2 essence).

**Objectifs :**
- Lire les codes défaut moteur, transmission, ABS (si supporté)
- Afficher et stocker les données moteur en temps réel
- Avoir un système évolutif et personnalisable
- Option : multi-voitures, interface web, affichage sur écran OLED/TFT
    """)
    st.image("https://cdn.pixabay.com/photo/2016/03/09/09/17/car-1245717_960_720.jpg", use_column_width=True)

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
