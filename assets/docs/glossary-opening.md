# The Observatory — glossary

What we call each part of the agency, each piece of content at each step, and each part of the app. One name per thing. The agency map (*The Observatory, an information agency*) and the flow diagram (*The Observatory — how the work flows*) show how the work moves, and this glossary follows them. If a name here disagrees with an older document, this one wins.

## The agency

The Observatory is an information agency. It has news desks, which watch the world and publish, and a management department, which decides how the desks work.

| Term | What it means |
|---|---|
| **Desk** | A news department with one general topic. Every desk runs the same process with its own focus: its own sources, its own scope rule, priorities, tag list and type checks, its own publications and its own weekly budget. There are two: the **AI desk** and the **Ethiopia desk**. |
| **AI desk** | Watches AI and agentic software engineering. |
| **Ethiopia desk** | Watches what is going on in or about Ethiopia. It reads sources in English and Amharic. |
| **Management** | The department that decides processes, roles and money: it checks and changes the settings, approves the desks' proposals, tests and accepts the models that do the work, watches health and spending, and reports on finances. |
| **Focus** | A desk's general topic. The desk defines the topic only; each publication defines its own audience. |
| **Working language** | The language of everything inside a desk: English for both desks today. Every note is written in it, whatever language its source used; an entry in any other language is translated into it first. Each desk names it in its settings (working_language, with its code in working_language_code), and the translator and the clipper are asked for it. |

A desk does not define an audience or a language of publication. Those belong to each publication, in its specification.

## One Book, separate newsrooms

Both desks keep their notes in one Book, so that connections between them can be seen, for example how global or Chinese AI activity bears on Ethiopia. The desks' work never mixes:

1. **One desk per piece of work.** Every model call, run and prompt carries exactly one desk; no model sees both desks' material at once.
2. **Own settings.** Each desk has its own scope rule, priorities, tag list and type checks. Nothing is shared by default.
3. **Notes are read by desk.** Every publication belongs to one desk, and the code reads notes only for a named desk.
4. **Own feedback loop.** Each desk's criteria review reads only its own notes; management approves desk by desk.
5. **Own resources.** Each desk has its own weekly spending limit.

What is shared is done once: collecting, the connector, and transcription of each episode. A source may serve more than one desk. The AI desk does not read the Ethiopia desk's notes.

## A desk's process

The same stages on every desk, in this order:

collector → connector → barrier → transcriber → splitter → Pre-Book → compare and select → translator → credibility check → clipper → tagger → Book → selector → grouper → report writer → translate (optional) → format → publish.

| Stage | What it does |
|---|---|
| **1 · Collect** | Many sources in, one connector, the desk's barrier, into the Pre-Book. Runs often. Collecting and the connector are shared by the desks; each desk's barrier judges only the entries from the sources it takes. |
