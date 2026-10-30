# Hi, I'm Sai Charith 👋

I'm a software engineer who enjoys backend development, machine learning, and figuring out why a system behaves the way it does.

Lately I've been building small AI tools and running experiments alongside them. The interesting part for me usually starts after the first version works: What happens when someone phrases a question differently? What does the model do with unfamiliar data? How do you catch a bad prediction before it becomes a bad user experience?

Here are a few projects I've been working on.

## Things I've built

### [EvidenceDesk-AI](https://github.com/charithreddy9/EvidenceDesk-AI) — Document search that shows its sources

**Python, FastAPI, React, SQLite, BGE-small, TF-IDF, Docker**

I wanted to build a document Q&A app that could point to the exact sentence behind an answer, rather than just return something that sounded convincing.

The first version used keyword search. It handled direct questions reasonably well but missed some paraphrases, so I tried local sentence embeddings. That helped with wording differences, but it introduced another problem: related-looking passages weren't always the *right* evidence.

I ended up combining semantic and keyword retrieval with a lightweight evidence check. The app now returns a quoted sentence and its source when it finds enough support, and says so when it doesn't. I also built an evaluation page to look at failed cases rather than relying only on an overall score.

The demo uses four fictional policy documents, so the results are useful for testing this particular system—not a claim about how well it would perform on every company's documents.

[Try the semantic demo](https://evidencedesk-ai-staging-bge.onrender.com) · [See the implementation](https://github.com/charithreddy9/EvidenceDesk-AI/tree/staging-fastembed) · [Tests and CI](https://github.com/charithreddy9/EvidenceDesk-AI/actions)

*The semantic version runs on a separate staging branch. The public production baseline uses TF-IDF.*

### [ShiftScope](https://github.com/charithreddy9/ShiftScope) — A small study of model confidence under data shift

**Python, scikit-learn, NumPy, SciPy, Matplotlib**

This one started with a question: if an ML model becomes less accurate, does its confidence change in a useful way?

I used the handwritten-digits dataset to compare logistic regression and random forest classifiers. I kept training and calibration data clean, gradually added noise to the test images, and measured accuracy, calibration error, selective risk, and conformal prediction-set coverage.

One result that stood out: logistic regression accuracy went from about **96.6% on clean images to 38.4% under heavy noise**. Its observed conformal coverage also fell well below the nominal 90% target once the test data shifted.

It's a deliberately small experiment, but I wanted to make the methodology and limitations easy to inspect. The code runs on a CPU, the plots can be regenerated, and GitHub Actions reruns the study.

[Read the research notes](https://github.com/charithreddy9/ShiftScope/blob/main/RESEARCH.md) · [See the results and plots](https://github.com/charithreddy9/ShiftScope/blob/main/results/report.md) · [Source code](https://github.com/charithreddy9/ShiftScope)

### [ActionInbox](https://github.com/charithreddy9/ActionInbox) — A quieter way to turn inbox reminders into tasks

**Python, FastAPI, scikit-learn, React, SQLite, Gmail API (optional)**

ActionInbox started as a local tool for turning a pasted email into a task I could review before saving. The first version used a small TF-IDF classifier and date rules; it scored **21/27 on an author-written synthetic category check**. That result exposed a bigger challenge than making a polished interface: a classifier can confidently mistake informational messages for things you need to do.

I added optional **read-only Gmail access** on a separate development branch. You choose when to search or scan, inspect the original message, correct suggested dates and categories, and explicitly approve any task saved to local SQLite. The app doesn't send email, change your inbox, scan in the background, or call a paid AI service.

More recently, I built **Smart Inbox Radar** to surface possible subscription renewals, bills, trial endings, luggage pickups, flight check-ins, appointments, package pickups, and document deadlines. Testing actual workflows revealed useful edge cases: promotional credit offers looked like payment deadlines; repeated HTML and legal footers became phantom tasks; and a missed luggage pickup needed a *follow-up* label rather than another upcoming reminder. I added targeted regression tests and rules for those failures, including suppressing completed confirmations and consolidating related pickup notices.

It's still a **local, review-first prototype**, not a reliable audit of everything due in a mailbox. Scans are limited, date extraction can miss details, and financial or travel alerts need verification with the original provider.

[Explore the stable baseline](https://github.com/charithreddy9/ActionInbox) · [Try the Smart Inbox Radar development branch](https://github.com/charithreddy9/ActionInbox/tree/feature/smart-inbox-radar) · [View test runs](https://github.com/charithreddy9/ActionInbox/actions)

*The baseline stays on `main`; Gmail and Smart Inbox Radar are under active development on feature branches.*

## Other projects

- [Flex Living Reviews Dashboard](https://github.com/charithreddy9/FlexLiving-Reviews-Dashboard) — a full-stack dashboard for reviewing and filtering guest feedback.
- [Movie Recommendation](https://github.com/charithreddy9/Movie-recommendation) — a content-based recommendation prototype.
- [RiskLens](https://github.com/charithreddy9/charithreddy9/tree/main/projects/risklens) — an ML dashboard built with synthetic transaction data.

## What I use

- **Python and ML:** scikit-learn, NumPy, model evaluation, embeddings, information retrieval
- **Backend:** FastAPI, Java, Spring Boot, SQL, REST APIs
- **Frontend:** React, JavaScript, TypeScript
- **Development:** Git, GitHub Actions, Docker, automated tests, AWS and Azure

## What I'm learning next

I'm working toward more independent evaluation for EvidenceDesk, more realistic distribution shifts for ShiftScope, and a better way for ActionInbox to distinguish an upcoming obligation from a confirmation, advertisement, or already-failed event. For ActionInbox, the next step is to measure real extraction errors before adding notifications or more automation.

I'm interested in **AI/ML engineering, applied ML research, and backend software engineering**. I enjoy work where I can build the system, test the assumptions behind it, and explain what the results actually mean.
