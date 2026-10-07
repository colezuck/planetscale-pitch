# Metal teach-back preparation

A five-minute explanation to an Aurora Postgres staff engineer, followed by questions. Read the [assignment](../brief/README.md), [slide plan](slide-plan.md), [speaking script](script-outline.md), and [Q&A](questions.md).

One problem: high I/O demand can create storage waits, slow customer-facing features and limit growth headroom. Metal’s local NVMe changes the persistent storage path; managed HA supports recovery when nodes fail. Connect each mechanism to customer experience, usage growth and engineering focus.

Five slides: Intro → Impact of Metal → Intercom business results → combined What is Metal / Aurora comparison → Postgres benchmark. Intercom is Vitess/MySQL, not a Postgres case study. Its 60%+ saving is database cost versus previous EBS io2, not total cloud spend. Convex, Depot and the tradeoffs slide are retained but hidden; volunteer capacity planning during Metal.

[Evidence review](../../context/product/aurora-metal-teach-back.md); [deck implementation](../../decks/teach-back/README.md); [Notion notes](https://app.notion.com/p/3ef1840cbb9e8105a768d99d5570e754), reconciled October 6, 2026. Manager feedback is preserved at the bottom. Aloud timing remains to be rehearsed.

The outcome and teaching slides have readable spoken paragraphs and one optional understanding question; the cover stays brief. The question checks the explanation rather than qualifying buying intent; prioritize the Metal question within five minutes.
