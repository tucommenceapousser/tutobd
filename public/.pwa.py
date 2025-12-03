# pwa.py – Serveur PWA pour Streamlit (compatible 2024+)
# full opensource by trhacknon

import streamlit as st
import os

def expose_pwa_files():
    """
    Expose manifest.json, service worker et offline.html
    avec StaticFileRouter (API officielle Streamlit)
    """
    try:
        from streamlit.web.server.static_file_router import StaticFileRouter

        base_dir = os.path.dirname(os.path.abspath(__file__))

        StaticFileRouter.add_static_route(
            "/manifest.json",
            os.path.join(base_dir, "manifest.json")
        )

        StaticFileRouter.add_static_route(
            "/pwabuilder-sw.js",
            os.path.join(base_dir, "pwabuilder-sw.js")
        )

        StaticFileRouter.add_static_route(
            "/offline.html",
            os.path.join(base_dir, "offline.html")
        )

        print("[PWA] manifest.json, service worker & offline.html exposés avec succès.")

    except Exception as e:
        st.error(f"[PWA ERROR] {e}")
