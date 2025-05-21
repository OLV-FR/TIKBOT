
import streamlit as st
import os
import shutil
from joe_bot import main  # Assure-toi que joe_bot.py contient une fonction main()
from pathlib import Path

st.set_page_config(page_title="TikBot Empire", page_icon="🎬")
st.title("🎬 TikBot Empire - Analyse intelligente de vidéos TikTok")

# Téléversement de fichier
uploaded_video = st.file_uploader("Téléverse une vidéo au format MP4", type=["mp4"])

if uploaded_video:
    video_path = Path("video_source.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
    st.success("Vidéo téléversée avec succès !")

    if st.button("Lancer l'analyse"):
        with st.spinner("🔍 Analyse de la vidéo en cours..."):
            try:
                main()
                st.success("✅ Analyse terminée !")

                # Affiche les clips générés
                output_dir = Path("Sortie")
                clips = list(output_dir.glob("*.mp4"))
                if clips:
                    st.subheader("📍 Extraits générés par TikBot Empire :")
                    for clip in clips:
                        st.video(str(clip))
                else:
                    st.warning("Aucun extrait vidéo détecté.")
            except Exception as e:
                st.error(f"❌ Une erreur est survenue : {e}")
