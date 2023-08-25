import streamlit as st

st.header('st_selectbox app')
selection = st.selectbox('What is your favorite color?', 
             ('Blue', 'Green', 'Yellow'))
st.write('My favorite color is: ', selection)