"""
This part of program runs the app, takes user input and displays the output
"""
import streamlit as st
from gtts import gTTS
from functions import url_to_text, pdf_to_text
from main import summarize

# This css property is added to change the background and hide the header
css_properties = '''
<style>
[data-testid="stApp"]{
    background-image: linear-gradient(to top, #b3ffab 0%, #12fff7 100%);
    }
[data-testid="stHeader"]{
    visibility: hidden;
}
</style>
'''
st.markdown(css_properties, unsafe_allow_html=True)


# This function takes input from the user and displays the appropriate input for the selected input
def user_input(user_option):
    if user_option == 'From URL':
        return st.text_input(label='enter url')
    elif user_option == 'From PDF':
        return st.file_uploader(label='Upload pdf'), st.text_input(label='Enter page numbers separated by comma or '
                                                                         'leave blank if you want all pages')
    elif user_option == 'Enter Text':
        return st.text_area('Enter the text', height=300)
    else:
        return None


# The summarizer function is going to call the appropriate function to get the text which is then used to call the
# summary function to get the final summary


def summarizer(user_option, user, fraction):
    if user_option == 'From URL':
        corpus = url_to_text(user)
        summary = summarize(corpus=corpus, n=fraction)
    elif user_option == 'From PDF':
        corpus = pdf_to_text(user[0], user[1])
        summary = summarize(corpus=corpus, n=fraction)
    elif user_option == 'Enter Text':
        summary = summarize(corpus=user, n=fraction)
    else:
        return None
    return summary


# This is the part of the app that displays the dropdown menu
st.write('''
# Quick Summarizer
This is a web app to summarize text. A user can input either a URL, a PDF document or directly entering a text.
''')
option = st.selectbox(
    label='Select the type of input',
    options=['From URL', 'From PDF', 'Enter Text'],
    index=None,
    placeholder="Choose an option")

input_field = user_input(option)  # Here we store the data given by the user (url/pdf/raw text)

# This is a parameter to control the summary length
frac = st.slider(label='Enter the fraction of the original text which you want summery reduce to', min_value=0.0,
                 max_value=1.0, step=0.01)
button1 = st.button('Submit')

# The following part of the program writes the summary and converts the text to speech
if button1:
    st.write("## The summary")
    with st.spinner('In progress...'):
        t = summarizer(user_option=option, user=input_field, fraction=frac)
        st.write(t)

    st.write('## The text to speech audio')
    with st.spinner('In progress...'):
        tts = gTTS(t)
        tts.save('./audio/audio.mp3')
        st.audio(data='./audio/audio.mp3')

