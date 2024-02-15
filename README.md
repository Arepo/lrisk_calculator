# L-risk calculator

This repo contains a functional but unfinished implementation of the models of human civilisation development described [here](https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-beyond-a-catastrophe) (though note updates to the cyclical model described [here](https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/ouuj93CPymfnvu8uQ)). Those posts are highly recommended reading if you want to use these tools, otherwise the inputs required for each model might be opaque.

The cyclical model and (decay plus perils-focused models) from that post correspond respectively to the 'simple calculator' and 'full calculator' in this repo. I've called them L(ongtermist)-risk calculators because they get at what I think are the core intuitions behind longtermism better than than the concept of existential risk, which has various problems I've described [here](https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/fi3Abht55xHGQ4Pha).

The simple calc is live at https://l-risk-calculator.streamlit.app/. Instructions for using it are on the page itself. To run it locally, navigate to the project folder and enter `streamlit run Longtermist_Risk_Calculator.py`, and it will open automatically.

To run the full calc:

1.  Set the values in ./calculators/full_calc/runtime_constants.py: higher values of MAX_PLANETS, MAX_CIVILISATIONS, MAX_PROGRESS_YEARS give a higher fidelity representation of the model (which theoretically allows unlimited numbers of each), but rapidly increase runtime, which I think is O(MAX_CIVILISATIONS * MAX_PROGRESS_YEARS^2). On my 2019 Macbook Pro, the runtime with the default settings for these files tends to be around 12 minutes.

2. Set the the nominal parameters of the model in params.yml. You might also choose to edit the functions that use those parameters to determine transitional probabilities - the functions I've used describe as simply as I could a fairly customisable S-curving development of various relevant technology-driven transitional probabilities. The yml file extensively discusses what these parameters represent.

3. Navigate to the project directory, and run `python full_calc.py`. This will output a printout of your parameters, the chances of success they imply from each civilisational state, and some further metadata, and save the result to results.csv. Please consider either submitting a PR with your results or pasting them onto this shared worksheet: https://docs.google.com/spreadsheets/d/132hveII9MYkGrW0uDvYzh1pqcmAqKuxQ3pHq6iCZH2A/edit#gid=0 - I'd love to see them! (beware that adding parameters can mess up the column arrangement of your row, so if you notice that's happened, you might want to describe what you changed in detail in the notes column)

4. The project uses the Markov chain library [PyDTMC](https://github.com/TommasoBelluzzo/PyDTMC). Note that its readme isn't comprehensive. Some useful clarifications in case you want to dig further into the code:
* the MarkovChain object has a `.states` property, which I find useful to confirm ordering in the full transition matrix
* the `mc.absorption_probabilities()` function produces an array of arrays with one top-level array for each absorbing state (in our case, two), in the order they were passed to the constructor (in our case, Extinction first, then Interstellar). The subarray elements correspond to the probability of hitting that absborbing state from each non-absorbing state, again in the order the were passed to the constructor (in our case, the preindustrial states for each possible future civilisation up to <the max number of future civilisations - 1>, then the industrial ones, etc)

5. Look at your results either in the printed output, or in the row added to `./results.csv`, which might be clearer. The value you most care about to start with is probably the 'perils-0' column, which represents our current all-things-considered probability of eventually becoming interstellar or existentially secure (whichever you choose to interpret and parameterise that end state as).

# Development roadmap/main TODOs:
* Double check that the maths is implemented correctly
* Tidy directory structure and leftover kruft
* Identify specific questions of interest - eg, how often do we pass through certain states on average?
* Add feature tests
* Add unit tests for full calc
* Add Sankey diagram visualisation
* Implement web version of full calculator - may require login to limit the number of submitted requests
* Look for optimisations for full calc, and/or figure out a way to determine sensible minimum runtime param values
* Extend full calc to include pre- and post-AGI world states (such that, eg., post-AGI, if we aren't in either absorbing state, the chance of transitioning directly to either one from time of perils is reduced)
* Add multiple sets of 'default' params to both simple and full calcs, based on averaged results, specific researchers etc
* Add an option for a [decreasing derivative formula](https://gamedev.stackexchange.com/questions/89723/how-can-i-come-up-with-a-simple-diminishing-return-equation/89744#89744) rather than the S-curve formulae, if it seems possible to do so without making the program harder to use overall
* (With a lot of extra time): refactor to allow users to easily add and remove Markov Chain states via a UI
* (With a lot of extra time, only possible after significant optimisations): introduce some kind of Monte Carlo simulation functionality
* Consider simplifying the perils graphing functions
* Have an option to look at Time of Perils in 10-progress-year-chunks, for greater runtime
* Implement zipf algorithm for intra-perils regressions (see preliminary commented out version in file)

## Running with pipenv

pipenv is a virtual environment tool which isolates python dependencies, which reduces dependency conflicts. To install pipenv and run this program, you can try:

```
pip3 install pipenv
python3 -m pipenv install --dev
python3 -m  pipenv shell
# then inside the pipenv shell:
  python --version
  python full_calc.py
```

For an Ubuntu 20.04 machine which has various python installations, this might instead look like:

```
pip3.10 install pipenv
python3.10 -m pipenv install --dev
python3.10 -m  pipenv shell
# then inside the pipenv shell:
  python --version # 3.10
  python full_calc.py
```

We are using python 3.10 as that's the version @Arepo used, and it will probably give fewer problems.

Some debugging commands which might help are:

```
pip3.10 install --upgrade pip wheel setuptools requests
sudo apt remove pipenv # use pip version, not apt version
```

