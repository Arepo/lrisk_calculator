# pylint: disable=too-many-function-args

"""Functions to calculate the transitional probabilities from time of perils states."""

from functools import cache

import calculators.full_calc.runtime_constants as constant
from calculators.full_calc.graph_functions import sigmoid_curved_risk
from calculators.full_calc.params import Params

params = Params().dictionary['perils']

@cache
def preindustrial_given_perils(k, progress_year):
    """Probability of transitioning to a preindustrial state given some number
    of progress years into the perils state of the kth civilisation"""
    return _parameterised_transition_probability(k, progress_year, 'preindustrial')

@cache
def industrial_given_perils(k, progress_year):
    """Probability of transitioning to an industrial state given some number of
    progress years into the perils state of the kth civilisation"""
    return _parameterised_transition_probability(k, progress_year, 'industrial')

@cache
def multiplanetary_given_perils(k, progress_year):
    """Probability of transitioning to a multiplanetary state given some number
    of progress years into the perils state of the kth civilisation"""
    return _parameterised_transition_probability(k, progress_year, 'multiplanetary')

@cache
def extinction_given_perils(k, progress_year):
    """Probability of transitioning to extinction given some number of progress
    years into the perils state of the kth civilisation"""
    return _parameterised_transition_probability(k, progress_year, 'extinction')

@cache
def interstellar_given_perils(k, progress_year):
    """Probability of transitioning to an interstellar state given some number
    of progress years into the perils state of the kth civilisation"""
    return _parameterised_transition_probability(k, progress_year, 'interstellar')

def _parameterised_transition_probability(k, progress_year, target_state):
    if k == 0:
        # Some kruft required to deal with values potentially being 0
        base_x_stretch = params[target_state].get('current_perils_base_x_stretch')
        base_x_stretch = base_x_stretch if base_x_stretch is not None else params[target_state]['base_x_stretch']
        x_stretch_stretch = params[target_state].get('current_perils_stretch_per_reboot')
        x_stretch_stretch = (x_stretch_stretch if x_stretch_stretch is not None else params[target_state]['stretch_per_reboot']) ** k
        y_stretch = params[target_state].get('current_perils_y_stretch')
        y_stretch = y_stretch if y_stretch is not None else params[target_state]['y_stretch']
        x_translation = params[target_state].get('current_perils_x_translation')
        x_translation = x_translation if x_translation is not None else params[target_state]['x_translation']
        sharpness = params[target_state].get('current_perils_sharpness')
        sharpness = sharpness if sharpness is not None else params[target_state]['sharpness']
    else:
        base_x_stretch = params[target_state]['base_x_stretch']
        x_stretch_stretch = params[target_state]['stretch_per_reboot'] ** k
        y_stretch = params[target_state]['y_stretch']
        x_translation = params[target_state]['x_translation']
        sharpness = params[target_state]['sharpness']

    total_x_stretch = base_x_stretch * x_stretch_stretch

    @cache
    def background_risk():
        # Exponent should be >0, since this is a probability that should be settable to 0 (and can't
        # be if the exponent is 0)
        return (params[target_state]['per_civilisation_background_risk_numerator'] ** (k + 1)
                /params[target_state]['base_background_risk_denominator'])

    return background_risk() + sigmoid_curved_risk(
        x=progress_year,
        x_stretch=total_x_stretch,
        y_stretch=y_stretch,
        x_translation=x_translation,
        sharpness=sharpness)

@cache
def transition_to_year_n_given_perils(k:int, progress_year:int, n=None):
    """Probability of transitioning to progress year n given some number of
    progress years into the kth time of perils"""
    possible_regressions = progress_year + 1

    if possible_regressions == constant.MAX_PROGRESS_YEARS:
        # We're at the maximum allowable number of progress years, so lose the 'regression' of
        # staying on the spot (which becomes our remainder)
        possible_regressions -= 1

    if n > possible_regressions:
        # We only allow progress to increment by up to one.
        return 0

    def any_intra_perils_regression():
        """How likely is it in total we regress any number of progress years between 0 and p
        inclusive?"""
        return params['progress_year_n']['any_regression']

    if n == possible_regressions:
        # The probability of advancing one progress year
        return 1 - (extinction_given_perils(k, progress_year)
                    + preindustrial_given_perils(k, progress_year)
                    + industrial_given_perils(k, progress_year)
                    + any_intra_perils_regression()
                    + multiplanetary_given_perils(k, progress_year)
                    + interstellar_given_perils(k, progress_year))




    def exponential_algorithm():
        if possible_regressions - n > constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS:
            # We round to 0 when numbers get small enough, so we don't have to deal with fractions like
            # ~a^10000/2a^10000 in the geometric sequence below
            return 0

        # If we get this far, we're setting up to calculate the division of the total probability of
        # any_intra_perils_regression() into the specific probability of a regression to year n
        if possible_regressions > constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS:
            # Reduce large numbers to the minimum, eg regression from progress-year 1000 from
            # progress-year 950 with max_distance 100 becomes regression from PY 100 to PY 50. This way
            # we ensure proportions still sum to 0.
            max_regressed_states = constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS
            target_year = n - (possible_regressions - constant.MAX_PROGRESS_YEAR_REGRESSION_STEPS)
        else:
            max_regressed_states = possible_regressions
            target_year = n

        geometric_base = params['progress_year_n']['geometric_base']

        # TODO cache this value, probably for each value of possible_regressions
        geometric_sum_of_weightings = ( (1 - geometric_base ** max_regressed_states)
                                        / (1 - geometric_base))

        numerator_for_progress_year_n = geometric_base ** target_year # How likely is it, that given
        # some loss, that loss took us to exactly progress year n?

        # Thus numerator_for_progress_year_n / geometric_sum_of_weightings is a proportion; you can play
        # with the values at https://www.desmos.com/calculator/1pcgidwr3f
        return (any_intra_perils_regression() * numerator_for_progress_year_n
                / geometric_sum_of_weightings)

    def linear_algorithm():
        """Probabilities of regressing n years are given by n/k, where k is the sum of all values of n
        up to the number of possible regressions (p+1))"""
        r = possible_regressions

        # In the following sum our starting value is always 1, as is our common difference
        # (because for high numbers of possible regressions, the fractional changes of among different
        # common differences are negligible)
        # and r = the number of terms = p+1 except if we're at the maximal allowable number of progress
        # years (since in progress year 0 we can 'regress' up to once, to progress
            # year 0, and so on)
        # TODO cache this value, probably for each value of possible_regressions
        arithmetic_sequence_sum = r/2 * (1 + r)

        return (n + 1) / arithmetic_sequence_sum * any_intra_perils_regression()

    def mean_algorithm():
        "Returns the mean of the linear and exponential algorithms"
        return (exponential_algorithm() + linear_algorithm()) / 2

    if params['progress_year_n']['algorithm'] == 'exponential':
        return exponential_algorithm()
    elif params['progress_year_n']['algorithm'] == 'linear':
        return linear_algorithm()
    elif params['progress_year_n']['algorithm'] == 'mean':
        return mean_algorithm()
    else:
        raise "Invalid algorithm given for progress_year_n"


# The functions below single out AI for special treatment, and will not be used in the MVP (and may
# become redundant afterwards).

# def _ai_x_translation():
#     return params['extinction']['agi_development']['x_translation']

# def annual_ai_first_development_probability(p):
#   def gamma_shape():
#     return params['extinction']['agi_development']['shape']

#   def gamma_scale():
#     return params['extinction']['agi_development']['scale']

#   return gamma.pdf(p, gamma_shape(), loc=_ai_x_translation(), scale=gamma_scale())
