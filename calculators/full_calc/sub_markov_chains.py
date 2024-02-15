# pylint: disable=fixme

"""Implements the two classes used to represent times of perils and multiplanetary states
respectively in the decay/perils-focused models described here:
https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/YnBwoNNqe6knBJH8p#The_decay_model
"""

from pydtmc import MarkovChain

import calculators.full_calc.runtime_constants as constant
from calculators.full_calc import multiplanetary
from calculators.full_calc import perils
from calculators.full_calc.params import Params

# See https://dbader.org/blog/python-memoization for a primer on caching
# TODO look into https://github.com/pymc-devs/pymc
# https://github.com/riccardoscalco/Pykov
# and https://martin-thoma.com/python-markov-chain-packages/

class IntraPerilsMCWrapper():
    """Wrapper for a Markov chain representing the transition probabilities between different
    progress years in a given time of perils, between that time of perils and the other
    civilisational states"""
    def __init__(self, k):
        print(f"Initialising IntraPerilsMCWrapper for k = {k}")
        self.k = k

        # Transitional probabilities from non-absorbing states
        year_range = range(0, constant.MAX_PROGRESS_YEARS)

        intra_transition_probabilities = {
            p: [perils.transition_to_year_n_given_perils(k, p, n) for n in year_range]
            for p in year_range}

        exit_probabilities = {p:[perils.extinction_given_perils(k, p),
                                 perils.preindustrial_given_perils(k, p),
                                 perils.industrial_given_perils(k, p),
                                 perils.multiplanetary_given_perils(k, p),
                                 perils.interstellar_given_perils(k, p)] for p in year_range}

        year_p_rows = [intra_transition_probabilities[p] + exit_probabilities[p]
                       for p in year_range]

        # Transitional probabilities from absorbing states (ie rows of 0s, with one 1)
        extinction_row =        [0] * constant.MAX_PROGRESS_YEARS + [1,0,0,0,0]
        preindustrial_row =     [0] * constant.MAX_PROGRESS_YEARS + [0,1,0,0,0]
        industrial_row =        [0] * constant.MAX_PROGRESS_YEARS + [0,0,1,0,0]
        multiplanetary_row =    [0] * constant.MAX_PROGRESS_YEARS + [0,0,0,1,0]
        interstellar_row =      [0] * constant.MAX_PROGRESS_YEARS + [0,0,0,0,1]

        probability_matrix = year_p_rows + [extinction_row,
                                            preindustrial_row,
                                            industrial_row,
                                            multiplanetary_row,
                                            interstellar_row]

        perils_years = [f"{num}" for num in year_range]


        self.mc = MarkovChain(probability_matrix, perils_years
                                            + ['Extinction',
                                                'Preindustrial',
                                                'Industrial',
                                                'Multiplanetary',
                                                'Interstellar'])

        self.starting_year = Params().dictionary['perils']['current_progress_year']
        # TODO: make it easier to investigate different values for this param
        # self.starting_year = 0 # For testing

    def extinction_given_perils(self):
        """Return the overall transitional probability of extinction for the kth civilisation, given
        that it's in a time of perils"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
            # When we hit the last civilisation, anything that would regress us just means we go
            # extinct

            # Min() function corrects a pydtmc floating point error that can make this above 1
            return min(self.mc.absorption_probabilities()[1][0] # preindustrial
                        + self.mc.absorption_probabilities()[2][0] # industrial
                        + self.mc.absorption_probabilities()[0][0] # extinction
                        , 1)
        if self.k == 0:
            return self.mc.absorption_probabilities()[0][self.starting_year]
            # Assume we start from where we actually are in the current time of perils, but in
            # future ones we start from year 0
        return min(self.mc.absorption_probabilities()[0][0], 1)

    def preindustrial_given_perils(self, k1):
        """Return the overall probability of transitioning to a preindustrial state for the kth
        civilisation, given that it's in a time of perils"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
            return 0
        if self.k == 0 and k1 == 1:
            return self.mc.absorption_probabilities()[1][self.starting_year]
        if self.k + 1 == k1:
            return self.mc.absorption_probabilities()[1][0]
        # The only preindustrial state we can reach from perils_k is preindustrial_(k+1)
        return 0

    def industrial_given_perils(self, k1):
        """Return the overall probability of transitioning to an industrial state for the kth
        civilisation, given that it's in a time of perils"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
            return 0
        if self.k == 0 and k1 == 1:
            return self.mc.absorption_probabilities()[2][self.starting_year]
        if self.k + 1 == k1:
            return self.mc.absorption_probabilities()[2][0]
        # The only industrial state we can reach from perils_k is industrial_(k+1)
        return 0

    def multiplanetary_given_perils(self, k1):
        """Return the overall probability of transitioning to a multiplanetary state for the kth
        civilisation, given that it's in a time of perils"""
        if self.k == 0 and k1 == 0:
            return self.mc.absorption_probabilities()[3][self.starting_year]
        if self.k == k1:
            return self.mc.absorption_probabilities()[3][0]
        # The only multiplanetary state we can reach from perils_k is multiplanetary_k
        return 0

    def interstellar_given_perils(self):
        """Return the overall probability of transitioning to an interstellar state for the kth
        civilisation, given that it's in a time of perils"""
        # This approach gives a smaller floating point error than treating pydtmc's absorption
        # probabilities as summing to 1

        # Max() function corrects a pydtmc floating point error that can make this <0
        return max( 1 - (self.extinction_given_perils()
                    + self.preindustrial_given_perils(self.k + 1)
                    + self.industrial_given_perils(self.k + 1)
                    + self.multiplanetary_given_perils(self.k)), 0)

class IntraMultiplanetaryMCWrapper():
    """Wrapper for a Markov chain representing the transition probabilities given different numbers
    of independent self-sustaining settlements in a multiplanetary state, between that time of
    perils and the other civilisational states"""
    def __init__(self, k):
        self.k = k
        print(f"Initialising IntraMultiplanetaryMCWrapper for k = {k}")

        extinction_row =     [0] * (constant.MAX_PLANETS - 1) + [1,0,0,0,0]
        preindustrial_row =  [0] * (constant.MAX_PLANETS - 1) + [0,1,0,0,0]
        industrial_row =     [0] * (constant.MAX_PLANETS - 1) + [0,0,1,0,0]
        perils_row =         [0] * (constant.MAX_PLANETS - 1) + [0,0,0,1,0]
        interstellar_row =   [0] * (constant.MAX_PLANETS - 1) + [0,0,0,0,1]
        planet_range = range(2, constant.MAX_PLANETS + 1) # Python range excludes max value

        intra_transition_probabilities = {
            q: [multiplanetary.transition_to_n_planets_given_multiplanetary(q, n)
               for n in planet_range]
            for q in planet_range}
        exit_probabilities = {
            q: [multiplanetary.extinction_given_multiplanetary(q),
                multiplanetary.preindustrial_given_multiplanetary(),
                multiplanetary.industrial_given_multiplanetary(),
                multiplanetary.perils_given_multiplanetary(q),
                multiplanetary.interstellar_given_multiplanetary(q)]
            for q in planet_range}

        qth_planet_rows = [intra_transition_probabilities[q] + exit_probabilities[q]
                           for q in planet_range]

        # qth_planet_list = {q:qth_planet_rows[q - 2] for q in planet_range}
        # Useful for figuring out the row corresponding to q planets, not used in code

        probability_matrix = qth_planet_rows + [extinction_row,
                                                preindustrial_row,
                                                industrial_row,
                                                perils_row,
                                                interstellar_row]

        planet_counts = [f"{num}" for num in planet_range]
        self.mc = MarkovChain(probability_matrix, planet_counts
                                                + ['Extinction',
                                                    'Preindustrial',
                                                    'Industrial',
                                                    'Perils',
                                                    'Interstellar'])


    def extinction_given_multiplanetary(self):
        """Return the overall transitional probability of extinction for the kth civilisation, given
        that it's in a multiplanetary state"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
            # When we hit the last civilisation, anything that would regress us means we just go
            # extinct
            return (self.mc.absorption_probabilities()[0][0]
                    + self.mc.absorption_probabilities()[1][0]
                    + self.mc.absorption_probabilities()[2][0]
                    + self.mc.absorption_probabilities()[3][0])
        return self.mc.absorption_probabilities()[0][0]

    def preindustrial_given_multiplanetary(self, k1):
        """Return the overall transitional probability to a preindustrial state for the kth
        civilisation, given that it's in a multiplanetary state"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
        # When we hit the last civilisation, anything that would regress us means we just go extinct
            return 0
        if self.k + 1 == k1:
            return self.mc.absorption_probabilities()[1][0]
        return 0

    def industrial_given_multiplanetary(self, k1):
        """Return the overall transitional probability to an industrial state for the kth
        civilisation, given that it's in a multiplanetary state"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
        # When we hit the last civilisation, anything that would regress us means we just go extinct
            return 0
        if self.k + 1 == k1:
            return self.mc.absorption_probabilities()[2][0]
        return 0

    def perils_given_multiplanetary(self, k1):
        """Return the overall transitional probability to a time of perils state for the kth
        civilisation, given that it's in a multiplanetary state"""
        if self.k + 1 >= constant.MAX_CIVILISATIONS:
        # When we hit the last civilisation, anything that would regress us means we just go extinct
            return 0
        if self.k + 1 == k1:
            return self.mc.absorption_probabilities()[3][0]
        return 0

    def interstellar_given_multiplanetary(self):
        """Return the overall transitional probability to an interstellar state for the kth
        civilisation, given that it's in a multiplanetary state"""
        return self.mc.absorption_probabilities()[4][0]
