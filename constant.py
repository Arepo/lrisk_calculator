MIN_PERILS_RISK = 8 # Set this to whatever the lowest x_translation value in the perils model is.
# This is the difference between the time of perils 'starting' in 1945, and the actual (with some
# hindsight) year in which at least one of the exit risks rises above 0: it lets us save some
# computational time on dealing with years with no probability of exit

MAX_PLANETS = 20
MAX_CIVILISATIONS = 5

MAX_PROGRESS_YEARS = 100
if MAX_PROGRESS_YEARS < 2:
  raise 'Need at least two possible progress years'

MAX_PROGRESS_YEAR_REGRESSION_STEPS = 50
if MAX_PROGRESS_YEAR_REGRESSION_STEPS < 1:
  raise 'Need at least one possible regression'
