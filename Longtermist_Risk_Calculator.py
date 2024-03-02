# pylint: disable=line-too-long, invalid-name, redefined-outer-name, fixme
# pylint: disable=pointless-string-statement, consider-using-f-string

"""Main page of the Streamlit app."""

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from calculators.simple_calc.simple_calc import SimpleCalc
st.set_page_config(
        page_title="L-risk calculator",
)

# TODO Add Sankey diagram

all_transitions = {
    'from preindustrial': [
        'Extinction',
        'Industrial'
    ],
    'from industrial': [
        'Extinction',
        'Future time of perils'
    ],
    'from present perils': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        "A 'minor' technological regression†",
        'Multiplanetary††',
        'Interstellar/existential security'
    ],
    'from future perils': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        'Multiplanetary††',
        'Interstellar/existential security'
    ],
    'from multiplanetary': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        'Future perils',
        'Interstellar/existential security'
    ],
    'from abstract state': [
        'Extinction',
        'Preindustrial',
        'Industrial',
        "A 'minor' technological regression†",
        'Multiplanetary††',
        'Interstellar/existential security'
    ]
}

obelus_string = """<span style="font-size:0.8em;">† Defined as an event that effectively reset the modern era, i.e. technologically regressed us the equivalent of about about 50-100 years, but left us with nuclear arsenals or other comparatively destructive weaponry.</span>

<span style="font-size:0.8em;">†† Defined as civilisation having established self-sustaining settlements on more than one planet.</span>"""

last_listed_transitions = [transitions[-1] + " " + origin_state for origin_state, transitions in all_transitions.items()]

# Get a flattened list of all transitions
target_states = [target_state + " " + origin_state for origin_state, target_state_list in all_transitions.items()
                 for target_state in target_state_list]

concrete_transitions = [state for state in target_states if not state.endswith('from abstract state')]

common_form_values = {
    'min_value': 0.0,
    'max_value': 1.0,
    'step': 0.01,
    'format': "%.2f",
}

def set_query_params():
    """Add a query string to represent each of the current set of form values"""
    query_params = {transition: value
                    for transition, value in st.session_state.items()
                    if transition in concrete_transitions}
    st.experimental_set_query_params(**query_params)


def update_transitions(transition_name, current_state):
    """For every transitional probability from the current state, update the value of the slider"""
    other_transitions = [transition for transition in all_transitions[current_state]
                         if transition != transition_name][::-1]
    st.session_state[transition_name + " " + current_state] = st.session_state[
        transition_name + " " + current_state + '_from_input']
    # Given the change, determine how much we need to adjust other transitional probabilities to
    # ensure they sum to 1
    excess_probability = sum(st.session_state[transition + ' ' + current_state] for transition in all_transitions[current_state]) - 1

    for transition in other_transitions:
        # If excess_probability is positive that means we've lowered the value of the transition
        # we're updating, and need to raise another
        if 0 < excess_probability <= st.session_state[transition  + " " + current_state]:
            # The difference is low enough to be absorbed by this transition, so we're done
            # adjusting sliders
            st.session_state[transition + " " + current_state] += -excess_probability
            break
        if excess_probability > 0:
            # Reduce this transition to 0 and continue to the next
            excess_probability -= st.session_state[transition + " " + current_state]
            st.session_state[transition + " " + current_state] = .0
    # If excess_probability is negative or 0, we add the difference it to extinction unless it's
    # extinction we modified, then we add it to the next-most regressed state)
    if excess_probability < 0 and transition_name + " " + current_state in last_listed_transitions:
        st.session_state[all_transitions[current_state][-2] + " " + current_state] -= excess_probability
    elif excess_probability < 0:
        st.session_state[all_transitions[current_state][-1] + " " + current_state] -= excess_probability
    set_query_params()

for session_value in target_states:
    # Determine values in session state, from query strings first, else recent user input, else
    # default to 0s and 1s
    query_params = st.experimental_get_query_params()
    if session_value in query_params:
        st.session_state[session_value] = float(query_params[session_value][0])
    elif session_value.endswith('from abstract state') and session_value not in st.session_state:
        st.session_state[session_value] = st.session_state[session_value.replace('from abstract state', 'from present perils')]
    elif session_value not in st.session_state and session_value in last_listed_transitions:
        st.session_state[session_value] = 1.0
    elif session_value not in st.session_state:
        st.session_state[session_value] = .0

def make_on_change_callback(transition_name, origin_state):
    """Create a function to allow us to pass the transition name to the callback"""
    def callback():
        update_transitions(transition_name, origin_state)
    return callback


st.write("#### The tool below allows you to give credences representing the transitional probabilities in the following diagram (descriptions below):")

st.image('https://39669.cdn.cke-cs.com/cgyAlfpLFBBiEjoXacnz/images/a4fab3864e51d5ecf59ea5a9d82e9ed8cbb98e30d914ba37.png/w_1170')

st.write("""_Extinction_: Extinction of whatever type of life you value any time inclusively between now and our sun’s death (i.e. any case where we've failed to develop interplanetary technology that lets us escape the event).

_Preindustrial_: Civilisation has regressed to [pre-first-industrial-revolution](https://www.britannica.com/money/topic/Industrial-Revolution/The-first-Industrial-Revolution)-equivalent technology.

_Industrial_: Civilisation has technology comparable to the first industrial revolution but does not yet have the technological capacity to do enough civilisational damage to regress to a previous state (e.g. nuclear weapons, biopandemics etc). A formal definition of industrial revolution technology is tricky but seems unlikely to dramatically affect probability estimates. In principle it could be something like '[kcals captured per capita](https://lukemuehlhauser.com/three-wild-speculations-from-amateur-quantitative-macrohistory/) go up more than 5x as much in a 100 year period as they had in any of the previous five 100-year periods.’

_Current perils_: Our current state, as of 1945, when we developed nuclear weaponry - what Carl Sagan called the ‘time of perils’.

_Future perils_: Human development has had a serious setback, and also has technology capable of threatening another serious contraction (such as nuclear weaponry, misaligned AI, etc.) but does not yet have multiple spatially isolated self-sustaining settlements. Arguably we could transition directly to this directly from our current state if there were a global shock sufficient to destroy much modern technology, but small enough to leave our nuclear arsenals and a decent fraction of industry intact or very quickly recoverable.

_Multiplanetary_: Civilisation has progressed to having at least two spatially isolated self-sustaining settlements capable of continuing in an advanced enough technological state to produce further such settlements even if all the others disappeared. Each settlement must be physically isolated enough to be unaffected by at least one type of technological milestone catastrophe impacting the other two (e.g. another planet, a hollowed out asteroid or an _extremely_ well-maintained bunker system). Although each settlement may face local threats, we might assume the risks to humanity as a whole, of either extinction or regression to reduced-technology-states, declines as the number of settlements increases.

_Interstellar_: Civilisation has progressed to having at least two self-sustaining colonies in different star systems, or gains existential security in some other way.""")

# Make values percentages

st.write("#### Now adjust the values to see how the overall probability of human descendants becoming interstellar"\
         " changes based on your credences.")

col1, col2 = st.columns(2, gap="large")


# First Section: Industrial given Preindustrial

with col1:
    st.write("""**What is the probability any time civilisation reverts to a _preindustrial_ state,
             that it directly transitions to either of the following states (assuming those are the
             only possible outcomes)?**""")

    for transition in all_transitions['from preindustrial']:
        st.slider(
            label=transition,
            value=st.session_state[transition + " " +  'from preindustrial'],
            on_change=make_on_change_callback(transition, 'from preindustrial'),
            key=transition + " " + 'from preindustrial' + "_from_input",
            **common_form_values)

# Second Section: Future perils given preindustrial

with col2:
    st.write("""**What is the probability any time civilisation enters an _industrial_
             state that it directly transitions to
             either of the following states (assuming those are the only possible outcomes)?**""")

    for transition in all_transitions['from industrial']:
        st.slider(
            label=transition,
            value=st.session_state[transition + " " + 'from industrial'],
            on_change=make_on_change_callback(transition,  'from industrial'),
            key=transition + " " + 'from industrial' + "_from_input",
            **common_form_values)

# # Section 3: Transitions from present perils

'---'
st.markdown("""## Transitional probabilities from the <span style='color: #07A0A3;'>current 'time of perils'</span>
""", unsafe_allow_html=True)

st.write("""**From our current state (postindustrial, dependent on a single planet, high-tech weaponry available),
         what is the probability that civilisation transitions directly to the following states?
         (assuming those are the only possible outcomes)?**""")

def make_on_change_present_perils_callback(transition_name):
    """Create a function to allow us to pass the transition name to the callback, and to update the
    probabilities of abstract state to match"""
    def callback():
        update_transitions(transition_name, 'from present perils')
        for state in all_transitions['from present perils']:
            st.session_state[state + " " + 'from abstract state'] = st.session_state[state + " " + 'from present perils']
    return callback

for transition in all_transitions['from present perils']:
    st.slider(
        label=transition,
        value=st.session_state[transition + " " + 'from present perils'],
        on_change=make_on_change_present_perils_callback(transition),
        key=transition + " " + 'from present perils' + "_from_input",
        **common_form_values)

st.markdown(obelus_string, unsafe_allow_html=True)

# Section 4 - Transitional probabilities from future perils states

'---'

st.markdown("""## Transitional probabilities from any <span style='color: #FF8000;'>future 'times of perils'</span>
""", unsafe_allow_html=True)

st.write("""**If future civilisations ever regain technology resembling our current level
         (postindustrial, dependent on a single planet, high-tech weaponry available), what is the probability
         that they will transitions directly to the following states?
         (assuming those are the only possible outcomes)?**""")

for transition in all_transitions['from future perils']:
    st.slider(
    label=transition,
    value=st.session_state[transition + " " + 'from future perils'],
    on_change=make_on_change_callback(transition, 'from future perils'),
    key=transition + " " + 'from future perils' + "_from_input",
    **common_form_values)



# Section 5 Transitional probabilities from multiplanetary states

'---'

st.markdown("""## Transitional probabilities from <span style='color: #6600CC;'>multiplanetary</span> states"""
            , unsafe_allow_html=True)

st.write("""**If civilisation ever develops self-sustaining settlements on more than one planets),
         what is the probability that they will transitions directly to the following states?
         (assuming those are the only possible outcomes)?**""")

for transition in all_transitions['from multiplanetary']:
    st.slider(
    label=transition,
    value=st.session_state[transition + " " + 'from multiplanetary'],
    on_change=make_on_change_callback(transition, 'from multiplanetary'),
    key=transition + " " + 'from multiplanetary' + "_from_input",
    **common_form_values)

'---'

st.markdown("""## Comparing the value of outcomes""")

all_transition_probabilities = {
    'extinction_given_preindustrial': st.session_state['Extinction from preindustrial'],
    'extinction_given_industrial': st.session_state['Extinction from industrial'],

    'extinction_given_present_perils': st.session_state['Extinction from present perils'],
    'preindustrial_given_present_perils': st.session_state['Preindustrial from present perils'],
    'industrial_given_present_perils': st.session_state['Industrial from present perils'],
    'future_perils_given_present_perils': st.session_state["A 'minor' technological regression† from present perils"],
    'interstellar_given_present_perils': st.session_state['Interstellar/existential security from present perils'],

    'extinction_given_future_perils': st.session_state['Extinction from future perils'],
    'preindustrial_given_future_perils': st.session_state['Preindustrial from future perils'],
    'industrial_given_future_perils': st.session_state['Industrial from future perils'],
    'interstellar_given_future_perils': st.session_state['Interstellar/existential security from future perils'],

    'extinction_given_multiplanetary': st.session_state['Extinction from multiplanetary'],
    'preindustrial_given_multiplanetary': st.session_state['Preindustrial from multiplanetary'],
    'industrial_given_multiplanetary': st.session_state['Industrial from multiplanetary'],
    'future_perils_given_multiplanetary': st.session_state['Future perils from multiplanetary'],
}

calc = SimpleCalc(**all_transition_probabilities)
mc = calc.markov_chain()
success_probabilities = mc.absorption_probabilities()[1]
data = dict(zip(mc.transient_states, success_probabilities))
probabilities_df = pd.DataFrame(
    data.items(),
    columns=['Civilisation state', 'Probability of becoming interstellar'])

st.markdown(f"### tl;dr: we have a {round(success_probabilities[2] * 100)}% chance of becoming interstellar")


st.markdown("""<h6 style="text-align: center;">
            Prospects from each state:
            </h6>""", unsafe_allow_html=True)

standard_blue = '#2968c3'
highlighted_red = '#c32929'
color_map = {
    'Preindustrial': standard_blue,
    'Industrial': standard_blue,
    'Present perils': highlighted_red,
    'Future perils': standard_blue,
    'Multiplanetary': standard_blue
}

probabilties_fig = px.bar(probabilities_df,
                          x='Civilisation state',
                          y='Probability of becoming interstellar',
                          color='Civilisation state',
                          color_discrete_map=color_map)

st.plotly_chart(probabilties_fig, use_container_width=True)


st.markdown("""
Let $V$ be the value we imagine of humans becoming interstellar and $V_{\\text{state}}$ be
the event that we attain that state. We assume that by the time we reach pass some
threshhold, like settling around the first other star, we are either now
existentially secure (hence have attained V in expectation) or never will be
(see [see this footnote](https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/YnBwoNNqe6knBJH8p#fncubjw6vmka) for rationale for this).

Let $T_{\\text{state}}$ be some event that transitions us to some other state
than 'present perils', for example, 'nuclear war that destroys all industry in
next 10 years' or 'humans develop self-sustaining offworld settlement before
2070'.
Thus:
- $P(V_{\\text{state}} | T_{\\text{state}})$ is the probability of becoming interstellar from
the state $T_{\\text{state}}$ would transition us to,
- $P(V_{\\text{state}} | \\neg T_{\\text{state}})$ is the probability of becoming interstellar
from our current state, given that $T_{\\text{state}}$ doesn't occur.

We can then express the expected value of $T_{\\text{state}}$ in terms of $V$, as
""", unsafe_allow_html=True)
st.latex(r'''
\mathbb{E}[T_{\text{state}}] = V \cdot \left( P[V_{\text{state}} | T_{\text{state}}] - P[V_{\text{state}} | \neg T_{\text{state}}] \right)
''')

difference_df = pd.DataFrame(
    calc.probability_differences().items(),
    columns=['State', 'Value of transitioning to state (as a multiple of V)'])
difference_fig = px.bar(
    difference_df,
    x='State',
    y='Value of transitioning to state (as a multiple of V)')

st.markdown("""<h6 style="text-align: center;">
            Value of each transition in terms of <em>V</em>:
            </h6>""", unsafe_allow_html=True)
st.plotly_chart(difference_fig, use_container_width=True)

# TODO This example seems priming
st.markdown("""
We might also represent $T_{\\text{state}}$ as having some fraction of the cost
of an extinction event $T_{\\text{extinction}}$. For example, if you think we
have a 60% chance of becoming interstellar from our current state, and a 50%
chance that we have to restart the time of perils would transition us to, the
loss from $X$ would be $0.6V$, and the loss of transitioning to as a percentage
of the loss of value from $T_{\\text{extinction}}$ would be $100\\frac{(0.6 - 0.5)}{0.6} \\approx 17\\%$.

Negative values are how *good* the transition is, relative to the badness of
extinction (note that since in this model we assume extinction is the worst
outcome, positive percentages are max 100% - the badness of extinction - but
negative values can theoretically be lower than -100% if the current chance of
success is less than 50%).
""", unsafe_allow_html=True)

x='State'
y='Cost of transitioning to state as a percentage of the cost of extinction'
proportion_df = pd.DataFrame(
    calc.probability_proportion_differences().items(),
    columns=[x, y])
proportion_fig = px.bar(
    proportion_df,
    x=x,
    y=y)

st.markdown("""<h6 style="text-align: center;">
            Cost of each transition as proportion of extinction:
            </h6>""", unsafe_allow_html=True)
st.plotly_chart(proportion_fig, use_container_width=True)




# Section 6 - Transitional probabilities from abstract events

'---'

st.markdown("""## Transitional probabilities from abstract events""")

st.markdown("""You could also consider an event, rather than as a transition, to be an adjustment
your credences of the transitions from our current time of perils conditional on the event
happening, to compare the difference it makes to our prospects. This way you can compare the
counterfactual value of 'events' which are 'you work on some cause area'. You can make such
adjustments with fields below (numbers input manually, to allow you arbitrary precision about your
estimate of the outcome):""")

col1, col2, col3 = st.columns(3, gap="small")

precision = 9

for state, col in zip(all_transitions['from abstract state'][:3], (col1, col2, col3)):
    with col:
        st.number_input(
            label=state,
            value=st.session_state[state + " " + 'from abstract state'],
            on_change=make_on_change_callback(state, 'from abstract state'),
            key=state + " " + 'from abstract state' + "_from_input",
            min_value= 0.0,
            max_value= 1.0,
            step= 0.01,
            format= f"%.{precision}f")

for state, col in zip(all_transitions['from abstract state'][3:], (col1, col2, col3)):
    with col:
        st.number_input(
            label=state,
            value=st.session_state[state + " " + 'from abstract state'],
            on_change=make_on_change_callback(state, 'from abstract state'),
            key=state + " " + 'from abstract state' + "_from_input",
            min_value= 0.0,
            max_value= 1.0,
            step= 0.01,
            format= f"%.{precision}f")

st.write(obelus_string, unsafe_allow_html=True)

probability_differences = np.array(list(calc.probability_differences().values()))
counterfactual_transitional_probabilities = (
    np.array([st.session_state[state + " " + 'from abstract state']
              for state in all_transitions['from abstract state']]))

result = np.round(np.dot(probability_differences, counterfactual_transitional_probabilities),
                  precision)
st.markdown("The expected value of the event is ${0}V$.".format(result))

'----'

st.markdown("Your answers are stored in the URL - please share them with others :)")
