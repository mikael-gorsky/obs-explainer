# The Observatory

What the application does, how the work moves through it, and the decisions its architecture rests on. The words follow the glossary; the agency map and the flow diagram show how the work moves.

## 1. What the Observatory is

The Observatory is an information agency. It watches its beats and tells its readers what happened.

It has three departments:

- **The AI desk** watches AI and agentic software engineering. It follows about five hundred sources: X accounts, media feeds, newsletters, model hubs, release feeds, podcasts, video channels, people and institutional pages. Many publish in Chinese, because on this subject a large share of what happens first happens there.
- **The Ethiopia desk** watches what is going on in or about Ethiopia. It reads sources in English and Amharic. It starts with a pilot set of sources (four X accounts, The Reporter Ethiopia and Borkena); its full source list comes from a research round still to be done.
- **Management** decides processes, roles and money: it checks and changes the settings, approves the desks' proposals, tests and accepts the models that do the work, watches health and spending, and reports on finances.

Between them the sources deliver a few thousand entries a day, and almost none of them matter. Each desk reads what its sources deliver, decides what matters, and shares the result two ways: it sends reports on a schedule to the places its readers already are, and it answers readers' questions through its in-bound channel.

Each desk produces as many publications as it needs. A publication's specification says when it comes out, what it selects, how it is written, where it goes, who it is for and in which language. Everything inside the Observatory is in English; every publication is in English for now, and publications in other languages may come later.

| Desk | Publications |
|---|---|
| **AI desk** | AI daily, by email, on LinkedIn and on the Telegram channel @observatory_ai, with the daily update of the Book on mgorsky.net (Sunday to Friday at 07:00). Podcasts and talks about AI, by email, LinkedIn and Telegram (Sundays at 07:00). Science corner: the week's most talked-about research papers in AI and the fields around it, with editor's picks where attention is thin (Fridays at 08:00). Agentic Software Engineering: AI writing code, the advances behind it, how AI thinks, tools, and case studies (Fridays at 08:00). |
| **Ethiopia desk** | Ethiopia daily brief: current news, politics, business and social, for a general audience (Sunday to Friday at 07:00). Ethiopian banking and fintech: banks, fintech companies, digital payment systems, financial regulation and economic news involving banks, for a professional audience (Fridays at 07:00). Ethiopia AI weekly: everything AI-related that happened in Ethiopia or about Ethiopia (Wednesdays at 07:00). Each goes by email and to the Telegram channel @o_ethiopia. One-off reports, such as the security report of 2 October 2026, go out on request. |

## 2. How it works

Every desk runs the same process, with its own focus. Two stages build the desk's knowledge and two share it. Management adjusts the standards by which each desk judges.

| Stage | What happens |
|---|---|
| **Collect** | Runs often, and is shared by the desks. A dozen kinds of collector each read one kind of source and decide what counts as one entry, because only they know what they are looking at. Eight posts in a thread are one entry. One newsletter is fifteen. Everything passes through a single connector that holds the fixed shape of an entry and refuses anything malformed. Each entry then goes to the barrier of every desk that takes its source, where a cheap model answers the desk's one broad question: for the AI desk, is this about AI or agentic software engineering; for the Ethiopia desk, is this news pertaining to what is going on in or about Ethiopia. For the AI desk's X posts and its feeds and pages, a second model looks again at what the first dropped, and an entry goes on if either keeps it; this pairing was chosen after benchmarks. What no desk keeps is dropped. An episode or a video is judged by its title and description; only if it is kept is its text fetched, once, transcribed on the notebook where no transcript exists, and divided into entries by each desk that kept it. What survives goes into the Pre-Book, untranslated, marked with the desks that kept it, and is kept for a few weeks. |
