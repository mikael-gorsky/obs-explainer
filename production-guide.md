# Production guide

This guide fixes how every episode looks and sounds, and how it is made, so that the episodes can be produced one after another without deciding these things again.

## Format

Each episode is a 16:9 video at 1920 by 1080 pixels and 30 frames a second. The long video is the ten episodes joined in order. Each episode stands alone: it opens on the building plan with its own room lit, and it ends on the plan with the next room lit. Cutting the long video into episodes therefore needs only cuts at those plan frames.

## Look

The background is the warm off-white of flow.png (#f7f6f2), with ink-coloured text (#1f1f1f). Headings are set in a serif face and all other text in a sans-serif face, as in the admin panel. The rooms and steps keep the colours of flow.png, and the colours keep their meaning throughout the series. Orange (border #e0962f, fill #fdf1dc) marks a step that calls a language model. Blue (border #3d6fa8, fill #e6eef9) marks ordinary code. Purple (border #8a5bb3, fill #f2e8f8) marks a person. Grey (border #8f8f8a, fill #ecebe6) marks something stored. A red dashed arrow (#c0392b) marks something dropped or sent back. Corners are square and lines are thin, in keeping with the admin panel's design.

## The building plan

The building plan is drawn by code (render/plan.py), so it is identical in every episode. Copy enters from the sources on the left, passes through the wire room, the barrier and the filing room, reaches the two newsrooms, is filed in the Book, and leaves through the print room to the destinations on the right. The readers' room sits below the Book, the server room in the lower left corner, and the management offices along the top. When an episode visits a room, that room is drawn in full colour and the others fade.

| Episode | Room lit |
|---|---|
| 1 | the whole building, room by room |
| 2 | wire room |
| 3 | barrier and filing room |
| 4 | the two newsrooms |
| 5 | the Book |
| 6 | print room and destinations |
| 7 | readers' room |
| 8 | server room |
| 9 | model lab and finance office |
| 10 | the whole building |

## Voice

The narrator is one calm British voice. The narration is written for the ear: full sentences in plain order, no contractions, figures that can be said aloud, and no abbreviation a listener cannot hear. It runs at about 140 words a minute, so a four-minute episode has about 560 words. Model names are not spoken; they appear on screen only.

The series is made entirely in this project's own working environment, with no use of the Observatory's services or of any outside service. The voice is Cori (en_GB-cori-high), read by Piper, an open-source speech engine that runs here, at length scale 1.05, with 0.45 seconds between sentences. Each sentence is read on its own, so that the time it begins is known exactly and a picture can begin with it (render/core.py). Piper and the voice live in the scratchpad named by PIPER_HOME.

## How an episode is made

The script of an episode (episodes/NN-*/script.md) is divided into scenes. Each scene gives its narration, what is on screen, and the screenshots and still images it needs. The pictures are drawn frame by frame in Python with Pillow, from the code in render/, and ffmpeg joins the frames, the screenshots and the voice into the episode. Each scene is drawn by its own function in render/epNN.py, which places each picture at the start of the sentence it illustrates.

Screenshots of the admin panel, the emails, the Telegram channels and the YouTube videos are supplied by the author at 1920 by 1080, with browser chrome hidden, and saved under the names the script gives them in assets/screenshots. Where a screenshot is missing, the draft cut shows a grey card with its name.

## Figures

Every figure spoken in the series is checked against the Observatory's settings or the Book shortly before the episode is voiced, because the agency keeps changing. Each script lists its figures and where each was checked.
