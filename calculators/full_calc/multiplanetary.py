# pylint: disable=fixme, invalid-name, too-many-function-args

"""Functions to calculate transition probabilities from multiplanetary states."""

from functools import cache
import yaml

import runtime_constants as constant
from graph_functions import sigmoid_curved_risk, exponentially_decaying_risk
from params import Params

params = Params().dictionary['multiplanetary']

@cache
def extinction_given_multiplanetary(q):
    """Probability of transitioning to extinction given a multiplanetary state with q
    settlements."""
    return parameterised_decaying_transition_probability('extinction', q=q)

def preindustrial_given_multiplanetary():
    """Sum of total preindustrial exit probability over all values of q. Returns 0 on default
    values"""
    return parameterised_decaying_transition_probability('preindustrial')

def industrial_given_multiplanetary():
    """Sum of total industrial exit probability over all values of q. Returns 0 on default values"""
    return parameterised_decaying_transition_probability('industrial')

@cache
def interstellar_given_multiplanetary(q):
    """Max value should get pretty close to 1, since at a certain number of planets the tech is all
    necessarily available and you've run out of extra planets to spread to.

    TODO need to specify behaviour for max value."""

    def x_stretch():
        return params['interstellar']['x_stretch'] # Just intuition

    def y_stretch():
        # TODO - if this asymptotes too fast, we might get invalid total probabilities. Is there a
        # neat way to guard against that?
        return params['interstellar']['y_stretch']

    def x_translation():
        return params['interstellar']['x_translation']

    def sharpness():
        return params['interstellar']['sharpness']

    # Graph with these values: https://www.desmos.com/calculator/vdyih29fqb
    return sigmoid_curved_risk(q, x_stretch(), y_stretch(), x_translation(), sharpness())

@cache
def parameterised_decaying_transition_probability(target_state, q=None):
    """Calculate the overall probability of transition for specified value of q given
    user-determined params"""
    if params[target_state]['two_planet_risk'] == 0:
        return 0

    @cache
    def starting_value():
        return params[target_state]['two_planet_risk']

    @cache
    def decay_rate():
        return params[target_state]['decay_rate']

    @cache
    def min_risk():
        return params[target_state]['min_risk']

    @cache
    def x_translation():
        return params[target_state]['x_translation']

    return exponentially_decaying_risk(
        x=q,
        starting_value=starting_value(),
        decay_rate=decay_rate(),
        min_probability=min_risk(),
        x_translation=x_translation())

@cache
def transition_to_n_planets_given_multiplanetary(q, n):
    """Should be a value between 0 and 1. Lower treats events that could cause regression to a
    1-planet civilisation in a perils state as having their probability less reduced by having
    multiple settlements.

    On the inside view it seems like the decay rate could be either a) higher than for extinction,
    since late-development AI seems like the main extinction risk at this stage, and that might be
    as able to destroy multiple settlements as it is one, or b) lower than for extinction, since AI
    risk seems like it would peak early and then rapidly decline if it doesn't kill us almost
    immediately.

    On the outside view, it seems like it should be slightly lower, since a multiplanetary
    civilisation provides less evidence against the probability of regressing to perils than it does
    against the probability of going extinct.

    So on balance I err towards making it slightly lower.
    """
    n_params = params['n_planets']

    def any_intra_multiplanetary_regression(q):
        return exponentially_decaying_risk(x=q,
                                        starting_value=n_params['two_planet_risk'],
                                        decay_rate=n_params['decay_rate'],
                                        x_translation=n_params['x_translation'],
                                        min_probability=n_params['min_risk'])

    def remainder_outcome(q):
        return 1 - (extinction_given_multiplanetary(q)
                    + preindustrial_given_multiplanetary()
                    + industrial_given_multiplanetary()
                    + any_intra_multiplanetary_regression(q)
                    + interstellar_given_multiplanetary(q)) # perils_given_multiplanetary is
                                                            # implicitly included as
                                                            # any_intra_multiplanetary_regression to
                                                            # n = 1

    # TODO does it matter that this commented function is unused?
    # def min_risk():
    #     return N_PARAMS['min_risk']

    if not n:
        # Allows us to check total probability sums to 1
        # TODO this branch prob obsolete now
        return any_intra_multiplanetary_regression(q)
    if n == q + 1:
        # This is our catchall branch - the probability is whatever's left after we decide all the
        # other risks
        return remainder_outcome(q)

    if n == q and q == constant.MAX_PLANETS:
        # For simplicity, when we hit max planets, we allow looping, and make that our remainder
        # probability
        return remainder_outcome(q)

    if n >= q:
        # We're only interested in changes to number of planets, and assume we can add max 1 at a
        # time
        return 0

    # The commented return value describes the linear decrease described above
    # Uncomment the next two lines if you think this is a more reasonable treatment
    # return any_intra_multiplanetary_regression(q) * ((n + 1)
    #                                               / (1 + (q ** 2)/2 + 3 * q / 2))
    # The commented out return values is the exponential decrease described above. TODO - where?
    geometric_base = n_params['geometric_base']

    numerator_for_n_planets = geometric_base ** n # How relatively likely is it, given
    # some loss, that that loss took us to exactly n planets?
    # TODO - see if this still matches intuitions
    geometric_sum_of_weightings = (geometric_base * (1 - geometric_base ** (q - 1))
                                    / (1 - geometric_base))
    # Thus numerator_for_n_planets / geometric_sum_of_weightings is a proportion; you can play
    # with the values at https://www.desmos.com/calculator/ku0p2iahq3
    return any_intra_multiplanetary_regression(q) * (numerator_for_n_planets / geometric_sum_of_weightings)
                                    # Brackets seem to improve floating point errors at least
                                    # when the contents should be 1

@cache
def perils_given_multiplanetary(q):
    """Ideally this would have a more specific notion of where in a time of perils you expect to end
    up given this transition, but since that could get complicated fast, I'm treating it as going to
    perils year 0 for now.

    Since perils is basically defined as 'modern+ technology but with only 1 planet', we can just
    use the existing formula for this.

    TODO if going to a fixed perils year, make it a later one."""
    return transition_to_n_planets_given_multiplanetary(q, 1)



# exit_probabilities = [extinction_given_multiplanetary(1,11),
#                         preindustrial_given_multiplanetary(1,11),
#                         industrial_given_multiplanetary(1,11),
#                         perils_given_multiplanetary(1,11),
#                         interstellar_given_multiplanetary(1,11)]

# intra_transition_probabilities = [transition_to_n_planets_given_multiplanetary(1, 11, n)
#                                   for n in range(2,21)]

# row = exit_probabilities + intra_transition_probabilities
# # transition_to_n_planets_given_multiplanetary(1, 9, 3)



# TODO - consider reintroducing this checksum
# if not 1 == (extinction_given_multiplanetary(k)
#              + preindustrial_given_multiplanetary(k)
#              + industrial_given_multiplanetary(k)
#              + perils_given_multiplanetary(k)
#              + interstellar_given_multiplanetary(k)):
#   raise InvalidTransitionProbabilities("Transition probabilities from multiplanetary must == 1")
