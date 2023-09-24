import streamlit as st
import pandas as pd
import numpy as np

# extinction_given_pre_equilibrium = st.slider('Extinction given Pre-equilibrium', .0, 1., step=0.001, format="%f")

# st.number_input(label="Extinction given Pre-equilibrium", )



# Initialize the session state variable if it doesn't exist
# if 'update_number' not in st.session_state:
#     st.session_state.update_number = False
# if 'update_slider' not in st.session_state:
#     st.session_state.update_slider = False
# if 'preindustrial_given_pre_equilibrium' not in st.session_state:
#     st.session_state.preindustrial_given_pre_equilibrium = 0.5


# # Define the on_change functions
# def update_from_slider():
#     # Update the session state
#     st.session_state.preindustrial_given_pre_equilibrium = slider_value

#     # Sync the number input to match the slider value
#     num_input.slider('Preindustrial given Pre-Equilibrium', value=slider_value)

# def update_from_number():
#     # Update the session state
#     st.session_state.preindustrial_given_pre_equilibrium = num_input_value

#     # Sync the slider to match the number input value
#     slider.slider('Preindustrial given Pre-Equilibrium', value=num_input_value)

# slider_value = st.slider(
#     'Preindustrial given Pre-Equilibrium',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.preindustrial_given_pre_equilibrium,
#     step=0.001,
#     format="%f",
#     on_change=update_number)

# # Calculate and display 'extinction_given_pre_equilibrium' based on preindustrial_given_pre_equilibrium
# num_input_value = st.number_input('Preindustrial given Pre-Equilibrium',
#                                     value=st.session_state.preindustrial_given_pre_equilibrium,
#                                     min_value=0.000000,
#                                     step=0.000001,
#                                     max_value=1.,
#                                     format="%f",
#                                     on_change=update_slider)


# # Calculate and display 'extinction_given_pre_equilibrium' based on preindustrial_given_pre_equilibrium
# st.slider('Extinction given Pre-Equilibrium', 0.0, 1.0, 1 - st.session_state.preindustrial_given_pre_equilibrium, disabled=True, format="%f")

# Initialize the session state variable if not present
if 'preindustrial_given_pre_equilibrium' not in st.session_state:
    st.session_state.preindustrial_given_pre_equilibrium = 0.5

# Define the on_change functions
def update_from_slider():
    # Directly use the value from session state, which will have the updated value
    st.session_state.preindustrial_given_pre_equilibrium = st.session_state['slider_value']

def update_from_number():
    # Directly use the value from session state, which will have the updated value
    st.session_state.preindustrial_given_pre_equilibrium = st.session_state['num_input_value']

# Define the slider
st.slider(
    'Preindustrial given Pre-Equilibrium',
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.preindustrial_given_pre_equilibrium,
    step=0.001,
    format="%f",
    on_change=update_from_slider,
    key='slider_value')  # This key will let you access the value in session state

# Define the number input
st.number_input('Preindustrial given Pre-Equilibrium',
                            value=st.session_state.preindustrial_given_pre_equilibrium,
                            min_value=0.000000,
                            step=0.000001,
                            max_value=1.,
                            format="%f",
                            on_change=update_from_number,
                            key='num_input_value')  # This key will let you access the value in session state

# Define the dependent slider
st.slider('Extinction given Pre-Equilibrium', 0.0, 1.0, 1 - st.session_state.preindustrial_given_pre_equilibrium, disabled=True, format="%f")
# # Create an input field for 'preindustrial_given_pre_equilibrium'
# preindustrial_given_pre_equilibrium = 1 - st.session_state.extinction_given_pre_equilibrium
# new_preindustrial = st.number_input('Preindustrial given Pre-Equilibrium',
#                                     value=preindustrial_given_pre_equilibrium,
#                                     min_value=0.000000,
#                                     step=0.000001,
#                                     max_value=1.,
#                                     format="%f")

# # Calculate 'extinction_given_pre_equilibrium' based on the entered value
# st.session_state.extinction_given_pre_equilibrium = 1 - new_preindustrial
# st.write(f'Extinction given Pre-Equilibrium: {st.session_state.extinction_given_pre_equilibrium}')

# st.write("""
#     On your assumptions...
#     The probability of becoming interstellar from a pre_equilibrium state = {{ calc.net_interstellar_from_pre_equilibrium() }}
#     The probability of becoming interstellar from a preindustrial state = {{ calc.net_interstellar_from_preindustrial() }}
#     The probability of becoming interstellar from an industrial state = {{ calc.net_interstellar_from_industrial() }}
#     The probability of becoming interstellar from a time of perils state = {{ calc.net_interstellar_from_perils() }}</p>
#     The probability of becoming interstellar from a multiplanetary state = {{ calc.net_interstellar_from_multiplanetary() }}</p>

#     *****

#     Therefore, if we consider eventual extinction and interstellar colonisation the only two outcomes...
#     a castatrophe that put us into a pre-equilibrium state would be {{ calc.pre_equilibrium_probability_reduction() }} as bad as an extinction event
#     a castatrophe that put us into a preindustrial state would be {{ calc.preindustrial_probability_reduction() }} as bad as an extinction event
#     a castatrophe that put us into an industrial state would be {{ calc.industrial_probability_reduction() }} as bad as an extinction event
#     and if we reached a multiplanetary state, it would increase our chance of becoming interstellar by {{ calc.multiplanetary_probability_increase() }}
# """)
