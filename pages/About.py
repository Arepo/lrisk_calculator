import streamlit as st

st.markdown("""
# Longtermism calculators

This site implements the cycical model of human civilisation [described here](https://forum.effectivealtruism.org/s/gWsTMm5Nbgdxedyns/p/YnBwoNNqe6knBJH8p) (with the 'survival' state replaced ). That post is recommended reading if you want to use these tools, since otherwise the inputs required for each model might be opaque.

## Simple calculator vs advanced calculator

The cyclical model and perils-focused models from that post correspond respectively to the 'simple calculator' and 'full calculator' in this repo (except that I've added an 8th state, 'future time of perils', to the cyclical one, since it seemed potentially important to distinguish between the risk of starting risk estimation from the very beginning of one and starting it from where we are now).

You can use the simple calculator from this site's homepage. It's designed to be straightforward to use and fast to run, and so makes the naive assumption that all future technological states are equivalent if they have equivalent levels of technology, or at least can be averaged over (except that it separates out our current era, on the grounds that we've survived through a number of globally catastrophic near-misses to get where we are, which might count for something).

The advanced calculator doesn't have a UI, and must be run as a script (see the [README](https://github.com/Arepo/lrisk_calculator) for instructions), but allows the user to plug in more granular [estimates of current risks](https://forum.effectivealtruism.org/posts/JQQAQrunyGGhzE23a/database-of-existential-risk-estimates), and to be more opinionated about how different civilisations might predictably face different challenges.
""")
