MAX_PLANETS = 20
MAX_PROGRESS_YEARS = 100
MAX_CIVILISATIONS = 5
MAX_PROGRESS_YEAR_REGRESSION_STEPS = 50

if MAX_PROGRESS_YEARS < 2:
  raise 'Need at least two possible progress years'
if MAX_PROGRESS_YEAR_REGRESSION_STEPS < 1:
  raise 'Need at least one possible regression'
