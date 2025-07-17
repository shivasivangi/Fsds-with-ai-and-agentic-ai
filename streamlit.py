import streamlit as st
st.title("my frist streamlit created by shiva")
st.write("welcome! this app calculate the square of the number")
st.header("select a number")
number=st.slider ("pick a number",0,100,25)
st.subheader("result")
squared_number=number*number
st.write(f"the square of**{number}** is **{squared_number}**.")