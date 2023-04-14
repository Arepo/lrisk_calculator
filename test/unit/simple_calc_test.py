import pytest
import pdb
from calculators.simple_calc.simple_calc import SimpleCalc

def test_pre_equilibrium_probabilities_sum_to_1():
    form = {'extinction_given_pre_equilibrium': 0.3}
    calc = SimpleCalc(form)
    assert calc.preindustrial_given_pre_equilibrium() == 0.7
    assert calc.extinction_given_pre_equilibrium() + calc.preindustrial_given_pre_equilibrium() == 1

def test_preindustrial_probabilities_sum_to_1():
    form = {'extinction_given_preindustrial': 0.4}
    calc = SimpleCalc(form)
    assert calc.industrial_given_preindustrial() == 0.6
    assert calc.extinction_given_preindustrial() + calc.industrial_given_preindustrial() == 1

def test_industrial_probabilities_sum_to_1():
    form = {'extinction_given_industrial': 0.6}
    calc = SimpleCalc(form)
    assert calc.future_perils_given_industrial() == 0.4
    assert calc.extinction_given_industrial() + calc.future_perils_given_industrial() == 1

def test_present_perils_probabilities_sum_to_1():
    form = {'extinction_given_present_perils': 0.01, 'pre_equilibrium_given_present_perils': 0.1,
            'preindustrial_given_present_perils': 0.0001, 'industrial_given_present_perils': 0.2,
            'future_perils_given_present_perils': 0.02, 'multiplanetary_given_present_perils': 0.3}
    calc = SimpleCalc(form)
    assert calc.interstellar_given_present_perils() == 0.3698999999999999
    assert (calc.extinction_given_present_perils() + calc.pre_equilibrium_given_present_perils()
            + calc.preindustrial_given_present_perils() + calc.industrial_given_present_perils()
            + calc.future_perils_given_present_perils() + calc.multiplanetary_given_present_perils()
            + calc.interstellar_given_present_perils()) == 1

def test_future_perils_probabilities_sum_to_1():
    form = {'extinction_given_future_perils': 0.02, 'pre_equilibrium_given_future_perils': 0.2,
            'preindustrial_given_future_perils': 0.0003, 'industrial_given_future_perils': 0.1,
            'multiplanetary_given_future_perils': 0.2}
    calc = SimpleCalc(form)
    assert calc.interstellar_given_future_perils() == 0.4797
    assert (calc.extinction_given_future_perils() + calc.pre_equilibrium_given_future_perils()
            + calc.preindustrial_given_future_perils() + calc.industrial_given_future_perils()
            + calc.multiplanetary_given_future_perils() + calc.interstellar_given_future_perils()) == 1

def test_multiplanetary_probabilities_sum_to_1():
    form = {'extinction_given_multiplanetary': 0.2, 'pre_equilibrium_given_multiplanetary': 0.02,
            'preindustrial_given_multiplanetary': 0.003, 'industrial_given_multiplanetary': 0.3,
            'future_perils_given_multiplanetary': 0.1}
    calc = SimpleCalc(form)
    assert calc.interstellar_given_multiplanetary() == 0.377
    assert (calc.extinction_given_multiplanetary() + calc.pre_equilibrium_given_multiplanetary()
            + calc.preindustrial_given_multiplanetary() + calc.industrial_given_multiplanetary()
            + calc.future_perils_given_multiplanetary() + calc.interstellar_given_multiplanetary()) == 1

def test_assembles_valid_markov_chain():
    form = {'extinction_given_pre_equilibrium': 0.3, 'extinction_given_preindustrial': 0.4, 'extinction_given_industrial': 0.6, 'extinction_given_present_perils': 0.01, 'pre_equilibrium_given_present_perils': 0.1,
            'preindustrial_given_present_perils': 0.0001, 'industrial_given_present_perils': 0.2,
            'future_perils_given_present_perils': 0.02, 'multiplanetary_given_present_perils': 0.3, 'extinction_given_future_perils': 0.02, 'pre_equilibrium_given_future_perils': 0.2,
            'preindustrial_given_future_perils': 0.0003, 'industrial_given_future_perils': 0.1,
            'multiplanetary_given_future_perils': 0.2, 'extinction_given_multiplanetary': 0.2, 'pre_equilibrium_given_multiplanetary': 0.02,
            'preindustrial_given_multiplanetary': 0.003, 'industrial_given_multiplanetary': 0.3,
            'future_perils_given_multiplanetary': 0.1}
    calc = SimpleCalc(form)
    # Markov chain library will throw a descriptive error if anything's invalid
    calc.markov_chain()

