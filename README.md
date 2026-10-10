# The Observatory explained

An explainer video series about The Observatory, an automated news agency that runs on one Mac (repository mikael-gorsky/observatory). The series is planned as ten short episodes for a general audience skewed to the technical, made first as one long video and cut later, with animations and screenshots.

*series-plan.md* holds the agreed plan of the series, *production-guide.md* how every episode looks, sounds and is made, and *episodes/* the script of each episode. *render/* holds the code that draws the pictures: `python3 render/plan.py out` draws the building plan, whole and for each episode, into out/. `python3 render/ep01.py` reads episode 1 aloud and renders its draft into out/ep01-draft.mp4; screenshots placed in assets/screenshots under their names (S01 and so on) replace the grey cards.
