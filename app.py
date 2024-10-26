# app.py

import streamlit as st
import speech_recognition as sr
import requests
from requests.auth import HTTPBasicAuth

# Set the page configuration
st.set_page_config(page_title="Music Bot", page_icon="🎵", layout="centered")

# Add a title and subtitle
st.title("🎶 Music Bot")
st.markdown("""
    Record your voice and let me play your favorite songs!
    Just say "play" followed by the song title.
""")

# Add some styling
st.markdown(
    """
    <style>
    .stAudio {
        margin: 20px 0;
        padding: 10px;
        background-color: #f0f8ff;
        border-radius: 5px;
    }
    .stButton {
        background-color: #4CAF50;
        color: white;
    }
    .stButton:hover {
        background-color: #45a049;
    }
    .developer-credit {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 12px;
        color: gray;
        background: rgba(255, 255, 255, 0.8);
        padding: 5px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Retrieve API keys from Streamlit secrets
youtube_api_key = st.secrets["YOUTUBE_API_KEY"]
spotify_client_id = st.secrets["SPOTIFY_CLIENT_ID"]
spotify_client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]

# Function to get Spotify token
def get_spotify_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        token_url,
        data={"grant_type": "client_credentials"},
        auth=HTTPBasicAuth(client_id, client_secret)
    )
    return response.json().get("access_token")

# Spotify song search
def search_spotify_song(song_title, token):
    search_url = f"https://api.spotify.com/v1/search?q={song_title}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(search_url, headers=headers).json()
    
    if 'tracks' in response and response['tracks']['items']:
        track = response['tracks']['items'][0]
        return track['external_urls']['spotify']  # Spotify link
    return None

# Capture audio input
audio_value = st.experimental_audio_input("🎤 Record a voice message")
video_id = None
spotify_song_url = None

if audio_value:
    st.audio(audio_value, format='audio/wav')
    # Save the audio for later processing
    with open("audio_message.wav", "wb") as f:
        f.write(audio_value.getbuffer())
        
    # Transcribe audio
    recognizer = sr.Recognizer()
    with sr.AudioFile("audio_message.wav") as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        st.success(f"You said: *{text}*")
        
        # Parse command
        if "play" in text.lower():
            song_title = text.lower().replace("play", "").strip()
            st.info(f"Searching for *{song_title}*...")

            # YouTube Search
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_title}&type=video&key={youtube_api_key}"
            response = requests.get(search_url).json()

            # Check if 'items' exists in response for YouTube
            if 'items' in response and len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
            else:
                st.warning("Could not find on YouTube. Trying Spotify...")

            # Spotify Search
            spotify_token = get_spotify_token(spotify_client_id, spotify_client_secret)
            spotify_song_url = search_spotify_song(song_title, spotify_token)
            
            # Check if song is found on Spotify
            if spotify_song_url:
                st.success(f"Playing *{song_title}* on Spotify!")
            elif not video_id:
                st.error("Could not find the song on either YouTube or Spotify.")
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Play YouTube video if video ID is found
if video_id:
    st.video(f"https://www.youtube.com/watch?v={video_id}")
# Display Spotify link if song URL is found
elif spotify_song_url:
    st.markdown(f"[Listen on Spotify]({spotify_song_url})")

# Developer credit
st.markdown(
    '<div class="developer-credit">Developer: OM GADEKAR</div>',
    unsafe_allow_html=True
)




# # app.py

# import streamlit as st
# import speech_recognition as sr
# import requests

# # Set the page configuration
# st.set_page_config(page_title="OG's Music Bot", page_icon="🎵", layout="centered")

# # Add a title and subtitle
# st.title("🎶 OG's Music Bot")
# st.markdown("""
#     Record your voice and let me play your favorite songs!
#     Just say "play" followed by the song title.
# """)

# # Add images at the top
# st.markdown(
#     """
#     <style>
#     .header-image {
#         display: flex;
#         justify-content: center;
#         margin: 20px 0;
#     }
#     .header-image img {
#         max-width: 100%;
#         height: auto;
#         border-radius: 10px;
#     }
#     .developer-image {
#         width: 50px; 
#         height: 50px; 
#         border-radius: 50%; 
#         margin-right: 10px;
#     }
#     .developer-credit {
#         position: fixed;
#         bottom: 10px;
#         right: 10px;
#         font-size: 12px;
#         color: gray;
#         background: rgba(255, 255, 255, 0.8);
#         padding: 5px;
#         border-radius: 5px;
#     }
#     .stButton {
#         background-color: #4CAF50;
#         color: white;
#     }
#     .stButton:hover {
#         background-color: #45a049;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Display the main image
# st.markdown(
#     '<div class="header-image"><img src="https://images.pexels.com/photos/159376/turntable-top-view-audio-equipment-159376.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Main Image"></div>',
#     unsafe_allow_html=True
# )

# # Developer credit
# st.markdown(
#     '<div class="developer-credit"><img class="developer-image" src="https://github.com/omgadekar2003/MusicBot/blob/main/20220503_112329.jpg?raw=true" alt="Developer">Developer: OM GADEKAR</div>',
#     unsafe_allow_html=True
# )

# # Add some styling for audio input
# st.markdown(
#     """
#     <style>
#     .stAudio {
#         margin: 20px 0;
#         padding: 10px;
#         background-color: #f0f8ff;
#         border-radius: 5px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Retrieve API key from Streamlit secrets
# api_key = st.secrets["YOUTUBE_API_KEY"]

# # Capture audio input
# audio_value = st.experimental_audio_input("🎤 Record a voice message")
# video_id = None

# if audio_value:
#     st.audio(audio_value, format='audio/wav')
#     # Save the audio for later processing
#     with open("audio_message.wav", "wb") as f:
#         f.write(audio_value.getbuffer())
        
#     # Transcribe audio
#     recognizer = sr.Recognizer()
#     with sr.AudioFile("audio_message.wav") as source:
#         audio_data = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio_data)
#         st.success(f"You said: *{text}*")
        
#         # Parse command
#         if "play" in text.lower():
#             song_title = text.lower().replace("play", "").strip()
#             st.info(f"Searching for *{song_title}*...")
            
#             # Search on YouTube
#             search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_title}&type=video&key={api_key}"
#             response = requests.get(search_url).json()

#             # Check if 'items' exists in response
#             if 'items' in response and len(response['items']) > 0:
#                 video_id = response['items'][0]['id']['videoId']
#             else:
#                 st.error("Could not find a video for the specified song. Please try another song title.")
#     except sr.UnknownValueError:
#         st.error("Sorry, I could not understand the audio.")
#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# # Play video if video ID is found
# if video_id:
#     st.video(f"https://www.youtube.com/watch?v={video_id}")

