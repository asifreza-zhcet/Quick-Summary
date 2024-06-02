import streamlit as st
import requests
from main import func

st.title('Text Summary')
url = st.text_input('enter the url')
st.write(func(url))
