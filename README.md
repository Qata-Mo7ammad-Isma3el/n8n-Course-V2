# n8n Course NodeCraft

![Nodecraft Course Main Image](NodeCraft.png)

n8n Course Version 2: NodeCraft is a practical, project-driven learning journey built to move beyond basics into real-world automation design and production-level workflows. Created through volunteer work with IEEE and already impacting 1000+ students, this edition is focused on helping learners think like builders and ship with confidence.

## Course format (V2)

- 30 hours total
- 12 sessions
- 2.5 hours per session

## Learning outcomes

By the end of the course, students can:

- Build production-grade n8n workflows with clean data flow and reliable error handling.
- Integrate APIs, webhooks, and credentials securely.
- Use JavaScript and Code nodes to simplify complex workflows.
- Ship AI-powered automations, agents, and RAG pipelines.
- Deploy and maintain workflows with version control and best practices.

## Full course structure (V2)

### Session 1: Automation mindset and the n8n universe

- What automation means in business and where ROI comes from
- n8n vs Zapier vs Make vs custom code
- How n8n thinks: workflows, nodes, items, execution log
- First workflow walkthrough
- Mini-exercise: Hello Automation

### Session 2: Environment setup and version control

- n8n Cloud overview
- Self-hosting with Docker
- VPS deployment with EasyPanel
- Backups, naming, and workflow hygiene
- GitHub basics for automation teams
- Exercise: deploy and back up a workflow

### Session 3: Triggers, core nodes, and data flow

- Trigger tour (manual, schedule, webhook, Gmail, Sheets, forms, Telegram)
- Core nodes: Set, If, Switch, Filter, Merge, Wait, Loop Over Items
- JSON and data shaping patterns
- Project: daily scheduled report

### Session 4: APIs and the HTTP Request node

- APIs in plain language, REST basics, status codes
- Authentication types (API key, bearer, basic, OAuth2)
- HTTP Request node deep dive (methods, params, headers, pagination, files)
- FastAPI playground and debugging
- Project: public API to Sheets

### Session 5: Webhooks, credentials, and security

- Webhooks vs APIs
- Webhook + Respond to Webhook patterns
- Securing webhooks (tokens, signatures, IP allowlists)
- Credential handling and secret safety
- Project: public webhook to validated response

### Session 6: Expressions, JavaScript, and the Code node

- n8n expressions: $json, $node, $items
- JavaScript basics for automation
- Code node patterns (run once vs per item)
- Python in Code nodes (quick tour)
- Exercise: refactor a 10-node workflow into 3

### Session 7: Error handling, debugging, and production habits

- Why workflows fail and how to read errors
- Error workflows, retry, backoff, and rate limits
- Alerting via Telegram and email
- Modular sub-workflows and documentation habits
- Project: robust data-sync workflow

### Session 8: Messaging platforms - Telegram and WhatsApp

- Telegram bot workflows (text, voice, media, inline keyboards)
- WhatsApp official vs unofficial paths
- Evolution API setup and usage
- Project: two-way Telegram bot

### Session 9: Business automations - documents, OCR, workspace

- Google Workspace automation patterns
- OCR pipelines and confidence handling
- Project A: business card manager
- Project B: meeting and task assistant

### Session 10: AI core nodes and prompt engineering

- LLM basics inside n8n
- Classification, extraction, summarization
- JSON-mode and schemas
- Cost and performance awareness
- Project: inbound email triage system

### Session 11: AI agents and agent tooling

- Agents vs workflows vs chains
- Memory and guardrails
- Tooling in n8n (HTTP, Call Workflow, Code)
- Project A: calendar assistant
- Project B: WhatsApp real-estate agent

### Session 12: RAG, MCP, production, and capstone

- RAG pipelines, evaluation, and reranking
- Model Context Protocol (MCP) basics
- Production readiness: queue mode, monitoring, cost control
- Capstone options: RAG assistant, WhatsApp ordering, MCP business agent, or approved custom

## How V2 evolves from the old structure

The previous 4-session plan has been expanded into a 12-session, 30-hour track that:

- Spreads foundations (automation, APIs, setup, and core nodes) across dedicated sessions.
- Adds deep dives into error handling, messaging platforms, and production habits.
- Expands AI coverage to include core nodes, agents, RAG, and MCP.
- Increases hands-on projects and real business scenarios.

## Legacy materials mapping

When preparing a V2 session, it is important to review the legacy materials in [Old_Sessions/](Old_Sessions/) because many V2 sessions build directly on those assets.
