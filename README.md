<div align="center">

# Sai Charith Reddy Yaredla
### Full-Stack AI/ML Engineer · Applied Machine Learning · LLM Applications · AI Product Engineering

**I build AI-powered products end to end:** from reproducible data and model evaluation to Python APIs, responsive interfaces, testing, and delivery.

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-149ECA?logo=react&logoColor=white)](https://react.dev)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://docker.com)

</div>

## 🚀 Featured AI/ML engineering projects

EvidenceDesk now has its own standalone repository; RiskLens remains a project folder. **Both are prototypes under active development—not deployed products.**

### 01 · [EvidenceDesk — Citation-Grounded AI Knowledge Workspace](https://github.com/charithreddy9/EvidenceDesk-AI)

> **Applied AI / RAG-style retrieval / Full-stack development**

A knowledge assistant with document ingestion, source-linked evidence, explicit abstention, and optional LLM-based synthesis.

**Built with:** Python · FastAPI · scikit-learn TF-IDF · React · Vite · optional OpenAI API

**Engineering details:** in-memory document indexing, cosine retrieval, input validation, source passages, offline evaluation script, API tests, and a responsive interface.

[**View source & setup →**](https://github.com/charithreddy9/EvidenceDesk-AI) · [Retrieval implementation](https://github.com/charithreddy9/EvidenceDesk-AI/backend/retrieval.py) · [Evaluation script](https://github.com/charithreddy9/EvidenceDesk-AI/backend/evaluate.py)

### 02 · [RiskLens — Transaction Risk ML Analytics Dashboard](./projects/risklens)

> **Machine learning / Classification / Model evaluation / Full-stack inference**

An ML-backed risk scoring dashboard using **fictional synthetic financial transactions**. Compare a boosted-tree classifier with a logistic-regression baseline and inspect validation metrics.

**Built with:** Python · scikit-learn · NumPy · FastAPI · React · Vite

**Engineering details:** deterministic data generation, stratified train/validation split, precision-recall evaluation, ROC AUC, global permutation importance, typed API inputs, dashboard, and tests.

[**View source & setup →**](./projects/risklens) · [Modeling pipeline](./projects/risklens/backend/model.py) · [Evaluation script](./projects/risklens/backend/evaluate.py)

### 03 · [CineMatch — Movie Recommendation System](https://github.com/charithreddy9/Movie-recommendation)

> **Recommendation algorithms / Full-stack ML prototype**

Content-based recommendation using TF-IDF cosine similarity with a FastAPI serving layer and React interface. Uses a small fictional movie catalog for demonstration.

[**Open repository →**](https://github.com/charithreddy9/Movie-recommendation)

### 04 · [Flex Living Reviews Dashboard](https://github.com/charithreddy9/FlexLiving-Reviews-Dashboard)

> **Full-stack software engineering / Data visualization**

Existing React/TypeScript + Node/Express application featuring review normalization, filtering, dashboard reporting, and REST API integration.

[**Open repository →**](https://github.com/charithreddy9/FlexLiving-Reviews-Dashboard)

---

## 🧠 Engineering focus

| Area | Core technologies |
|---|---|
| Applied AI | Retrieval-augmented generation, prompt design, LLM APIs, embeddings concepts, evaluation |
| ML engineering | scikit-learn, feature engineering, classification, recommendation, model metrics |
| Backend systems | Python, FastAPI, Java/Spring Boot, Node.js, REST APIs, PostgreSQL |
| Frontend | React, TypeScript, JavaScript, responsive UI |
| Engineering practices | Automated testing, GitHub Actions, Docker, reproducible experiments, cloud workflows |

## 🔍 How to evaluate my work

My portfolio aims to provide **real implementation evidence, not just screenshots**:

- **Run it:** each project contains local instructions and a self-contained backend/frontend.
- **Inspect it:** ML pipeline, API contracts, data-generation logic, and source files are linked above.
- **Test it:** code-level automated tests and evaluation scripts are included.
- **Understand it:** project READMEs document tradeoffs, limitations, next steps, and dataset provenance.

**Current limitations:** new projects have not yet been production-deployed; their frontend builds and cross-environment CI are being validated. RiskLens uses exclusively synthetic financial data; EvidenceDesk contains fictional policy documents and uses lexical retrieval with optional LLM synthesis. No real-world model performance is claimed.

## 📍 Next build milestones

1. Validate CI and add integration test coverage.
2. Add real public benchmark datasets with clear licensing, robust ML evaluation, and per-case error analysis.
3. Add containers, polished screenshots, deployed demos, and observability.
4. Publish RiskLens as its own repository and pin the strongest projects.

---

**Let's build useful AI systems that people can inspect, test, and trust.**
