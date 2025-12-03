# pwa.py – Serveur PWA pour Streamlit
# full opensource by trhacknon

import streamlit as st
from starlette.responses import FileResponse

def expose_pwa_files():
    """
    Expose manifest.json, service worker et offline.html
    via le serveur interne Starlette utilisé par Streamlit.
    """
    try:
        from streamlit.web.server import Server
        app = Server.get_current()._app   # récupération de l’app Starlette

        # Manifest
        @app.get("/manifest.json")
        def serve_manifest():
            return FileResponse("manifest.json", media_type="application/manifest+json")

        # Service worker
        @app.get("/pwabuilder-sw.js")
        def serve_sw():
            return FileResponse("pwabuilder-sw.js", media_type="application/javascript")

        # Page offline PWA
        @app.get("/offline.html")
        def serve_offline():
            return FileResponse("offline.html", media_type="text/html")

        print("[PWA] manifest.json, pwabuilder-sw.js & offline.html servis correctement.")

    except Exception as e:
        st.error(f"[PWA] Erreur lors de l’enregistrement des routes : {e}")
