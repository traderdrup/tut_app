import streamlit as st
import numpy as np
import pandas as pd

st.header('st_line_chart app')
chart_data = pd.DataFrame(np.random.rand(20, 3),
                          columns=['a', 'b', 'c'])
st.line_chart(chart_data)

