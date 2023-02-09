# These constants determine runtime, which is something like
# O(MAX_CIVILISATIONS*MAX_PROGRESS_YEARS^2) or O(MAX_CIVILISATIONS*MAX_PLANETS^2) if the
# latter is bigger. So setting them higher substantially increases runtime, but will also increase
# the accuracy of the final output.

MAX_PLANETS = 20
MAX_CIVILISATIONS = 30

MAX_PROGRESS_YEARS = 100
if MAX_PROGRESS_YEARS < 2:
  raise 'Need at least two possible progress years'

MAX_PROGRESS_YEAR_REGRESSION_STEPS = 50
if MAX_PROGRESS_YEAR_REGRESSION_STEPS < 1:
  raise 'Need at least one possible regression'
