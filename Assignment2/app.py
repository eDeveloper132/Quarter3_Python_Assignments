import streamlit as st

conversion_factors = {
    "meter": 1,
    "kilometer": 1000,
    "foot": 0.3048,
    "inch": 0.0254,
    "mile": 1609.34
}

def convert(value, input_unit, output_unit):
    """Convert the value from input_unit to output_unit via meters."""
    input_factor = conversion_factors[input_unit]
    output_factor = conversion_factors[output_unit]
    value_in_meters = value * input_factor
    output_value = value_in_meters / output_factor
    return output_value

st.title("Unit Converter")
st.write("Convert between different units of length.")

units = list(conversion_factors.keys())

col1, col2 = st.columns(2)

with col1:
    st.subheader("From")
    input_unit = st.selectbox("Select unit", units, key="input_unit")
    value = st.number_input("Enter value", min_value=0.0, value=0.0, step=0.1)

with col2:
    st.subheader("To")
    output_unit = st.selectbox("Select unit", units, key="output_unit")

if value is not None:
    result = convert(value, input_unit, output_unit)
    st.write(f"{value} {input_unit} is equal to {result:.4f} {output_unit}")