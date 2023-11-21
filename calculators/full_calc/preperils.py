# pylint: disable=invalid-name

"""Functions to calculate transition probabilities from preperils states."""

from functools import cache
import yaml
from params import Params

params = Params().preperils

@cache
def extinction_given_preindustrial(k):
    """Calculate probability of extinction from preindustrial state in the kth civilisation,
    given user-specified params."""
    p_params = params.preindustrial

    base_expected_time_in_years = p_params.base_expected_time_in_years

    stretch_per_reboot = p_params.stretch_per_reboot

    expected_time_in_years = base_expected_time_in_years * stretch_per_reboot ** k

    extinction_probability_per_year = (1 /
        p_params.extinction_probability_per_year_denominator)

    extinction_probability_per_year = (1 /
        p_params.extinction_probability_per_year_denominator)

    return 1 - ((1 - extinction_probability_per_year) ** expected_time_in_years)

@cache
def industrial_given_preindustrial(k, k1):
    """Calculate probability of extinction from preindustrial state in the kth civilisation,
    as the complement of extinction_given_preindustrial."""
    if k != k1:
        # We can't transition to different civilisations from a preperils state
        return 0
    return 1 - extinction_given_preindustrial(k)

@cache
def extinction_given_industrial(k):
    """Calculate probability of extinction from an industrial state in the kth civilisation,
    given user-specified params."""
    # To allow for some inside view about the first time we reboot, we could
    # have an explicit condition here:
    # if k == 1:
    #   do_something_different

    i_params = params.industrial

    base_annual_extinction_probability = (1 /
        i_params.base_annual_extinction_probability_denominator)

    annual_extinction_probability_multiplier = i_params.annual_extinction_probability_multiplier

    stretch_per_reboot = i_params.stretch_per_reboot

    expected_time_in_years = i_params.base_expected_time_in_years * stretch_per_reboot ** (k - 1)

    return (1 - (1 - base_annual_extinction_probability * annual_extinction_probability_multiplier)
                ** expected_time_in_years)

@cache
def perils_given_industrial(k, k1):
    """Calculate probability of extinction from industrial state in the kth civilisation,
    as the complement of extinction_given_industrial."""
    if k != k1:
        # We can't transition to different civilisations from a preperils state
        return 0
    return 1 - extinction_given_industrial(k)
