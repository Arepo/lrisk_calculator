# L-risk calculator

To run the simple calc in a browser tab, navigate to ./calculators/website, and from the command line enter
`flask --app webapp run`

See the work in progress effective altruism [forum post](https://docs.google.com/document/d/13EOMnSSHIco50dKTba6gK8mVzitNpDSD2dbrH_gzdds/edit#) describing this project.

TODOs:
* Check that the maths is implemented correctly
* Tidy directory structure and leftover kruft
* Add feature tests
* Add unit tests for full calc
* Add Sankey diagram visualisation
* Consider Streamlit frontend
* Implement web version of full calculator - may require login to limit the number of submitted requests
* Look for optimisations for full calc, and/or figure out a way to determine sensible minimum runtime param values
* Extend full calc to include pre- and post-AGI world states (such that, eg., post-AGI, if we aren't in either absorbing state, the chance of transitioning directly to either one from time of perils is reduced)
* Add some initial values for full calc and/or simple calc - ideally a dropdown allowing you to select from relevant researchers' best guesses
