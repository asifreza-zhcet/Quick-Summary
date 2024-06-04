import streamlit as st
import requests
import streamlit as st
from gtts import gTTS
from main import func


page_bg_img = '''
<style>
[data-testid="stApp"]{
    background-image: linear-gradient(to top, #b3ffab 0%, #12fff7 100%);;
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


if 'button_1' not in st.session_state:
    st.session_state['button_1'] = False

if 'button_2' not in st.session_state:
    st.session_state['button_2'] = False


st.title('''
Quick Summary  
This is a web app which diplays text summary of any website and also converts the text to speech.
Plese enter the url which you wish to summerize.
''')


url = st.text_input("Enter url")
frac = st.slider(label='fraction', min_value=0.0, max_value=1.0, step=0.01)

button_1 = st.button(label='submit')

if button_1 or st.session_state['button_2']:
    st.session_state['button_1'] = True
    st.session_state.summary = func(url, frac)
    st.write(st.session_state['summary'])

if st.session_state.button_1:
    button_2 = st.button(label='speech')
    st.session_state['button_2'] = True

    if button_2:
        tts = gTTS(st.session_state['summary'])
        tts.save('./audio/audio.mp3')
        st.audio(data='./audio/audio.mp3')



