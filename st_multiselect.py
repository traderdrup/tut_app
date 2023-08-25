import streamlit as st

st.header('Multi select app')
options = st.multiselect('What is your favorite colors?',
                         ['Green', 'Blue', 'Red', 'Yellow'],
                         ['Green', 'Red', 'Blue'])
st.write('My favorite colors are: ', options)