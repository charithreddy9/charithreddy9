# Hi, I'm Sai Charith 👋

**Software Engineer | Applied AI & Machine Learning | Backend Systems**

I build practical AI/ML applications and measurable experiments — from **source-grounded document retrieval** to **model reliability under distribution shift** and **local LLM email intelligence**. I enjoy the full engineering loop: designing a baseline, building the API and interface, testing where it fails, and making limitations visible.

**Focus:** Python · FastAPI · scikit-learn · local LLMs / Ollama · semantic retrieval · evaluation · React · SQL · Docker · GitHub Actions

**Featured work:** [EvidenceDesk-AI](https://github.com/charithreddy9/EvidenceDesk-AI) · [ShiftScope](https://github.com/charithreddy9/ShiftScope) · [ActionInbox](https://github.com/charithreddy9/ActionInbox/tree/feature/llm-email-intelligence)

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

### [ActionInbox](https://github.com/charithreddy9/ActionInbox/tree/feature/llm-email-intelligence) — Local LLM email-to-task intelligence

**Python · FastAPI · Ollama / Qwen3 4B · scikit-learn · React · SQLite · Gmail API (read-only)**

ActionInbox began as an explainable email-to-task baseline. Its TF-IDF classifier achieved **21/27 (77.8%)** on a small, author-written **synthetic intent-category test**, which surfaced false positives and the limits of matching isolated sentences. I then added optional Gmail read-only OAuth and a user-triggered Smart Inbox Radar, fixing edge cases such as promotional payment offers, completed confirmations, and duplicate pickup reminders.

The experimental **v5 development branch** adds **local LLM-driven extraction**: the model reads up to five manually selected emails together and proposes *zero, one or multiple* tasks, context-specific categories, deadlines and related-event groupings. The backend validates JSON structure, source IDs, date format and source quotations; tasks remain editable and **nothing is saved until approved**.

The model runs locally through Ollama without a paid AI endpoint. Automated backend/frontend checks pass, but **real-model accuracy has not been benchmarked**, and the first local inference encountered an HTTP 503 that still needs runtime verification. The older keyword radar remains available while the LLM workflow is evaluated.

[See the v5 implementation and setup](https://github.com/charithreddy9/ActionInbox/tree/feature/llm-email-intelligence) · [Automated checks](https://github.com/charithreddy9/ActionInbox/actions/workflows/ci.yml?query=branch%3Afeature%2Fllm-email-intelligence) · [Original stable baseline](https://github.com/charithreddy9/ActionInbox/tree/main)


## Other projects

- [Flex Living Reviews Dashboard](https://github.com/charithreddy9/FlexLiving-Reviews-Dashboard) — a full-stack dashboard for reviewing and filtering guest feedback.
- [Movie Recommendation](https://github.com/charithreddy9/Movie-recommendation) — a content-based recommendation prototype.
- [RiskLens](https://github.com/charithreddy9/charithreddy9/tree/main/projects/risklens) — an ML dashboard built with synthetic transaction data.

## Engineering toolkit

- **AI / ML:** scikit-learn, local LLM inference with Ollama, embeddings, hybrid retrieval, calibration, conformal prediction and model evaluation
- **Backend / data:** Python, FastAPI, Java, Spring Boot, SQL, SQLite, REST APIs
- **Frontend:** React, JavaScript and TypeScript
- **Shipping and verification:** Docker, GitHub Actions, pytest, reproducible experiments, AWS and Azure

## Current engineering priorities

My next focus is **measuring ActionInbox's real-model task extraction quality** (false positives, multi-task recall, deadline association, and latency), **evaluating EvidenceDesk on independently labeled unseen documents**, and **extending ShiftScope beyond synthetic image noise**.

I'm interested in **AI/ML engineering, applied ML research and backend software engineering**, especially roles that combine reliable models with strong software engineering.

