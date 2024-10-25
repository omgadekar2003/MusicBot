# import streamlit as st
# import speech_recognition as sr
# import requests

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
#             api_key = 'YOUR_YOUTUBE_API_KEY'
#             search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_title}&type=video&key={api_key}"
#             response = requests.get(search_url).json()
#             video_id = response['items'][0]['id']['videoId']
#     except sr.UnknownValueError:
#         st.write("Sorry, could not understand the audio.")

# # Play video if video ID is found
# if video_id:
#     st.video(f"https://www.youtube.com/watch?v={video_id}")



import streamlit as st
import speech_recognition as sr
import requests

# Capture audio input
audio_value = st.experimental_audio_input("Record a voice message")
video_id = None

if audio_value:
    st.audio(audio_value)
    # Save the audio for later processing
    with open("audio_message.wav", "wb") as f:
        f.write(audio_value.getbuffer())
        
    # Transcribe audio
    recognizer = sr.Recognizer()
    with sr.AudioFile("audio_message.wav") as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        st.write("You said:", text)
        
        # Parse command
        if "play" in text.lower():
            song_title = text.lower().replace("play", "").strip()
            st.write(f"Searching for {song_title}...")
            
            # Search on YouTube
            api_key = 'API_key_1'
            search_url = f"AIzaSyA4WqgO32cIvDv5IUfqG5ggV3Ej9dIUiFg={song_title}&type=video&key={api_key}"
            response = requests.get(search_url).json()
            
            # Check if 'items' exists in response
            if 'items' in response and len(response['items']) > 0:
                video_id = response['items'][0]['id']['videoId']
            else:
                st.write("Could not find a video for the specified song. Please try another song title.")
    except sr.UnknownValueError:
        st.write("Sorry, could not understand the audio.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

# Play video if video ID is found
if video_id:
    st.video(f"https://www.youtube.com/watch?v={video_id}")

