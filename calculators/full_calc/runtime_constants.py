# pylint: skip-file

# These constants determine runtime, which is something like
# O(MAX_CIVILISATIONS*MAX_PROGRESS_YEARS^2) or O(MAX_CIVILISATIONS*MAX_PLANETS^2) if the
# latter is bigger (although I have the impression that MAX_CIVILISATIONS has some
# exponentiation going on due to later civilisations requiring more precision in
# their float values). So setting them higher substantially increases runtime, but will also increase
# the fidelity of the final output (since the theoretical model assumes arbitrarily many).

# Some example runtimes on my 2019 Macbook Pro:
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 10, MAX_PROGRESS_YEARS = 4000, runtime = 997 seconds
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 10, MAX_PROGRESS_YEARS = 2000, runtime = 180 seconds
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 20, MAX_PROGRESS_YEARS = 1000, runtime = 98 seconds
# MAX_PLANETS = 20, MAX_CIVILISATIONS = 10, MAX_PROGRESS_YEARS = 2000, runtime = 196 seconds
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 20, MAX_PROGRESS_YEARS = 2000, runtime = 399 seconds


MAX_PLANETS = 20 # Gas giant moons and hollowed out asteroids might be self-sustainy
# enough at least en masse to get this number quite a lot higher than the number of nominal
# planets in the solar system.
MAX_CIVILISATIONS = 10
# For default parameters, higher values of the first two constants barely change
# the outcomes but substantially increase runtime.
MAX_PROGRESS_YEARS = 500 # The longer the stretches x_scales set in the params, the more this
# parameter seems likely to matter






# Min 2 to have a notion of progressing and 'regressing', but beware that with
# standard setup, we'll get an index out of bounds error if this is less than 71 (since we're
# treated as being in 70, 0-indexed)
if MAX_PROGRESS_YEARS < 2:
    raise 'Need at least 2 possible progress years'

MAX_PROGRESS_YEAR_REGRESSION_STEPS = 50
if MAX_PROGRESS_YEAR_REGRESSION_STEPS < 1:
    raise 'Need at least one possible regression'
