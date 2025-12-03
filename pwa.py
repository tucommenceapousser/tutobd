import streamlit as st
from starlette.responses import FileResponse

def expose_pwa_files():
    try:
        from streamlit.web.server import Server
        server = Server.get_current()

        if not server:
            st.warning("Impossible d'initialiser le serveur Streamlit")
            return

        app = server._app

        @app.get("/manifest.json")
        def manifest():
            return FileResponse("manifest.json")

        @app.get("/pwabuilder-sw.js")
        def sw():
            return FileResponse("pwabuilder-sw.js")

        @app.get("/offline.html")
        def offline():
            return FileResponse("offline.html")

        @app.get("/favicon.png")
        def favicon():
            return FileResponse("favicon.png")

    except Exception as e:
        st.error(f"Erreur PWA: {e}")
