import streamlit as st
import requests
import streamlit as st
from gtts import gTTS
from main import func
print('a')

def text_to_speech(summary):
    tts = gTTS(summary)
    tts.save('audio.mp3')
    st.audio(data='audio.mp3')
    print('b')

st.title('Text Summary')
with st.form(key='my_form'):
    url = st.text_input("Enter url")
    frac = st.slider(label='fraction', min_value=0.0, max_value=1.0, step=0.01)
    submit_button = st.form_submit_button(label='Submit')
    print('c')


if submit_button:
    summary = func(url, frac)
    st.write(summary)
    speech_button = st.button(label='speech',on_click=text_to_speech,args=(summary,))
    print('d')   

print('*'*50)    

