# # app.py

# import streamlit as st
# import speech_recognition as sr
# import requests

# # Retrieve API key from Streamlit secrets
# api_key = st.secrets["YOUTUBE_API_KEY"]

# # Capture audio input
# audio_value = st.experimental_audio_input("Record a voice message")
# video_id = None

# if audio_value:
#     st.audio(audio_value)
#     # Save the audio for later processing
#     with open("audio_message.wav", "wb") as f:
#         f.write(audio_value.getbuffer())
        
#     # Transcribe audio
#     recognizer = sr.Recognizer()
#     with sr.AudioFile("audio_message.wav") as source:
#         audio_data = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio_data)
#         st.write("You said:", text)
        
#         # Parse command
#         if "play" in text.lower():
#             song_title = text.lower().replace("play", "").strip()
#             st.write(f"Searching for {song_title}...")
            
#             # Search on YouTube
#             search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_title}&type=video&key={api_key}"
#             response = requests.get(search_url).json()

#             # Check if 'items' exists in response
#             if 'items' in response and len(response['items']) > 0:
#                 video_id = response['items'][0]['id']['videoId']
#             else:
#                 st.write("Could not find a video for the specified song. Please try another song title.")
#     except sr.UnknownValueError:
#         st.write("Sorry, could not understand the audio.")
#     except Exception as e:
#         st.write(f"An error occurred: {e}")

# # Play video if video ID is found
# if video_id:
#     st.video(f"https://www.youtube.com/watch?v={video_id}")



# app.py

import streamlit as st
import speech_recognition as sr
import requests

# Set the page configuration
st.set_page_config(page_title="Music Bot", page_icon="🎵", layout="centered")

# Add a title and subtitle
st.title("🎶 Music Bot")
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
    '<div class="header-image"><img src="https://github.com/omgadekar2003/MusicBot/blob/main/DALL%C2%B7E%202024-10-25%2021.55.46%20-%20A%20high-definition%20image%20of%20a%20young%20person%20with%20headphones%20on%2C%20sitting%20comfortably%20in%20a%20cozy%20room%20while%20listening%20to%20music%20through%20a%20music%20bot%20on%20a%20lap.webp" alt="Main Image"></div>',
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
api_key = st.secrets["YOUTUBE_API_KEY"]

# Capture audio input
audio_value = st.experimental_audio_input("🎤 Record a voice message")
video_id = None

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
            
            # Search on YouTube
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_title}&type=video&key={api_key}"
            response = requests.get(search_url).json()

            # Check if 'items' exists in response
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

