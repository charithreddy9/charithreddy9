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

### [ActionInbox](https://github.com/charithreddy9/ActionInbox) — Turning emails into tasks, without losing control

**Python, FastAPI, scikit-learn, React, SQLite**

I wanted a simple way to pull follow-ups out of emails without giving an app permission to do things automatically.

ActionInbox takes pasted email text or an `.eml` file and suggests an action, category, and possible due date. It shows the supporting text, then lets you edit or dismiss the suggestion before anything is saved.

The first classifier got **21 out of 27** hand-written synthetic test messages right. That's not enough to trust it on a real inbox, and the mistakes are worth looking at. I included the evaluation report and confusion matrix for that reason.

There isn't a Gmail connection or automatic sending in this version. Keeping it local and review-first was a conscious choice.

[Explore ActionInbox](https://github.com/charithreddy9/ActionInbox) · [Evaluation notes](https://github.com/charithreddy9/ActionInbox/blob/main/research/RESEARCH.md) · [CI checks](https://github.com/charithreddy9/ActionInbox/actions)

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

I want to test EvidenceDesk against documents I haven't used while developing it, try ShiftScope on more realistic kinds of distribution shift, and improve ActionInbox's handling of ambiguous requests and dates.

I'm interested in **AI/ML engineering, applied ML research, and backend software engineering**. I enjoy work where I can build the system, test the assumptions behind it, and explain what the results actually mean.
