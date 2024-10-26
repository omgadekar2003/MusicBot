import streamlit as st
import speech_recognition as sr
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set the page configuration
st.set_page_config(page_title="OG's Music Bot", page_icon="🎵", layout="centered")

# Add a title and subtitle
st.title("🎶 OG's Music Bot")
st.markdown("""
    Record your voice and let me play your favorite songs!
    Just say "play" followed by the song title.
""")

# Add images at the top
st.markdown(
    """
    <style>
    .header-image {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .header-image img {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
    }
    .developer-image {
        width: 50px; 
        height: 50px; 
        border-radius: 50%; 
        margin-right: 10px;
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
    .stButton {
        background-color: #4CAF50;
        color: white;
    }
    .stButton:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the main image
st.markdown(
    '<div class="header-image"><img src="https://images.pexels.com/photos/159376/turntable-top-view-audio-equipment-159376.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Main Image"></div>',
    unsafe_allow_html=True
)

# Developer credit
st.markdown(
    '<div class="developer-credit"><img class="developer-image" src="https://github.com/omgadekar2003/MusicBot/blob/main/20220503_112329.jpg?raw=true" alt="Developer">Developer: OM GADEKAR</div>',
    unsafe_allow_html=True
)

# Add some styling for audio input
st.markdown(
    """
    <style>
    .stAudio {
        margin: 20px 0;
        padding: 10px;
        background-color: #f0f8ff;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Retrieve API key from Streamlit secrets
youtube_api_key = st.secrets["YOUTUBE_API_KEY"]

# Spotify API Credentials
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
redirect_uri = st.secrets["REDIRECT_URI"]

# Authentication using Spotipy
scope = "user-read-playback-state user-modify-playback-state"
sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

# Get the access token
token_info = sp_oauth.get_cached_token()
if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    st.write(f"[Login to Spotify]({auth_url})")

# Capture audio input
audio_value = st.experimental_audio_input("🎤 Record a voice message")
video_id = None
spotify_track_id = None

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
            
            # Search on Spotify
            if token_info:
                access_token = token_info['access_token']
                sp = spotipy.Spotify(auth=access_token)
                
                results = sp.search(q=song_title, type="track", limit=1)
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    spotify_track_id = track['id']
                    st.write(f"Playing on Spotify: *{track['name']}*")
                    st.components.v1.html(
                        f"""
                        <iframe src="https://open.spotify.com/embed/track/{spotify_track_id}" 
                                width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                        """,
                        height=100
                    )
                else:
                    # If not found on Spotify, search on YouTube
                    st.info(f"Could not find *{song_title}* on Spotify, searching on YouTube...")
                    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_title}&type=video&key={youtube_api_key}"
                    response = requests.get(search_url).json()
                    if 'items' in response and len(response['items']) > 0:
                        video_id = response['items'][0]['id']['videoId']
                    else:
                        st.error("Could not find a video for the specified song. Please try another song title.")
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Play video if video ID is found
if video_id:
    st.video(f"https://www.youtube.com/watch?v={video_id}")

# Display the Spotify player if a track ID is found
if spotify_track_id:
    st.components.v1.html(
        f"""
        <iframe src="https://open.spotify.com/embed/track/{spotify_track_id}" 
                width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """,
        height=100
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

