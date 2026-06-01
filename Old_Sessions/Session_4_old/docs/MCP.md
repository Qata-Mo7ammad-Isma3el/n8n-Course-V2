# MCP in n8n — The Complete Guide

## What is MCP?

**MCP (Model Context Protocol)** is an open standard created by **Anthropic** (makers of Claude) in November 2024. It solves one big problem:

> AI models are smart, but they're **trapped**. They can't access your databases, tools, or apps on their own.

MCP fixes this by giving AI a **universal plug** to connect to the outside world — like **USB-C for AI**.

```
Before MCP:  AI ←→ Custom Code ←→ Tool A
             AI ←→ Custom Code ←→ Tool B
             AI ←→ Custom Code ←→ Tool C
             (every tool needs its own custom integration)

After MCP:   AI ←→ MCP ←→ Tool A
                       ←→ Tool B
                       ←→ Tool C
             (one standard protocol for everything)
```

---

## How MCP Works (The 4 Players)

```
┌─────────────────────────────────────────────────────┐
│                    MCP HOST                         │
│  (The app you interact with: Claude, ChatGPT, n8n)  │
│                                                     │
│   ┌──────────────┐      ┌──────────────────┐        │
│   │   LLM Brain  │ ←──→ │   MCP CLIENT     │        │
│   │  (thinks &   │      │  (translator     │        │
│   │   decides)   │      │   between LLM    │        │
│   └──────────────┘      │   and servers)   │        │
│                         └────────┬─────────┘        │
└──────────────────────────────────┼──────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
              ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
              │ MCP SERVER│  │ MCP SERVER│  │ MCP SERVER│
              │ (Gmail)   │  │ (Slack)   │  │ (Database)│
              └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
                    │              │              │
              ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
              │  Gmail    │  │  Slack    │  │  Postgres │
              │  API      │  │  API      │  │  Database │
              └───────────┘  └───────────┘  └───────────┘
```

| Component | What It Does | Simple Analogy |
|-----------|-------------|----------------|
| **MCP Host** | The app you use (Claude, n8n) | Your phone |
| **MCP Client** | Translates requests between AI and servers | The USB-C port |
| **MCP Server** | Connects to a specific tool/data source | The cable to each device |
| **Transport Layer** | Carries messages (uses JSON-RPC 2.0) | The electrical signal in the cable |

---

## What is n8n?

**n8n** is an open-source **workflow automation platform**. Think of it as LEGO blocks for connecting apps — you drag, drop, and link services together visually without writing much code.

n8n supports 400+ integrations (Gmail, Slack, databases, APIs, etc.) and has **native AI capabilities**.

---

## MCP + n8n = Why It Matters

n8n and MCP together create a **two-way street**:

```
Direction 1: n8n AS an MCP Server
─────────────────────────────────
External AI (Claude, ChatGPT)  ──→  n8n workflows
"Hey Claude, run my lead-scoring workflow"

Direction 2: n8n AS an MCP Client
─────────────────────────────────
n8n AI Agent  ──→  External MCP Servers
"n8n agent, use the Notion MCP server to grab my tasks"
```

---

## The Two MCP Nodes in n8n

n8n gives you **two built-in nodes** to work with MCP:

### 1. MCP Server Trigger Node

> **Purpose:** Makes your n8n workflows available to external AI agents.

```
┌──────────────────────────────────────────────┐
│          n8n WORKFLOW                        │
│                                              │
│  ┌────────────────┐    ┌──────────────────┐  │
│  │ MCP Server     │───→│ Tool: Search DB  │  │
│  │ Trigger        │───→│ Tool: Send Email │  │
│  │ (exposes URL)  │───→│ Tool: Get Report │  │
│  └────────────────┘    └──────────────────┘  │
│         ▲                                    │
└─────────┼────────────────────────────────────┘
          │
    ┌─────┴─────┐
    │  Claude   │  "Search the database for Q4 sales"
    │  Desktop  │
    └───────────┘
```

**How it works:**

1. Add an **MCP Server Trigger** node to your workflow
2. Connect **tool nodes** to it (Gmail, Slack, HTTP Request, custom functions, etc.)
3. n8n generates a **URL** (test and production)
4. Give that URL to any MCP client (Claude Desktop, ChatGPT, Cursor, etc.)
5. The AI can now **discover and call** your tools

**Key settings:**

| Setting | What to Do |
|---------|-----------|
| MCP URL Path | Auto-generated, or customize it |
| Authentication | None (testing), Bearer token, or Header auth (production) |
| Test URL | Active when you click "Listen for Test Event" |
| Production URL | Active when you publish/activate the workflow |

### 2. MCP Client Tool Node

> **Purpose:** Lets your n8n AI agents use tools from external MCP servers.

```
┌─────────────────────────────────────────────────┐
│                n8n WORKFLOW                     │
│  ┌─────────┐   ┌──────────┐   ┌──────────────┐  │
│  │ Chat    │──→│ AI Agent │──→│ MCP Client   │  │
│  │ Trigger │   │ (LLM)    │   │ Tool         │  │
│  └─────────┘   └──────────┘   └──────┬───────┘  │
│                                      │          │
└──────────────────────────────────────┼──────────┘
                                       │
                              ┌────────▼────────┐
                              │ External MCP    │
                              │ Server          │
                              │ (e.g., Notion,  │
                              │  Airtable, etc.)│
                              └─────────────────┘
```

**How it works:**

1. Add a **trigger** (Chat, Webhook, Schedule, etc.)
2. Add an **AI Agent** node with your LLM of choice
3. Add **MCP Client Tool** node and connect it to the agent
4. Enter the **SSE Endpoint URL** of the external MCP server
5. Set authentication if required
6. Choose which tools to expose: **All** or **Selected**
7. Your n8n agent can now call external MCP tools

---

## Instance-Level MCP Access (New)

n8n also offers a **centralized MCP access** option — instead of per-workflow MCP triggers, you expose your whole n8n instance to MCP clients.

```
┌─────────────────────────────────────────┐
│  n8n Instance                           │
│                                         │
│  Workflow A  -> Available in MCP        │  
│  Workflow B  -> Available in MCP        │ 
│  Workflow C  -> Not exposed             │ 
│  Workflow D  -> Available in MCP        │
│                                         │
│  Settings > Instance-level MCP          │
│  ┌─────────────────────────────────┐    │
│  │ Auth: OAuth or Access Token     │    │
│  │ URL: your-instance.n8n.cloud    │    │
│  └─────────────────────────────────┘    │
└────────────────────┬────────────────────┘
                     │
        ┌────────────▼────────────┐
        │  Claude / Lovable /     │
        │  any MCP client         │
        └─────────────────────────┘
```

**Key rules:**

- Workflows must be **published** to be eligible
- You must **explicitly enable** each workflow for MCP access
- n8n enforces a **5-minute timeout** for MCP-triggered executions
- Auth options: **OAuth** (recommended) or **Personal Access Token**

---

## MCP Server Trigger vs. Instance-Level MCP

| Feature | MCP Server Trigger Node | Instance-Level MCP |
|---------|------------------------|-------------------|
| Scope | One workflow only | Multiple workflows |
| Setup | Per-workflow node | Central settings page |
| Use case | Custom MCP server behavior | Quick blanket access |
| Auth | Bearer / Header | OAuth / Access Token |
| Workflow editing from AI | No | No |
| URL | Per-workflow URL | One instance URL |

---

## Real-World Example: Full Flow

**Scenario:** You want Claude Desktop to manage your Airtable task planner via n8n.

```
Step 1: Build the MCP Server in n8n
────────────────────────────────────
┌────────────────┐    ┌─────────────────┐
│ MCP Server     │───→│ Airtable:       │
│ Trigger        │    │ List Tasks      │
│                │───→│ Airtable:       │
│ (Production    │    │ Create Task     │
│  URL active)   │───→│ Airtable:       │
│                │    │ Update Task     │
└────────────────┘    └─────────────────┘
     ▲
     │ Bearer Auth token: "my-secret-token"
     │ URL: https://my-n8n.com/mcp/tasks

Step 2: Connect Claude Desktop
──────────────────────────────
Add to claude_desktop_config.json:
{
  "mcpServers": {
    "n8n-tasks": {
      "command": "npx",
      "args": ["mcp-remote",
               "https://my-n8n.com/mcp/tasks"],
      "env": {
        "MCP_BEARER_TOKEN": "my-secret-token"
      }
    }
  }
}

Step 3: Talk to Claude
──────────────────────
You: "Show me all overdue tasks in Airtable"
Claude: *calls List Tasks tool via MCP*
Claude: "You have 3 overdue tasks: ..."

You: "Mark the first one as done"
Claude: *calls Update Task tool via MCP*
Claude: "Done! Task marked as complete."
```

---

## Building an MCP Client Workflow in n8n

**Scenario:** Your n8n AI agent needs to pull data from an external Notion MCP server.

```
┌─────────┐    ┌───────────┐    ┌───────────────┐
│  Chat   │───→│ AI Agent  │───→│ MCP Client    │
│  Input  │    │ (Claude   │    │ Tool          │
│         │    │  Sonnet)  │    │               │
└─────────┘    └───────────┘    │ SSE Endpoint: │
                                │ https://mcp.  │
                                │ notion.com/mcp│
                                └───────────────┘

User types: "What meetings do I have tomorrow?"
→ AI Agent decides to use Notion calendar tool
→ MCP Client calls the Notion MCP server
→ Results come back
→ AI formats and responds
```

**Setup steps:**

1. Create new workflow → Add **Chat Trigger**
2. Add **AI Agent** node → Pick your LLM model
3. Add **MCP Client Tool** → Paste the SSE endpoint URL
4. Set auth (Bearer, Header, OAuth2, or None)
5. Choose tools: All or Selected
6. Activate → Open chat → Start asking questions

---

## n8n-MCP (Community Tool)

There's also a popular **community MCP server** ([github.com/czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp)) that does something different: it gives AI assistants **deep knowledge about n8n itself** — all 1,000+ nodes, their properties, and documentation.

```
┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ Claude Code  │────→│ n8n-MCP     │────→│ Your n8n     │
│ or Cursor    │     │ Server      │     │ Instance     │
│              │     │             │     │              │
│ "Build me a  │     │ - Node docs │     │ Creates &    │
│  workflow    │     │ - Validation│     │ manages      │
│  that..."    │     │ - Examples  │     │ workflows    │
└──────────────┘     └─────────────┘     └──────────────┘
```

This lets AI **build, validate, and deploy** n8n workflows for you.

---

## MCP vs RAG — Quick Comparison

| | MCP | RAG |
|---|-----|-----|
| **Purpose** | Connect AI to tools & actions | Feed AI with relevant documents |
| **Direction** | Two-way (read AND write) | One-way (read only) |
| **Can take actions?** | Yes (send emails, update records) | No (only retrieves info) |
| **Standardized?** | Yes (open protocol) | No (it's a technique) |
| **Best for** | AI agents that DO things | AI chatbots that KNOW things |

---

## Transport: How MCP Messages Travel

```
MCP Client  ←──JSON-RPC 2.0──→  MCP Server

Two transport methods:
┌────────────────────────────────────────────┐
│ stdio (Standard Input/Output)              │
│ → For LOCAL servers                        │
│ → Fast, synchronous                        │
│ → Used by Claude Desktop configs           │
├────────────────────────────────────────────┤
│ SSE (Server-Sent Events) / Streamable HTTP │
│ → For REMOTE servers                       │
│ → Real-time streaming                      │
│ → Used by n8n's MCP nodes                  │
└────────────────────────────────────────────┘
```

> **Important for n8n:** Since n8n uses SSE/streamable HTTP, connecting stdio-based clients like Claude Desktop requires a proxy bridge (like `mcp-remote`).

---

## Security Best Practices

| Practice | Why |
|----------|-----|
| Always use **Bearer auth** in production | Prevents unauthorized access to your MCP URL |
| Store tokens as **environment variables** | Never hardcode secrets in workflows |
| **Explicitly enable** workflows for MCP | No workflow is exposed by default |
| Use **long, random tokens** | Short tokens are easy to guess |
| Log MCP operations | For auditing who called what and when |
| Strip sensitive data | Control what the AI can see in responses |

---

## Quick-Start Checklist

**Want n8n to BE an MCP Server (AI calls your workflows)?**

- [ ] Create a workflow in n8n
- [ ] Add **MCP Server Trigger** node
- [ ] Connect tool nodes (Gmail, Slack, HTTP, custom workflows)
- [ ] Set up Bearer authentication
- [ ] Activate the workflow (use Production URL)
- [ ] Configure your MCP client with the URL + token
- [ ] Test it!

**Want n8n to USE external MCP servers?**

- [ ] Create a workflow with a trigger (Chat, Webhook, etc.)
- [ ] Add an **AI Agent** node with an LLM
- [ ] Add **MCP Client Tool** node
- [ ] Paste the external MCP server's SSE endpoint
- [ ] Configure authentication
- [ ] Select which tools to use
- [ ] Activate and test!

---

## Summary

```
MCP = Universal plug for AI to talk to tools

n8n + MCP = 
  ┌─────────────────────────────────────────┐
  │  Your n8n workflows become AI-callable  │
  │           (MCP Server Trigger)          │
  │                  +                      │
  │  Your n8n agents can use any MCP tool   │
  │           (MCP Client Tool)             │
  │                  =                      │
  │    Powerful, two-way AI automation      │
  └─────────────────────────────────────────┘
```