import streamlit as st
import pandas as pd
import numpy as np

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    # First Section: Preindustrial given Pre-Equilibrium

    if 'preindustrial_given_pre_equilibrium' not in st.session_state:
        st.session_state.preindustrial_given_pre_equilibrium = 0.5

    def update_preequilibrium_from_slider():
        st.session_state.preindustrial_given_pre_equilibrium = st.session_state['pre_equilibrium_slider_value']

    def update_preindustrial_from_number():
        st.session_state.preindustrial_given_pre_equilibrium = st.session_state['pre_equilibrium_num_input_value']

    st.slider(
        label='Preindustrial given Pre-Equilibrium',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.preindustrial_given_pre_equilibrium,
        step=0.001,
        format="%f",
        on_change=update_preequilibrium_from_slider,
        key='pre_equilibrium_slider_value')

    st.number_input(label='Preindustrial (Number) given pre-equilibrium',
                    value=st.session_state.preindustrial_given_pre_equilibrium,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.001,
                    format="%f",
                    on_change=update_preindustrial_from_number,
                    key='pre_equilibrium_num_input_value')

    st.slider(label='Extinction given Pre-Equilibrium',
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
                    step=0.001,
                    format="%f",
                    on_change=update_preindustrial_from_number,
                    key='preindustrial_num_input_value')

    st.slider(label='Extinction given Preindustrial',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.industrial_given_preindustrial,
            disabled=True, format="%f")


# Third Section: Future perils given preindustrial

with col3:

    if 'future_perils_given_industrial' not in st.session_state:
        st.session_state.future_perils_given_industrial = 0.5

    def update_perils_from_slider():
        st.session_state.future_perils_given_industrial = st.session_state['future_perils_slider_value']

    def update_perils_from_number():
        st.session_state.future_perils_given_industrial = st.session_state['future_perils_num_input_value']

    st.slider(
        label='Future perils (slider) given industrial',
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.future_perils_given_industrial,
        step=0.001,
        format="%f",
        on_change=update_perils_from_slider,
        key='future_perils_slider_value')

    st.number_input(label='Future perils (number) given industrial',
                    value=st.session_state.future_perils_given_industrial,
                    min_value=0.0,
                    max_value=1.0,
                    step=0.001,
                    format="%f",
                    on_change=update_perils_from_number,
                    key='future_perils_num_input_value')

    st.slider(label='Extinction given industrial',
            min_value=0.0,
            max_value=1.0,
            value=1 - st.session_state.future_perils_given_industrial,
            disabled=True, format="%f")





# # Section 4: Transitions from present perils

# def update_present_perils_ex_extinction_from_slider():
#     st.session_state.extinction_given_present_perils = st.session_state['present_perils_extinction_slider_value']
#     if remainder() < 0:
#         st.session_state.preindustrial_given_present_perils += remainder()

# def update_present_perils_ex_preindustrial_from_slider():
#     st.session_state.preindustrial_given_present_perils = st.session_state['present_perils_preindustrial_slider_value']
#     if remainder() < 0:
#         st.session_state.extinction_given_present_perils += remainder()

def multiplanetary_probability():
    if remainder() >= 0:
        return remainder()
    return .0

def remainder():
    return 1 - sum([st.session_state[transition] for transition in specifiable_transitions])

specifiable_transitions = [
    'extinction_given_present_perils',
    'preequilibrium_given_present_perils',
    'preindustrial_given_present_perils',
    'industrial_given_present_perils',
    'future_perils_given_present_perils',
    'interstellar_given_present_perils'
]

for transition in specifiable_transitions:
    if transition not in st.session_state:
        st.session_state[transition] = 0.1

if 'remainder' not in st.session_state:
    st.session_state.remainder = remainder()

def update_transitions_given_present_perils_from_slider(transition_name):
    other_transitions = [transition for transition in specifiable_transitions if transition != transition_name]
    st.session_state[transition_name] = st.session_state[transition_name + '_slider_value']
    # Reduce the values of the other transitions as much as need be to ensure that the sum of all transitions is 1
    excess_probability = -remainder()
    for transition in reversed(other_transitions):
        if excess_probability > 0 and excess_probability <= st.session_state[transition]:
            # The difference is low enough to be absorbed by this transition, so we're done adjusting sliders
            st.session_state[transition] += remainder()
            break
        elif excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition]
            st.session_state[transition] = .0
        # If excess_probability is negative or 0, it will be added to the multiplanetary transition probability


def make_on_change_callback(transition_name):
    def callback():
        update_transitions_given_present_perils_from_slider(transition_name)
    return callback

for transition in specifiable_transitions:
    st.slider(
    label=transition,
    min_value=0.0,
    max_value=1.0,
    value=st.session_state[transition],
    step=0.001,
    format="%f",
    on_change=make_on_change_callback(transition),
    key=transition + '_slider_value')

multiplanetary = st.slider(
    label='Multiplanetary given present perils',
    min_value=0.0,
    max_value=1.0,
    value=multiplanetary_probability(),
    disabled=True, format="%f")

# st.slider(
#     label='Extinction (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.extinction_given_present_perils,
#     step=0.001,
#     format="%f",
#     on_change=update_present_perils_ex_extinction_from_slider,
#     key='present_perils_extinction_slider_value')

# st.slider(
#     label='Preindustrial (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.preindustrial_given_present_perils,
#     step=0.001,
#     format="%f",
#     on_change=update_present_perils_ex_preindustrial_from_slider,
#     key='present_perils_preindustrial_slider_value')






# Initialization of slider values if not present
# keys = [
#     'extinction',
#     'preequilibrium',
#     'preindustrial',
#     'industrial',
#     'future_perils',
#     'interstellar'
# ]

# for key in keys:
#     if key not in st.session_state:
#         st.session_state[key] = 0.1

# def adjust_sliders(exclude_key):
#     available_balance = 1 - st.session_state[exclude_key]
#     for key in keys:
#         if key != exclude_key:
#             if st.session_state[key] > available_balance:
#                 st.session_state[key] = available_balance
#             available_balance -= st.session_state[key]

# # Save previous states to detect which slider was changed
# previous_states = {key: st.session_state[key] for key in keys}

# # Display sliders
# for key in keys:
#     st.session_state[key] = st.slider(
#         label=f'{key.capitalize()} given present perils',
#         min_value=0.0,
#         max_value=1.0,
#         value=st.session_state[key],
#         step=0.001,
#         format="%f"
#     )

# # Determine the last adjusted slider
# last_adjusted = next((key for key in keys if st.session_state[key] != previous_states[key]), None)

# if last_adjusted:
#     adjust_sliders(last_adjusted)

# # Display the total
# total = sum(st.session_state[key] for key in keys)
# st.write(f"Total of sliders: {total:.3f}")

# # Calculate and display the multiplanetary slider value
# multiplanetary = 1 - total
# st.slider(label='Multiplanetary given present perils',
#          min_value=0.0,
#          max_value=1.0,
#          value=multiplanetary,
#          disabled=True, format="%f")








# # Manual input version

# # Initialization
# slider_labels = [
#     'Extinction given present perils',
#     'Preequilibrium given present perils',
#     'Preindustrial given present perils',
#     'Industrial given present perils',
#     'Future perils given present perils',
#     'Interstellar given present perils'
# ]

# slider_keys = [
#     'extinction',
#     'preequilibrium',
#     'preindustrial',
#     'industrial',
#     'future_perils',
#     'interstellar'
# ]

# for key in slider_keys:
#     if key not in st.session_state:
#         st.session_state[key] = 0.1

# # Display sliders
# for label, key in zip(slider_labels, slider_keys):
#     st.session_state[key] = st.slider(
#         label=label,
#         min_value=0.0,
#         max_value=1.0,
#         value=st.session_state[key],
#         step=0.001,
#         format="%f"
#     )

# # Display the total
# total = sum(st.session_state[key] for key in slider_keys)
# st.write(f"Total of sliders: {total:.3f}")

# # Warning and auto-adjust proposal if total exceeds 1
# if total > 1:
#     st.warning("The total exceeds 1. Adjust the sliders or see the proposed adjustments below.")
#     if st.button("Show proposed adjustments"):
#         excess = total - 1
#         decrease_per_slider = excess / len(slider_keys)
#         for key, label in zip(slider_keys, slider_labels):
#             proposed_value = max(0, st.session_state[key] - decrease_per_slider)
#             st.write(f"Proposed value for {label}: {proposed_value:.3f}")

# # Calculate and display the multiplanetary slider value
# multiplanetary = 1 - total
# st.slider(label='Multiplanetary given present perils',
#          min_value=0.0,
#          max_value=1.0,
#          value=multiplanetary,
#          disabled=True, format="%f")






# if 'extinction_given_present_perils' not in st.session_state:
#     st.session_state.extinction_given_present_perils = 0.5

# if 'pre_equilibrium_given_present_perils' not in st.session_state:
#     st.session_state.pre_equilibrium_given_present_perils = 0.5

# if 'preindustrial_given_present_perils' not in st.session_state:
#     st.session_state.preindustrial_given_present_perils = 0.5

# if 'industrial_given_present_perils' not in st.session_state:
#     st.session_state.industrial_given_present_perils = 0.5

# if 'future_perils_given_present_perils' not in st.session_state:
#     st.session_state.future_perils_given_present_perils = 0.5

# if 'interstellar_given_present_perils' not in st.session_state:
#     st.session_state.interstellar_given_present_perils = 0.5

# if 'multiplanetary_given_present_perils' not in st.session_state:
#     st.session_state.multiplanetary_given_present_perils = 0.5


# def update_present_perils_from_slider():
#     pass
#     # st.session_state.future_perils_given_industrial = st.session_state['future_perils_slider_value']

# def update_present_perils_from_number():
#     pass
#     # st.session_state.future_perils_given_industrial = st.session_state['future_perils_num_input_value']

# st.slider(
#     label='Extinction (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.extinction_given_present_perils,
#     step=0.001,
#     format="%f",
#     # on_change=update_present_perils_from_slider,
#     key='extinction_given_present_perils_slider_value')

# st.slider(
#     label='Preequilibrium (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.pre_equilibrium_given_present_perils,
#     step=0.001,
#     format="%f",
#     # on_change=update_present_perils_from_slider,
#     key='pre_equilibrium_given_present_perils_slider_value')

# st.slider(
#     label='Preindustrial (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.preindustrial_given_present_perils,
#     step=0.001,
#     format="%f",
#     # on_change=update_present_perils_from_slider,
#     key='preindustrial_given_present_perils_slider_value')

# st.slider(
#     label='Industrial (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.industrial_given_present_perils,
#     step=0.001,
#     format="%f",
#     # on_change=update_present_perils_from_slider,
#     key='industrial_given_present_perils_slider_value')

# st.slider(
#     label='Future perils (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.future_perils_given_present_perils,
#     step=0.001,
#     format="%f",
#     # on_change=update_present_perils_from_slider,
#     key='future_perils_given_present_perils_slider_value')

# st.slider(
#     label='Interstellar (slider) given present perils',
#     min_value=0.0,
#     max_value=1.0,
#     value=st.session_state.future_perils_given_present_perils,
#     step=0.001,
#     format="%f",
#     # on_change=update_present_perils_from_slider,
#     key='interstellar_given_present_perils_slider_value')

# st.slider(label='Multiplanetary given present perils',
#         min_value=0.0,
#         max_value=1.0,
#         value=1 - st.session_state.multiplanetary_given_present_perils,
#         disabled=True, format="%f")

# st.number_input(label='Future perils (number) given industrial',
#                 value=st.session_state.future_perils_given_industrial,
#                 min_value=0.0,
#                 max_value=1.0,
#                 step=0.001,
#                 format="%f",
#                 on_change=update_perils_from_number,
#                 key='future_perils_num_input_value')


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
