import streamlit as st
import pandas as pd
import numpy as np

col1, col2 = st.columns(2, gap="large")

with col1:
    # First Section: Preindustrial given Pre-Equilibrium

    if 'preindustrial_given_pre_equilibrium' not in st.session_state:
        st.session_state.preindustrial_given_pre_equilibrium = 0.5

    def update_preequilibrium_from_slider():
        st.session_state.preindustrial_given_pre_equilibrium = st.session_state['pre_equilibrium_slider_value']

    st.slider(
        label='Preindustrial given Pre-Equilibrium',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.preindustrial_given_pre_equilibrium,
        step=0.001,
        format="%f",
        on_change=update_preequilibrium_from_slider,
        key='pre_equilibrium_slider_value')

    st.slider(label='Extinction (1) given Pre-Equilibrium',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.preindustrial_given_pre_equilibrium,
            disabled=True, format="%f")


# Second Section: Industrial given Preindustrial

with col2:

    if 'industrial_given_preindustrial' not in st.session_state:
        st.session_state.industrial_given_preindustrial = 0.5

    def update_preindustrial_from_slider():
        st.session_state.industrial_given_preindustrial = st.session_state['preindustrial_slider_value']

    def update_preindustrial_from_number():
        st.session_state.industrial_given_preindustrial = st.session_state['preindustrial_num_input_value']

    st.slider(
        label='Industrial (Slider) given Preindustrial',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.industrial_given_preindustrial,
        step=0.001,
        format="%f",
        on_change=update_preindustrial_from_slider,
        key='preindustrial_slider_value')

    st.number_input(label='Industrial (Number) given Preindustrial',
                    value=st.session_state.industrial_given_preindustrial,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.000001,
                    format="%f",
                    on_change=update_preindustrial_from_number,
                    key='preindustrial_num_input_value')

    st.slider(label='Extinction (2) given Preindustrial',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.industrial_given_preindustrial,
            disabled=True, format="%f")

# if 'industrial_given_preindustrial' not in st.session_state:
#     st.session_state.industrial_given_preindustrial = 0.5

# def update_preindustrial_from_slider():
#     st.session_state.industrial_given_preindustrial = st.session_state['preindustrial_slider_value']

# def update_preindustrial_from_number():
#     st.session_state.industrial_given_preindustrial = st.session_state['preindustrial_num_input_value']

# st.slider(
#     label='Industrial (Slider) given Preindustrial',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.industrial_given_preindustrial,
#     step=0.001,
#     format="%f",
#     on_change=update_preindustrial_from_slider,
#     key='preindustrial_slider_value')

# st.number_input(label='Industrial (Number) given Preindustrial',
#                 value=st.session_state.industrial_given_preindustrial,
#                 min_value=0.0,
#                 max_value=1.0,
#                 step=0.000001,
#                 format="%f",
#                 on_change=update_preindustrial_from_number,
#                 key='preindustrial_num_input_value')

# st.slider(label='Extinction (2) given Preindustrial',
#         min_value=0.0,
#         max_value=1.0,
#         value=1 - st.session_state.industrial_given_preindustrial,
#         disabled=True, format="%f")


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
