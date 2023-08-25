import streamlit as st
from datetime import time, datetime 

st.header('st_slider tutorial')

#example 1
st.subheader('Age slider')
age = st.slider('How old are you?', 0, 130, 25)
st.write('I am ', age, 'years old')

#example 2
st.subheader('Range slider')
values = st.slider('Select a range of values',
                   0.0, 100.0, (25.0, 75.0))
st.write('Values: ', values)

#example 3
st.subheader('Range time slider')
appointment = st.slider('Schedule your appointment:', 
                        value = (time(11, 30), time(12, 45)))
st.write('You are scheduled for: ', appointment)

#example 4
st.subheader('Datetime range slider')
start_time = st.slider('When do you start?',
                       value = datetime(2023, 1, 1, 9, 30),
                       format='DD/MM/YY - hh/mm')
st.write('Start time: ', start_time)

