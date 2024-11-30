import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_link(song_name, artist_name):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        query = f"{song_name} {artist_name}"
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()
        
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return "Nenhum link encontrado"
    except Exception as e:
        return f"Erro ao buscar no YouTube: {e}"






spotify_data = pd.read_csv("spotify-2023.csv", encoding="latin1")



st.title("🎵 Compile Sua Playlist")
st.write("Responda algumas perguntas rápidas e receba uma playlist personalizada!")


mood = st.radio("Qual o seu humor agora?", ["Alegre", "Neutro", "Triste"])
speed = st.radio("Prefere músicas mais rápidas ou lentas?", ["Rápidas", "Lentas"])
activity = st.radio("Você gosta mais de dançar ou relaxar ouvindo música?", ["Dançar", "Relaxar"])


if st.button("Descubra Sua Playlist"):

    filtered_data = spotify_data[
        ((spotify_data['energy_%'] > 70) if speed == "Rápidas" else (spotify_data['energy_%'] <= 70)) &
        ((spotify_data['danceability_%'] > 70) if activity == "Dançar" else (spotify_data['danceability_%'] <= 70))
    ]
    suggested_playlist = filtered_data.sample(5) if not filtered_data.empty else None


    if suggested_playlist is not None:
        st.success("🎧 Baseado no seu perfil:")
        st.write("Sua playlist personalizada com links do YouTube:")
        for index, row in suggested_playlist.iterrows():
            youtube_link = get_youtube_link(row['track_name'], row['artist(s)_name'])
            st.write(f"- **{row['track_name']}** de *{row['artist(s)_name']}*: [Ouça no YouTube]({youtube_link})")
    else:
        st.warning("Não conseguimos encontrar músicas que correspondam às suas preferências. Tente ajustar as opções!")



