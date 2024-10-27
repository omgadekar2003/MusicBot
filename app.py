# app.py

import streamlit as st
import speech_recognition as sr
import requests

# Set the page configuration
st.set_page_config(page_title="OG's Music Bot", page_icon="🎵", layout="centered")

# Add a title and subtitle
st.title("🎶 OG's Music Bot")
st.markdown("""
    Record your voice and let me play your favorite songs!
    Just say "play" followed by the song title.
""")

# Add styling for the images and UI
st.markdown(
    """
    <style>
    .header-image {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .header-image img {
        width: 100%;  /* Makes the image long in width */
        max-height: 200px;  /* Limits the height */
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
        left: 10px;  /* Changed position to the bottom-left */
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
    .stAudio {
        margin: 20px 0;
        padding: 10px;
        background-color: #f0f8ff;
        border-radius: 5px;
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

# Retrieve API key from Streamlit secrets
api_key = st.secrets["YOUTUBE_API_KEY"]

# Capture audio input with a label
st.markdown("**🎤 Record a voice message**")
audio_value = st.experimental_audio_input("")  # Added label argument
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

# Play video with autoplay if video ID is found
if video_id:
    autoplay_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
    st.markdown(
        f'<iframe width="560" height="315" src="{autoplay_url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )


#------



# # app.py
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

# # Add styling for the images and UI
# st.markdown(
#     """
#     <style>
#     .header-image {
#         display: flex;
#         justify-content: center;
#         margin: 20px 0;
#     }
#     .header-image img {
#         width: 100%;  /* Makes the image long in width */
#         max-height: 200px;  /* Limits the height */
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
#         left: 10px;  /* Changed position to the bottom-left */
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
#     .stAudio {
#         margin: 20px 0;
#         padding: 10px;
#         background-color: #f0f8ff;
#         border-radius: 5px;
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

# # Retrieve API key from Streamlit secrets
# api_key = st.secrets["YOUTUBE_API_KEY"]

# # Capture audio input with a label
# st.markdown("**🎤 Record a voice message**")
# audio_value = st.experimental_audio_input("")  # Added label argument
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





#------


