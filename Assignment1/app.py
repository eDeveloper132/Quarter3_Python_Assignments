import streamlit as st

st.title("Shape Area Calculator")
st.write("Select a shape and enter the required dimensions to calculate its area.")

shape = st.selectbox("Choose a shape:", ["Rectangle", "Circle", "Triangle"])

if shape == "Rectangle":
    length = st.number_input("Enter the length:", min_value=0.0)
    width = st.number_input("Enter the width:", min_value=0.0)
    area = length * width
    st.success(f"The area of the rectangle is: {area}")
elif shape == "Circle":
    radius = st.number_input("Enter the radius:", min_value=0.0)
    area = 3.1416 * radius ** 2
    st.success(f"The area of the circle is: {area}")
elif shape == "Triangle":
    base = st.number_input("Enter the base:", min_value=0.0)
    height = st.number_input("Enter the height:", min_value=0.0)
    area = 0.5 * base * height
    st.success(f"The area of the triangle is: {area}")