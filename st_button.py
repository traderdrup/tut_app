import streamlit as st
st.header('st.button')

if st.button('Say Hello'):
    st.write('Hello World')
else:
    st.write('Goodbye')

