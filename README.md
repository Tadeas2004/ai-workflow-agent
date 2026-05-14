# AI-Powered Asynchronous Email Intelligence & Analytics Pipeline

An enterprise-grade, idempotent email automation and processing framework. The system establishes a secure integration with the **Gmail REST API via OAuth2**, enforces transactional integrity and exact-once processing semantics using a localized **SQLite state tracking engine**, and orchestrates a highly deterministic **Two-Step LLM Inference Chain** powered by the `google-genai` SDK and the `gemini-2.5-flash-lite` model.

**Live Production Instance:** [ai-email-agent-9n28.onrender.com](https://ai-email-agent-9n28.onrender.com)

---

## 🏗️ Architectural Overview & Design Patterns

The pipeline is architected to address common distributed systems and LLM integration challenges, specifically **structural drift, hallucinations, API rate-limiting, and state synchronization**.

### System Workflow Dataflow
