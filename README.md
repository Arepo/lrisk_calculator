# L-risk calculator

This repo contains a functional but unfinished implementation of the models of human civilisation development described [here](https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-beyond-a-catastrophe) (with the 'survival' state renamed less confusingly as 'pre-equilibrium'). That post is highly recommended reading if you want to use these tools, since otherwise the inputs required for each model might be opaque.

The cyclical model and perils-focused models from that post correspond respectively to the 'simple calculator' and 'full calculator' in this repo (except that I've added an 8th state, 'future time of perils', to the cyclical one, since it seemed potentially important to distinguish between the risk of starting risk estimation from the very beginning of one and starting it from where we are now). I've called them L(ongtermist)-risk calculators because get at what I think are the core intuitions behind the concept of X(istential) risk, which as a concept has various problems described [here](https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/fi3Abht55xHGQ4Pha).

To run the simple calc, navigate to ./calculators/website, and from the command line enter
`flask --app webapp run` - then visit http://127.0.0.1:5000/, submit your best guesses, and you'll see the results at the top of the form.

To run the full calc, first set the values in runtime_constants.py: higher values of MAX_PLANETS, MAX_CIVILISATIONS, MAX_PROGRESS_YEARS give more 'accurate' representation of the model, but rapidly increase runtime, which I think is O(MAX_CIVILISATIONS * MAX_PROGRESS_YEARS^2). On my 2019 Macbook Pro, the runtime was 153 seconds with the values set to the following…
MAX_PLANETS = 20
MAX_CIVILISATIONS = 30
MAX_PROGRESS_YEARS = 1000
MAX_PROGRESS_YEAR_REGRESSION_STEPS = 50

Then set the the nominal parameters of the model in params.yml. You might also choose to edit the functions that use those parameters to determine transitional probabilities - the functions I've used describe as simply as I could a fairly customisable S-curving development of various relevant technology-driven transitional probabilities. See [this Google doc](https://docs.google.com/document/d/13EOMnSSHIco50dKTba6gK8mVzitNpDSD2dbrH_gzdds/edit#) for a more in-depth discussion of the functions I've used and what their parameters represent.

Once you're satisfied with the parameters, navigate to navigate to ./calculators/full_calc, and run `python3 full_calc.py`. Note that with default runtime constants, it will take about 30 seconds to run. The result is a breakpoint in the code that gives you access to a MarkovChain object that you can interrogate (see printed instructions). The API of the MarkovChain library is described [here](https://github.com/TommasoBelluzzo/PyDTMC). Note that its readme isn't comprehensive. Some useful clarifications:
* the MarkovChain object has a `.states` property, which I find useful to confirm ordering in the full transition matrix
* the `mc.absorption_probabilities()` function produces an array of arrays with one top-level array for each absorbing state (in our case, two), in the order they were passed to the constructor (in our case, Extinction first, then Interstellar). The subarray elements correspond to the probability of hitting that absborbing state from each non-absorbing state, again in the order the were passed to the constructor (in our case, the prequilibrium states for each possible future civilisation up to <the max number of future civilisations - 1>, then the preindustrial ones, etc)

# Storing results for discussion

When you run the full calculator, it it will store he parameters you've chosen and the results they imply in results.csv.

If you do so, please consider committing the changes to the CSV file and submitting it as a pull request, so we can compare how people's intuitions differ. Feel free to add a name/brief description to the run if there's any salient parameters you want to highlight, and any notes you have to the second column.

# Philosophy of the calculator
## Expect increasing difficulty of developing technology

A core assumption behind this model is that we should expect each civilisation to use the most accessible resources, and thus that - with the partial exception of reboot 1, which will for the first time have leftover technology from the previous civilisation to learn from - each civilisation will tend to have less accessible resources and so slower technological growth than the last. The overall pattern is

* A high level of technology is required to become interstellar
* Reaching that level requires some amount of time at high risk of causing a collapse of civilisation, or of entirely destroying ourselves (a ‘time of perils’)
* Each collapse gives us a chance of going extinct from natural background risk before we reboot the next technological civilisation, and this chance might increase per reboot
* Each reboot increases the amount of time we spend in the subsequent time of perils
* Therefore the risk of reboot should be considered in the same category as an extinction risk - a [longtermist risk](https://forum.effectivealtruism.org/posts/zuQeTaqrjveSiSMYo/a-proposed-hierarchy-of-longtermist-concepts), if you will (hence the Github repo name); more specifically a contraction risk

The size of this risk could be negligible or enormous, depending on the values one assumes for the various relevant parameters.

It’s possible that inside-view considerations could outweigh this effect for near-term reboots – for example, post-apocalyptic civilisations being more cautious about creating or using advanced weaponry. One could straightforwardly add these to the calculator as an if statement, but by default, it treats each reboot with the same underlying logic.

## Use year-based states to represent a time of perils

This is really part of the underlying model, and I discussed it somewhat in the [EA forum post](https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-beyond-a-catastrophe), but it’s complicated enough that I think it’s worth discussing further, and explaining why I picked it over a simpler implementation of (for example) a small number of states representing availability of specific technologies.

We divide a time of perils into 'progress years'. A progress year is defined as a level of technology that a) gives the probability of transitioning to each other civilisational state during a year spent at that level of technology, b) is equivalent to some number of actual years of uninterrupted technological development at some abstract base rate of progress, given no global setbacks, we imagine it would take to reach that level of technology given the availability of resources (ie taking into account how many previous civilisations have existed). For example, progress-year 200 for civilisation 3 represents the level of technology the third civilisation would have been able to reach after 200 years of relatively peaceful progress; it might be reached either by 200 such happy years, or, for example, by 300 such years and then a calamity that wiped out 100 years of technological development.

This approach has a few benefits:
1) data about our current era heavily tends towards annualisation. For example: we have annual estimates of GDP, both at the global and country level; we have annual [estimates of background extinction risk](https://www.nature.com/articles/s41598-019-47540-7) (which could become relevant given elongation of future perils states, per previous section); also the most granular existential risk estimates we have are per year (see Michael Aird’s [existential risk database](https://docs.google.com/spreadsheets/d/1W10B6NJjicD8O0STPiT3tNV3oFnT8YsfjmtYR8RO_RI/)).

So the progress year approach makes it easy to use such data to inform our credences. Similarly, other risk estimates from that database are point estimates about the probability of some outcome by some year. Such point estimates don’t plug in quite so neatly, since we can’t straightforwardly equate <the number of actual years until the given date> with <its distance in progress years> - but doing so maybe isn’t a bad first approximation (and we can calculate a more precise way of interpreting the estimate if we think it’s important).


2) it lets us consider scenarios in which a 'minor' catastrophe sets us back, say, 50 years - a blip which would usually be literally invisible in existential risk discussions, but which, on this approach, we can now think of as a small but conceivably significant longtermist risk.


3) it’s agnostic about how we determine our base rate of technological progress. I chose the default parameters in the full calculator by eyeballing historical GDP, and putting us in about the ~70th progress year from 1945 (rather than the 78th, where we would have been in 2023 with GDP growth every year). But if, for example, you thought that the end of the space race was contingent and that in [a different world](https://www.imdb.com/title/tt7772588/) it could have progressed much further, you might consider us to be in a much less advanced progress year today (probably leading to a more optimistic set of predictions for future times of peril).

4) It gives us some scope to parameterise differential technological progress, such as by changing the relative x-stretch for certain transitional probabilities, as described in the next section.

## Use an S-curve function to represent increasing probabilities of [technological expansion/contraction](https://forum.effectivealtruism.org/posts/zuQeTaqrjveSiSMYo/a-proposed-hierarchy-of-longtermist-concepts)

To capture my intuitions about risks from various technologies rising over time, I wanted a function that ‘looked S-curved’ but had a distinct starting point. Somewhat arbitrarily, I’ve used one with the form y = 1/(1 + x^-A * e^-x)[^xkrempel] (you can play with an implementation of this graph [here](https://www.desmos.com/calculator/9u4pho91yo)), such that
* x is the progress year (and must be >= 0)
* y is the annual probability for any value of x of transitioning to the specified state given that level of technology
* _e_ is the [constant e](https://en.wikipedia.org/wiki/E_(mathematical_constant))
* A is a somewhat nebulous 'sharpness' parameter, which determines the steepness of the centre of the S-curve (must be > 0; values between 0 and 1 remove the slow takeoff of the S). This parameter might end up being irrelevant - I normally leave it at 2 by default - but it gives the curve a natural 0 point, and allows more flexibility to otherwise tweak the shape of the curve to (for example) fit historical data

Then, to give more us more control over this curve, I added parameters that stretch and translate it, to allow us to express and generalise opinions like
* ‘from an outside view, the average annual probability per year of us going extinct* won’t be more than B’
* ‘it would take C[^xasymptote] years for the world to max out on stockpiles of all the technologies we can currently foresee that could make us extinct†’
* ‘each time civilisation has to reboot, it will take us D times longer to develop some or all technologies that could make us extinct*’ (with the possible exception noted above of the first reboot)
* ‘there was (now that we know nuclear weaponry wouldn’t [ignite the atmosphere](https://www.realclearscience.com/blog/2019/09/12/the_fear_that_a_nuclear_bomb_could_ignite_the_atmosphere.html)) 0 chance of us making ourselves extinct† until E years after the start of the time of perils’

† Or transitioning to a state of pre-equilibrium/preindustrial/industrial/multiplanetary/interstellar

Adding these considerations to the initial form gets us the inelegant (but still S-shaped) function [B / (1 + 1 / (CD^k) * (x - E)^-A * e^ -(1 / (CD^k) * (x - E)))](https://www.desmos.com/calculator/mpqprh9iyq), such that
* k is the number of times civilisation has ‘rebooted’ - that is, has regressed to a lower technology state from a time of perils or multiplanetary state (meaning we are currently in k=0)
* B is a stretch along the y-axis
* C[^xasymptote] is a stretch along the x-axis
* D is a multiplier on C that we apply once per civilisational reboot (so after k reboots, the stretch would be CDk).
* E is a translation along the x-axis

In effect, D makes the trajectory of our current or second time of perils a blueprint for all future ones.

One could also investigate the implications of differential technological progress in our current time of perils by (say) running the calculator with values that decrease the steepness of some particular S-curve only when k=0 (there’s no native support for this, but it could be added easily if desired).

# Use an exponential decay function to represent risks decreasing as we settle multiple planets

In general, I expect self-sustaining settlements to provide resilience to virtually all catastrophes that wouldn’t immediately send humanity extinct, and to most catastrophes that would. Naively, for example, if the probability of nuclear war destroying civilisation on a single planet were 1/2, and there were no then the probability of it happening on three planets would be (1/2)^3 or 1/8. AI is the main exception, but would need an extension to the model (described under limitations below) to treat it properly; for now I don’t distinguish it from the other threats.

To capture my intuitions about this class of states, the probabilities of transitions to lower technology states derive from an exponential decay formula, with equation [y = A(1 - r)^(x - C) + D](https://www.desmos.com/calculator/dhembkybvt), such that
* x is the number of self-sustaining settlements,
* y is the probability for any value of x of transitioning to the specified state from that number of planets
* A is a stretch parallel to the y-axis, representing the starting probability† of the transition (for x=2, since 2 planets is the minimum to definitionally qualify as being in a multiplanetary state)
* r is a value between 0 and 1 representing the the steepness of the decay (so the transition probability is multiplied by (1-r) for each additional planet)†
* C is a translation parallel to the x-axis, always set to 2 by default (again because that’s the definitional starting point of the multiplanetary state)
D is a translation in the y-direction representing the minimum value the risk can reduce to†

† though D is applied after A and r, so will modify those values accordingly

In this class of states we don’t pay any attention to the number of reboots - I assume that, for example, the availability of fossil fuels from Earth will have stopped being a limiting factor at this level of technology.

For the probability of transitioning to an interstellar state, I use the same S-curve function as above, but such that x is the number of self-sustaining settlements.

# Limitations of the calculator

I have a few concerns about the calculator, some of which point to ways I would like to see it improved if I or anyone else developed it further:

## 1) Model uncertainty
As an implementation of the model in the previous post, all [that model’s limitations](https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-beyond-a-catastrophe#Limitations_of_this_approach) apply.

## 2) AGI
The future trajectory of AGI development seems unique among foreseeable threats. Nuclear weapons, biotechnology and other advanced weaponry seem likely to pose an ongoing threat to civilisation, albeit one that might diminish exponentially as our civilisation expands. Also they could cause our civilisation to contract multiple times, in much the same way each time.

By contrast, AGI seems likely to quickly lead to one of three outcomes: extinction, existential security, or business-as-usual albeit with a new powerful tool (as in, for example, [Drexler’s AI services vision](https://www.fhi.ox.ac.uk/wp-content/uploads/Reframing_Superintelligence_FHI-TR-2019-1.1-1.pdf)). The first two aren’t ongoing probabilities from having the technology - they’re something that will presumably happen very quickly or not at all once we develop it (or, if creating a friendly AGI doesn’t mean the risk of an unfriendly one killing us reduces to near-0, either there is some similar ‘secure AGI’ that does, or we don’t have any chance of a long-term future).

To work this intuition into the model, I would like to eventually introduce a separate class of states partitioning the whole of civilisation into pre- and post- development of AGI states. Once AGI has been developed and if has neither caused extinction nor existential security, the risk of those outcomes from AGI during both times of perils and multiplanetary states would be much lower.

For the MVP of this project I've omitted AGI as a separate consideration.

## 3) Usability

The S-curve logic is fairly complex, and I wonder whether it could be simplified without losing anything of value. Perhaps more importantly, the ‘calculator’ currently is a Python script which users will need to run locally. In an ideal world it would have a browser-based UI, though the practicality of that might be limited by the next two concerns.

## 4) Runtime

Because we have to model a potentially very large number of states, depending on how much precision we go for, the current runtime of the calculator is on the order of several minutes, potentially longer. This isn’t a huge problem for generating a few individual estimates, but ideally we would be able to run a Monto Carlo simulation - that is, a simulation of the results of running the calculator a large number of times with somewhat randomised parameters. With the current runtimes this would be effectively impossible.

Most of this runtime comes from the implementation of a time of perils as having potentially thousands of progress years, each year a state to which you could theoretically transition from any other year in the same era. A future version of the calculator could implement a simpler version of the time of perils for simulation purposes, or allow greater separation of the intra-perils states from the bigger picture, to allow caching.

## 5) Function selection

The broad shape of the functions described above seem intuitively obvious to me, but people could certainly disagree. The functions shouldn’t be too hard to change if you fork the code, but these straddle the boundary between ‘model’ and ‘parameter’ in a way that makes me wonder if there shouldn’t be a more streamlined way of giving alternatives, perhaps from a pre-determined list, as input in the [parameters file](https://github.com/Arepo/lrisk_calculator/blob/main/params.yml).


## 6) No automated testing 😔

This was just due to time restrictions - I would love to set some up.

## 7) No persistence of results

Especially given the long runtimes, it would be nice to store the results in a CSV or similar, for easy sharing

# Concete TODOs:
* Double check that the maths is implemented correctly
* Tidy directory structure and leftover kruft
* Identify specific questions of interest - eg, how often do we pass through certain states on average?
* Add feature tests
* Add unit tests for full calc
* Add Sankey diagram visualisation
* Implement web version of full calculator - may require login to limit the number of submitted requests
* Look for optimisations for full calc, and/or figure out a way to determine sensible minimum runtime param values
* Extend full calc to include pre- and post-AGI world states (such that, eg., post-AGI, if we aren't in either absorbing state, the chance of transitioning directly to either one from time of perils is reduced)
* Add some initial values for full calc and/or simple calc - ideally a dropdown allowing you to select from relevant researchers' best guesses
* (With a lot of extra time); refactor to allow users to easily add and remove Markov Chain states



[^xasymptote]: strictly speaking the graph continues to rise infinitesimally forever, and, since this is a stretch, the parameter doesn’t represent a max number of years. But hopefully, by playing with it on Desmos you’ll easily get an intuition for where your value of C sets the ‘rough maximum’ to be.

[^xkrempel]: I owe this formula to Nick Krempel.
