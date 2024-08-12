import streamlit as st


def home():
    st.title("BPhO Computation Challenge 2024")
    st.write(
        "Umair Malik's response to this year's BPhO Computational Challenge, which focused primarily on the physics of Projectile Modelling."
    )
    st.header("About")
    st.write(
        "The project uses a backend of Python to generate the required data reliably, using a framework of the NumPy and Math libraries for the bulk of the tasks, with additional support from SciPy."
    )
    st.write(
        "The frontend is thought Streamlit, a visualisation library that allowed for interactivity from the user, through slider and input widgets."
    )
    st.write(
        "The source code for this project can be found on https://github.com/UmairMalik08/BPhO-App."
    )
