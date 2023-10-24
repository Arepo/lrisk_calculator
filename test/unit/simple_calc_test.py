# pylint: disable=missing-function-docstring, missing-module-docstring, unused-import, trailing-newlines

import pdb
from calculators.simple_calc.simple_calc import SimpleCalc

def test_preindustrial_probabilities_sum_to_1():
    probabilities = {'extinction_given_preindustrial': 0.4}
    calc = SimpleCalc(**probabilities)
    assert calc.industrial_given_preindustrial() == 0.6
    assert calc.extinction_given_preindustrial() + calc.industrial_given_preindustrial() == 1

def test_industrial_probabilities_sum_to_1():
    probabilities = {'extinction_given_industrial': 0.6}
    calc = SimpleCalc(**probabilities)
    assert calc.future_perils_given_industrial() == 0.4
    assert calc.extinction_given_industrial() + calc.future_perils_given_industrial() == 1

def test_present_perils_probabilities_sum_to_1():
    probabilities = {
        'extinction_given_present_perils': 0.01, 'preindustrial_given_present_perils': 0.0001,
        'industrial_given_present_perils': 0.2, 'future_perils_given_present_perils': 0.02,
        'interstellar_given_present_perils': 0.3}
    calc = SimpleCalc(**probabilities)
    assert calc.multiplanetary_given_present_perils() == 0.4699
    assert (calc.extinction_given_present_perils() + calc.preindustrial_given_present_perils()
            + calc.industrial_given_present_perils() + calc.future_perils_given_present_perils()
            + calc.multiplanetary_given_present_perils()
            + calc.interstellar_given_present_perils()) == 1

def test_future_perils_probabilities_sum_to_1():
    probabilities = {
        'extinction_given_future_perils': 0.02, 'preindustrial_given_future_perils': 0.0003,
        'industrial_given_future_perils': 0.1, 'interstellar_given_future_perils': 0.2}
    calc = SimpleCalc(**probabilities)
    assert calc.multiplanetary_given_future_perils() == 0.6797
    assert (calc.extinction_given_future_perils() + calc.preindustrial_given_future_perils()
            + calc.industrial_given_future_perils() + calc.multiplanetary_given_future_perils()
            + calc.interstellar_given_future_perils()) == 1

def test_multiplanetary_probabilities_sum_to_1():
    probabilities = {
        'extinction_given_multiplanetary': 0.2, 'preindustrial_given_multiplanetary': 0.003,
        'industrial_given_multiplanetary': 0.3, 'future_perils_given_multiplanetary': 0.1}
    calc = SimpleCalc(**probabilities)
    assert calc.interstellar_given_multiplanetary() == 0.397
    assert (calc.extinction_given_multiplanetary() + calc.preindustrial_given_multiplanetary()
            + calc.industrial_given_multiplanetary() + calc.future_perils_given_multiplanetary()
            + calc.interstellar_given_multiplanetary()) == 1

def test_assembles_valid_markov_chain():
    probabilities = {'extinction_given_preindustrial': 0.4, 'extinction_given_industrial': 0.6,
            'extinction_given_present_perils': 0.01, 'preindustrial_given_present_perils': 0.0001,
            'industrial_given_present_perils': 0.2, 'future_perils_given_present_perils': 0.02,
            'interstellar_given_present_perils': 0.3, 'extinction_given_future_perils': 0.02,
            'preindustrial_given_future_perils': 0.0003, 'industrial_given_future_perils': 0.1,
            'interstellar_given_future_perils': 0.2, 'extinction_given_multiplanetary': 0.2,
            'preindustrial_given_multiplanetary': 0.003, 'industrial_given_multiplanetary': 0.3,
            'future_perils_given_multiplanetary': 0.1}
    calc = SimpleCalc(**probabilities)
    # The Markov chain library will throw a descriptive error here if anything's invalid
    calc.markov_chain()
