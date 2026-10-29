# Hi, I'm Sai Charith Reddy Yaredla 👋

I'm a software engineer interested in the intersection of **machine learning, applied AI, and backend engineering**. I like building things I can test and explain—not just getting a model to return an answer, but figuring out when that answer is reliable.

Recently, I've been focusing on two sides of AI work: building source-grounded systems people can use, and running small, reproducible experiments to understand where ML models fail.

## Projects I'm most excited about

### 🔎 [EvidenceDesk-AI](https://github.com/charithreddy9/EvidenceDesk-AI) — Finding answers without making them up

**Python · FastAPI · React · BGE-small / FastEmbed · TF-IDF · SQLite · Docker**

I built EvidenceDesk to explore a common problem with document search: finding a relevant-looking passage doesn't necessarily mean it answers the question.

I started with keyword retrieval, added local semantic embeddings, and tested where both approaches struggled. The hybrid staging version combines BGE-small with TF-IDF, checks evidence before answering, and quotes the source sentence. If the documents don't contain enough information, it abstains rather than guessing.

The part I'm particularly proud of is the evaluation loop. I kept the failed questions visible, measured how stricter filtering affected recall, and added automated checks for both answerable and unanswerable cases.

**[Try the hybrid demo](https://evidencedesk-ai-staging-bge.onrender.com)** · **[Explore the code and evaluation](https://github.com/charithreddy9/EvidenceDesk-AI/tree/staging-fastembed)** · **[CI checks](https://github.com/charithreddy9/EvidenceDesk-AI/actions)**

> The demo uses four fictional policies. Its small, manually authored evaluation set is a regression check, not a real-world accuracy benchmark. The default `main` deployment is a separate, simpler TF-IDF baseline.

### 📊 [ShiftScope](https://github.com/charithreddy9/ShiftScope) — What happens to model confidence when data changes?

**Python · scikit-learn · NumPy · SciPy · Matplotlib · GitHub Actions**

ShiftScope is a small ML research project built around a question I wanted to investigate: **when a classifier becomes less accurate, does its confidence become less trustworthy too?**

I trained logistic regression and random forest models on the scikit-learn handwritten-digits dataset, then gradually corrupted only the test images. I compared accuracy, calibration error, selective risk, and conformal prediction-set coverage across multiple random seeds.

In this controlled experiment, logistic regression accuracy dropped from about **96.6% on clean digits to 38.4% under strong noise**. The observed coverage of its nominal 90% conformal prediction sets also fell considerably. That matters because the usual coverage guarantee depends on assumptions violated by this test-time shift.

I kept the project intentionally lightweight: it runs on a laptop CPU, publishes charts and an experiment report, and has automated reproducibility checks.

**[Read the experiment](https://github.com/charithreddy9/ShiftScope)** · **[View results](https://github.com/charithreddy9/ShiftScope/blob/main/results/report.md)** · **[Reproducibility CI](https://github.com/charithreddy9/ShiftScope/actions)**

> The results describe a synthetic noise experiment on a small dataset—not broad claims about model robustness in production.

### 📬 [ActionInbox](https://github.com/charithreddy9/ActionInbox) — Turning email into tasks, with a human in control

**Python · FastAPI · scikit-learn · React · SQLite · GitHub Actions**

ActionInbox finds possible action items, categories, and due dates in pasted emails or imported `.eml` files. Instead of silently creating reminders, it shows the supporting sentence and lets you edit or reject every suggestion before saving it.

The local TF-IDF / logistic regression model was evaluated on 27 hand-written synthetic messages: **21/27 intent classifications correct**. The false positives and confusion matrix are documented rather than hidden. The repository includes automated API tests and a checked frontend build.

**[Explore the code and demo instructions](https://github.com/charithreddy9/ActionInbox)** · **[Inspect evaluation results](https://github.com/charithreddy9/ActionInbox/blob/main/research/RESEARCH.md)** · **[GitHub Actions](https://github.com/charithreddy9/ActionInbox/actions)**

> Local-first prototype only. No Gmail integration or automatic reminders; its small synthetic test is not a real-world inbox benchmark.

## Other work

- **[Flex Living Reviews Dashboard](https://github.com/charithreddy9/FlexLiving-Reviews-Dashboard):** a full-stack review analytics and reporting application.
- **[CineMatch / Movie Recommendation](https://github.com/charithreddy9/Movie-recommendation):** a content-based recommendation prototype using similarity search.
- **[RiskLens](https://github.com/charithreddy9/charithreddy9/tree/main/projects/risklens):** a synthetic transaction-risk classification and dashboard prototype.

## Tools I work with

| Area | Technologies |
| --- | --- |
| **Machine learning & evaluation** | Python, scikit-learn, NumPy, statistical metrics, calibration, experiment design |
| **Applied AI** | Embeddings, semantic search, retrieval, source-grounded answers, evaluation |
| **Backend** | FastAPI, Java, Spring Boot, SQL, REST APIs |
| **Frontend** | React, JavaScript / TypeScript |
| **Engineering** | GitHub Actions, Docker, automated tests, reproducible builds, AWS / Azure |

## What I'm working toward

I'm interested in **AI/ML engineer, applied scientist, and research-oriented software engineering** roles. I'm especially drawn to work where good experiments and careful measurement matter as much as implementation.

Next on my list: evaluating ShiftScope on a more realistic distribution shift, and testing EvidenceDesk with genuinely new documents and independently labeled answers.

---

*I enjoy understanding why a system works—and being able to show the evidence when it doesn't.*
