# pylint: disable=fixme, too-many-instance-attributes, too-many-arguments, too-many-locals
# pylint: disable=too-many-public-methods

"""Implementation of the simple calculator."""

from collections import OrderedDict
from pydtmc import MarkovChain
import numpy as np

# This script prints out a series of probabilities for transition becoming interstellar based on
# estimates of the transition probabilities of various(values are currently hardcoded placeholders)
# states, as in a Markov chain. The states are extinction, preindustrial, industrial, the current
# time of perils, any future times of perils, multiplanetary, and interstellar.
#
# A full description/explanation of the model is in the section titled The Cyclical Model in this
# post:
# https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-after-a-catastrophe#The_cyclical_model
#
# These values are all placeholders. Add your own, and see what happens.

# TODO Nia's comments: https://github.com/niajane/lrisk_calc_comments/pull/1/files

# Transition probabilities

def rounded(func):
    "Round the probabilities to be between 0 and 1 in case of floating point errors"
    def inner(val):
        val = func(val)
        if val < 0:
            return 0
        if val > 1:
            return 1
        return val
    return inner

class SimpleCalc:
    """Wrapper for the pydtmc MarkovChain class that calculates the probability of becoming
    interstellar given user-specified credences"""
    def __init__(self, extinction_given_preindustrial=0, extinction_given_industrial=0,
                extinction_given_present_perils=0, preindustrial_given_present_perils=0,
                industrial_given_present_perils=0, future_perils_given_present_perils=0,
                interstellar_given_present_perils=0, extinction_given_future_perils=0,
                preindustrial_given_future_perils=0, industrial_given_future_perils=0,
                interstellar_given_future_perils=0, extinction_given_multiplanetary=0,
                preindustrial_given_multiplanetary=0, industrial_given_multiplanetary=0,
                future_perils_given_multiplanetary=0):

        # Premodern transition probabilities
        self.ext_g_pi = extinction_given_preindustrial
        self.ext_g_i = extinction_given_industrial

        # Present perils transition probabilities
        self.ext_g_pp = extinction_given_present_perils
        self.pi_g_pp = preindustrial_given_present_perils
        self.i_g_pp = industrial_given_present_perils
        self.fp_g_pp = future_perils_given_present_perils
        self.int_g_pp = interstellar_given_present_perils

        # Future perils transition probabilities
        self.ext_g_fp = extinction_given_future_perils
        self.pi_g_fp = preindustrial_given_future_perils
        self.i_g_fp = industrial_given_future_perils
        self.int_g_fp = interstellar_given_future_perils

        # Multiplanetary transition probabilities
        self.ext_g_mp = extinction_given_multiplanetary
        self.pi_g_mp = preindustrial_given_multiplanetary
        self.i_g_mp = industrial_given_multiplanetary
        self.fp_g_mp = future_perils_given_multiplanetary

        self.mc = None

    # From preindustrial
    @rounded
    def extinction_given_preindustrial(self):
        """Return the rounded user-specified probability. The complement of the
        probability of becoming industrial from this state"""
        return self.ext_g_pi

    @rounded
    def industrial_given_preindustrial(self):
        "Return the calculated probability based on extinction_given_preindustrial"
        return 1 - self.extinction_given_preindustrial()


    # From industrial
    @rounded
    def extinction_given_industrial(self):
        """Return the rounded user-specified probability. The complement of the
        probability of reaching a future time of perils from this state"""
        return self.ext_g_i

    @rounded
    def future_perils_given_industrial(self):
        "Return the calculated probability based on extinction_given_industrial"
        return 1 - self.extinction_given_industrial()


    # From present perils
    @rounded
    def extinction_given_present_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.ext_g_pp

    @rounded
    def preindustrial_given_present_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.pi_g_pp

    @rounded
    def industrial_given_present_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.i_g_pp

    @rounded
    def future_perils_given_present_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.fp_g_pp

    @rounded
    def interstellar_given_present_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.int_g_pp

    @rounded
    def multiplanetary_given_present_perils(self):
        """Return the calculated probability based on the other transitional
        probabilities from the present"""
        return 1 - (self.extinction_given_present_perils()
                    + self.preindustrial_given_present_perils()
                    + self.industrial_given_present_perils()
                    + self.future_perils_given_present_perils()
                    + self.interstellar_given_present_perils())


    # From future perils
    @rounded
    def extinction_given_future_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.ext_g_fp

    @rounded
    def preindustrial_given_future_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.pi_g_fp

    @rounded
    def industrial_given_future_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.i_g_fp

    @rounded
    def interstellar_given_future_perils(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming a multiplanetary civilisation from this state"""
        return self.int_g_fp

    @rounded
    def multiplanetary_given_future_perils(self):
        """Return the calculated probability based on the other transitional
        probabilities from a future time of perils"""
        return 1 - (self.extinction_given_future_perils()
                    + self.preindustrial_given_future_perils()
                    + self.industrial_given_future_perils()
                    + self.interstellar_given_future_perils())

    # From mutiplanetary
    @rounded
    def extinction_given_multiplanetary(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming an interstellar civilisation from this state"""
        return self.ext_g_mp

    @rounded
    def preindustrial_given_multiplanetary(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming an interstellar civilisation from this state"""
        return self.pi_g_mp

    @rounded
    def industrial_given_multiplanetary(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming an interstellar civilisation from this state"""
        return self.i_g_mp

    @rounded
    def future_perils_given_multiplanetary(self):
        """Return the rounded user-specified probability. Co-determines the
        probability of becoming an interstellar civilisation from this state"""
        return self.fp_g_mp

    @rounded
    def interstellar_given_multiplanetary(self):
        """Return the calculated probability based on the other transitional
        probabilities from a multiplanetary state"""
        return 1 - (self.extinction_given_multiplanetary()
                    + self.preindustrial_given_multiplanetary()
                    + self.industrial_given_multiplanetary()
                    + self.future_perils_given_multiplanetary())

    def markov_chain(self):
        """Generate or returned cached pydtmc MarkovChain object based on the user-specified
        transitional probabilities according to the cyclical model of civilisation described
        here: https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/YnBwoNNqe6knBJH8p"""
        if self.mc:
            return self.mc
        extinction_transition_probabilities =     [1, 0, 0, 0, 0, 0, 0]
        preindustrial_transition_probabilities =  [self.extinction_given_preindustrial(),
                                                   0,
                                                   self.industrial_given_preindustrial(),
                                                   0,
                                                   0,
                                                   0,
                                                   0]
        industrial_transition_probabilities =   [self.extinction_given_industrial(),
                                               0,
                                               0,
                                               0,
                                               self.future_perils_given_industrial(),
                                               0,
                                               0]
        present_perils_transition_probabilities = [self.extinction_given_present_perils(),
                                                   self.preindustrial_given_present_perils(),
                                                   self.industrial_given_present_perils(),
                                                   0,
                                                   self.future_perils_given_present_perils(),
                                                   self.multiplanetary_given_present_perils(),
                                                   self.interstellar_given_present_perils()]
        future_perils_transition_probabilities =   [self.extinction_given_future_perils(),
                                                    self.preindustrial_given_future_perils(),
                                                    self.industrial_given_future_perils(),
                                                    0,
                                                    0,
                                                    self.multiplanetary_given_future_perils(),
                                                    self.interstellar_given_future_perils()]
        multiplanetary_transition_probabilities = [self.extinction_given_multiplanetary(),
                                                   self.preindustrial_given_multiplanetary(),
                                                   self.industrial_given_multiplanetary(),
                                                   0,
                                                   self.future_perils_given_multiplanetary(),
                                                   0,
                                                   self.interstellar_given_multiplanetary()]
        interstellar_transition_probabilities =   [0, 0, 0, 0, 0, 0, 1]

        transition_probability_matrix = [extinction_transition_probabilities,
                                         preindustrial_transition_probabilities,
                                         industrial_transition_probabilities,
                                         present_perils_transition_probabilities,
                                         future_perils_transition_probabilities,
                                         multiplanetary_transition_probabilities,
                                         interstellar_transition_probabilities]

        self.mc = MarkovChain(transition_probability_matrix, ['Extinction',
                                                             'Preindustrial',
                                                             'Industrial',
                                                             'Present perils',
                                                             'Future perils',
                                                             'Multiplanetary',
                                                             'Interstellar'])
        return self.mc

    # Convenience methods for the probability of direct-path transitions

    def probability_of_preindustrial_to_perils_directly(self):
        "Probability of reaching a future time of perils at least once from a preindustrial state"
        return self.industrial_given_preindustrial() * self.future_perils_given_industrial()

    def net_interstellar_from_preindustrial(self):
        "Probability of eventually (by any path) becoming interstellar from a preindustrial state"
        return self.markov_chain().absorption_probabilities()[1][0]

    def net_interstellar_from_industrial(self):
        "Probability of eventually (by any path) becoming interstellar from an industrial state"
        return self.markov_chain().absorption_probabilities()[1][1]

    def net_interstellar_from_present_perils(self):
        "Probability of eventually (by any path) becoming interstellar from our current state"
        return self.markov_chain().absorption_probabilities()[1][2]

    def net_interstellar_from_future_perils(self):
        "Probability of eventually (by any path) becoming interstellar from a future time of perils"
        return self.markov_chain().absorption_probabilities()[1][3]

    def net_interstellar_from_multiplanetary(self):
        "Probability of eventually (by any path) becoming interstellar from a multiplanetary state"
        return self.markov_chain().absorption_probabilities()[1][4]

    # Convenience methods for describing the signed proportionate change in expected value from
    # transitioning to other states than our current one relative to some astronomical value V

    def extinction_probability_difference(self):
        "The absolute loss in expected value from going extinct"
        return -self.net_interstellar_from_present_perils()

    def preindustrial_probability_difference(self):
        "The absolute change in expected value from regressing to a preindustrial state"
        return (self.net_interstellar_from_preindustrial()
                - self.net_interstellar_from_present_perils())

    def industrial_probability_difference(self):
        "The absolute change in expected value from regressing to an industrial state"
        return self.net_interstellar_from_industrial() - self.net_interstellar_from_present_perils()

    def future_perils_probability_difference(self):
        "The absolute change in expected value from transitioning to an industrial state"
        return (self.net_interstellar_from_future_perils()
                - self.net_interstellar_from_present_perils())

    def multiplanetary_probability_difference(self):
        "The absolute change in expected value from transitioning to a multiplanetary state"
        return (self.net_interstellar_from_multiplanetary()
                - self.net_interstellar_from_present_perils())

    def interstellar_probability_difference(self):
        "The absolute change in expected value from transitioning to an interstellar state"
        return 1 - self.net_interstellar_from_present_perils()

    def probability_differences(self):
        """An ordered dictionary of the absolute changes in expected value from transitioning
        to each other state in the cyclical model"""
        return OrderedDict([
        ('Extinction', self.extinction_probability_difference()),
        ('Preindustrial', self.preindustrial_probability_difference()),
        ('Industrial', self.industrial_probability_difference()),
        ('Future perils', self.future_perils_probability_difference()),
        ('Multiplanetary', self.multiplanetary_probability_difference()),
        ('Interstellar', self.interstellar_probability_difference())
        ])

    def extinction_probability_proportion(self):
        "The loss in expected value from going extinct as a proportion of current expected value"
        return '100%'

    def preindustrial_probability_proportion(self):
        """The change in expected value from transitioning to a preindustrial state as a signed
        proportion of current expected value"""
        return str((self.net_interstellar_from_present_perils()
                    - self.net_interstellar_from_preindustrial())
                    / self.net_interstellar_from_present_perils() * 100) + '%'

    def industrial_probability_proportion(self):
        """The change in expected value from transitioning to an industrial state as a signed
        proportion of current expected value"""
        return str((self.net_interstellar_from_present_perils()
                    - self.net_interstellar_from_industrial())
                / self.net_interstellar_from_present_perils() * 100) + '%'

    def future_perils_probability_proportion(self):
        """The change in expected value from transitioning to a future time of perils state as a
        signed proportion of current expected value"""
        return str((self.net_interstellar_from_present_perils()
                    - self.net_interstellar_from_future_perils())
                    / self.net_interstellar_from_present_perils() * 100) + '%'

    def multiplanetary_probability_proportion(self):
        """The change in expected value from transitioning to a future time of perils state as a
        signed proportion of current expected value"""
        return str((self.net_interstellar_from_present_perils()
                    - self.net_interstellar_from_multiplanetary())
                    / self.net_interstellar_from_present_perils() * 100) + '%'

    def interstellar_probability_proportion(self):
        """The change in expected value from transitioning to an interstellar state as a
        signed proportion of current expected value"""
        return str((self.net_interstellar_from_present_perils() - 1)
                    / self.net_interstellar_from_present_perils() * 100) + '%'

    def probability_proportion_differences(self):
        """An ordered dictionary of the signed proportional changes in expected value from
        transitioning to each other state in the cyclical model"""
        if self.net_interstellar_from_present_perils():
            return OrderedDict([
                ('Extinction', self.extinction_probability_proportion()),
                ('Preindustrial', self.preindustrial_probability_proportion()),
                ('Industrial', self.industrial_probability_proportion()),
                ('Future perils', self.future_perils_probability_proportion()),
                ('Multiplanetary', self.multiplanetary_probability_proportion()),
                ('Interstellar', self.interstellar_probability_proportion())
            ])
        return OrderedDict([
            ('Extinction', np.nan),
            ('Preindustrial', np.nan),
            ('Industrial', np.nan),
            ('Future perils', np.nan),
            ('Multiplanetary', np.nan),
            ('Interstellar', np.nan)
        ])
