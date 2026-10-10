# Episode 1. A news agency with no staff

Length: about 4 minutes, 560 words of narration. Room lit: the whole building, drawn room by room.

## Scene 1. The morning issue (0:00 to 0:25)

**Narration.** Every morning at seven, an email called AI daily goes out to its readers. It carries twenty short stories about artificial intelligence, each with its source. Nobody wrote it. No person chose the stories, checked them, or pressed send.

**On screen.** Small cards scroll upward across the whole frame, about two hundred of them, each a rectangle with a thin border and two grey lines standing for text. A few carry a word in English, Chinese or Amharic, so that the mix of languages is visible. A clock in the upper right corner turns from 06:59 to 07:00. At that moment the cards fall together into the centre and become a screenshot of an AI daily email (S01). On "Nobody wrote it", the email fades to half strength and the words "no editor, no staff" appear over it in the serif face.

## Scene 2. The size of the problem (0:25 to 1:10)

**Narration.** The email comes from the Observatory, a news agency that runs on one laptop. It follows 575 sources. Most of them write in English, but 47 write in Chinese and 29 in Amharic. Together they deliver several thousand items every week: posts, articles, newsletters, papers, podcasts and videos. Out of all this, the agency picks twenty stories a day for one of its desks and fifteen for the other. This series explains how a program can make that choice, and make it well enough that people want to read the result.

**On screen.** A large number counts up from 0 to 575. Below it, a horizontal bar divides into three parts as the languages are named: 497 English, 47 Chinese, 29 Amharic, with the remaining two labelled "French and Russian". On "posts, articles, newsletters", seven small icons appear in a row, one for each kind of item, drawn as simple outlines. A funnel then draws itself, wide at the top and narrow at the bottom. Hundreds of dots pour in at the top, and twenty come out at the bottom and line up as twenty short bars. On the last sentence, a question in the serif face fills the lower third: "How does a program choose twenty stories out of thousands?"

## Scene 3. What the agency produces (1:10 to 2:00)

**Narration.** The agency has two desks. The AI desk follows artificial intelligence, and above all the use of AI to write software. The Ethiopia desk follows news in and about Ethiopia, with the economy and banking first. Each desk publishes on a timetable. The AI desk sends a daily email, a weekly digest of research papers, a weekly issue on agentic software engineering, and short spoken videos. The Ethiopia desk sends a daily brief and two weekly issues, one on banking and one on AI in Ethiopia. Readers choose what they receive, by email or by Telegram, at their own hour, and in English, Russian or Amharic.

**On screen.** The frame divides into two columns headed "AI desk" and "Ethiopia desk". As each publication is named, a card appears in its column with the publication's name and its day and time: AI daily, Sunday to Friday, 07:00; Science corner, Friday, 08:00; Agentic Software Engineering, Friday, 08:00; the spoken AI daily and the shorts, daily; Ethiopia daily brief, Sunday to Friday, 07:00; Ethiopian banking and fintech, Friday, 07:00; Ethiopia AI weekly, Wednesday, 07:00. The columns then slide aside for four screenshots that appear one after another, each for about three seconds: a Telegram post in the AI channel (S02), the public site's home page (S03), a frame of a spoken AI daily video (S04), and a frame of an Agentic Software Engineering short (S05). On the last sentence, a screenshot of a reader's subscription page (S06) shows the choice of channel, hour and language.

## Scene 4. No staff and one machine (2:00 to 2:45)

**Narration.** There are no staff. One laptop runs everything, and every connection goes out from it: to the sources, to the companies that run the language models, and to the places where the issues are published. Nothing connects to it from outside. The language models it uses are small and cheap. In a recent week, the whole agency spent about seven dollars on them. Cheap models make mistakes. They misread, they add details that were never there, and they believe what a company says about itself. Much of this series is about how the design catches those mistakes.

**On screen.** A plain line drawing of an open laptop sits in the centre: a rectangle for the screen, a flat trapezium for the base, thin ink lines on the off-white background. Arrows grow outward from it in three directions, to three labelled groups: "sources" on the left, "language models" at the top, and "readers" on the right. Each arrow has its head at the far end, pointing away from the laptop. On "Nothing connects to it from outside", a dashed arrow tries to come in from the bottom edge and stops short with a small red cross. On "seven dollars", a price tag appears above the laptop reading "about $7 a week". On "Cheap models make mistakes", three short phrases appear one after another beside the laptop, each in orange: "misreads the source", "adds a detail", "believes the press release".

## Scene 5. Documents before code (2:45 to 3:30)

**Narration.** Before any code was written, the system was described as a news agency, in plain documents. A glossary names every part. A flow diagram shows how the work moves. A description of the application says what each part does, and why. So the agency has rooms, and each room has a job. Copy arrives in the wire room. A barrier turns away what is off the subject. The newsrooms choose the stories and check them. The archive, called the Book, keeps every note. The print room makes the issues, and the readers' room answers questions. Management sets the rules and pays the bills.

**On screen.** Three screenshots of the documents appear side by side, slightly overlapping, as pages: the glossary (S07), the flow diagram (the file flow.png from the Observatory repository) and the opening of the application description (S08). They slide away, and the building plan draws itself from render/plan.py, one room at a time, each room appearing as the narration names it: wire room, barrier, filing room, the two newsrooms, the Book, print room, readers' room, and finally the four management offices along the top. The arrows between the rooms draw last.

## Scene 6. The map of the series (3:30 to 4:00)

**Narration.** Each of the next episodes visits one of these rooms, and explains the engineering idea behind it. Along the way we follow one real story, from the moment its source publishes it to the moment a reader opens it. The story begins where every story begins, at the door of the wire room.

**On screen.** The complete building plan. A small numbered disc appears in the corner of each room, giving the episode that visits it, in the order of the table in production-guide.md. On "one real story", a single card, the same shape as the cards of scene 1 but outlined in red, appears at the left edge among the sources. On the last sentence, every room fades except the wire room, and the card moves to its door. The frame holds for two seconds.

## Screenshots needed

S01 is an AI daily email as a reader sees it, the whole message in one tall image. S02 is a post in the AI Telegram channel. S03 is the home page of observatory.mgorsky.net. S04 is one frame of a spoken AI daily video. S05 is one frame of an Agentic Software Engineering short, with a story typed on the terminal. S06 is a reader's subscription page on the public site. S07 is the opening of observatory-glossary.md as rendered on GitHub. S08 is the opening of Observatory application.md as rendered on GitHub. S07 and S08 can be drawn here from the repository files, so the author needs to supply only S01 to S06.

## Figures and where they were checked

575 sources switched on, 516 for the AI desk and 59 for the Ethiopia desk; 497 in English, 47 in Chinese, 29 in Amharic, 1 in French and 1 in Russian: config/sources.json, 10 October 2026. Twenty stories a day for the AI desk and fifteen for the Ethiopia desk: config/newsrooms.json, first_priority. Several thousand items a week: the Pre-Book held 19,830 items over its 21 days on 7 October (observatory-agency-map.md), which is more than six thousand a week. About seven dollars a week: $7.26 in the seven days to 7 October (observatory-agency-map.md); to be checked again before voicing. The timetable: config/publications.json, 10 October 2026.
