# Zero-SDK Interop: How MCP Lets Your Platform Use Other Platforms Without Trusting Them

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Veera%20S%20Gutta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veerasgutta/)

**Published:** May 2026  
**Author:** Veera S Gutta  
**Reading Time:** 14 minutes  
**Status:** Research & Thought Leadership  
**LinkedIn:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

## ⚖️ Legal Disclaimer

**IMPORTANT NOTICE:** This document represents personal learning, research, and experimentation conducted independently. All content is created for educational purposes and knowledge sharing within the AI/ML community.

- 🎓 **Educational Content**: Based on publicly available documentation, open-source tools, and community knowledge
- 📚 **Public Research**: Insights derived from publicly available specs (modelcontextprotocol.io, a2a-protocol.org), Linux Foundation announcements, and conference proceedings (AAIF MCP Dev Summit NA 2026)
- 💡 **Illustrative Examples**: Architecture patterns and code are created for demonstration purposes, not production specifications
- 🚫 **No Proprietary Information**: Contains no confidential information from any employer or client
- 🗣️ **Personal Views**: All opinions expressed are solely my own and do not represent the views of any current or former employer

---

## 📋 Executive Summary

For most of the last decade, "integrating with another platform" meant the same thing: pull in their SDK, learn their object model, take a transitive dependency on their release schedule, and hope their security posture matches yours. Multiply that by every vendor you talk to and you get the **N×M integration tax** — the quiet operating cost of every enterprise architecture.

In late 2024, Anthropic published the **Model Context Protocol (MCP)** to collapse N×M into N+M. By December 2025, MCP had been donated to the Linux Foundation's **Agentic AI Foundation**, with OpenAI, Google, Block, Microsoft, AWS, and most major frameworks shipping support. By the **MCP Dev Summit NA 2026** (April, ~1,200 attendees), the architectural consensus had hardened: **gateway + registry as the agent control plane**, with stateless transports, durable task primitives, and progressive tool discovery.

In parallel, **A2A (Agent2Agent)** — donated by Google to the Linux Foundation in mid-2025 — became the standard for agent↔agent communication, complementing MCP's agent↔tools focus.

The opportunity for an enterprise platform is now sharper than it has ever been: **consume capabilities from any other platform without integrating their SDK, without leaking your internals, and without trusting their schemas at face value.**

This article is about how to do exactly that.

**Key Insights:**
- 🔌 **MCP collapses N×M into N+M** — one client, one server interface, no per-vendor SDK
- 🛡️ **Gateway + Registry is the new control plane** — Uber, Amazon, Docker, Kong, Solo.io all converged here
- 🧱 **Reasoning layer ≠ Action layer** — keep LLM thinking separate from where governance, auth, and mutation enforcement actually live
- 🪪 **Pydantic (or any strict schema) at the boundary** is a security primitive, not a typing convenience
- 🃏 **Minimum-viable Agent Cards** — capability advertisement is an information-disclosure decision
- ⚠️ **Lethal trifecta** (untrusted input + sensitive data + external egress) is the canonical MCP threat model
- 🔁 **Egress hygiene matters as much as ingress** — your tool descriptions, errors, and traces leak your platform if you let them

---

## The N×M Tax Nobody Wants to Pay Anymore

Picture an enterprise AI platform that needs to pull data from a CRM, a ticketing system, a document store, an observability backend, and three internal services. The 2023 answer was: integrate five SDKs. Wire up five auth flows. Maintain five sets of types. Track five release cadences. Re-test the world every time any of them ships a breaking change.

Now picture the same platform needing to expose its own capabilities to *other* organizations' agents. Suddenly you're shipping SDKs in Python, TypeScript, Java, Go, and C# — each one a public surface area you have to support, version, secure, and document. Each one a transitive dependency someone else is now baking into their build.

This is the **N×M problem**: N clients × M services, each pair requiring a bespoke integration. It is the integration shape that gave us GraphQL fatigue, OpenAPI sprawl, and the "we'll just build a custom connector" graveyard.

MCP's bet — now validated by the entire industry — is that AI agents need the **LSP equivalent for tools**. One protocol, JSON-RPC over a stateless transport, with a small set of primitives (resources, tools, prompts), and capability negotiation between hosts and servers. You implement the server *once*; every MCP-aware client can call it. You implement the client *once*; every MCP server in the world becomes reachable.

The 2026 reality:

- **OpenAI, Anthropic, Google DeepMind** all ship MCP support natively.
- **Microsoft Semantic Kernel, Azure OpenAI, Cloudflare Workers** are first-class MCP hosts.
- **Amazon, Uber** run MCP at production scale internally — Uber's GenAI Gateway alone processes tens of thousands of agent executions per week.
- **Linux Foundation governance** via the Agentic AI Foundation removes the "single-vendor protocol" risk that would have killed adoption a decade ago.

The implication for platform builders: **stop shipping SDKs to expose capabilities, and stop pulling in SDKs to consume them.** Both sides of the integration have a better answer.

---

## What "Use Another Platform Without Their SDK" Actually Means

When a partner platform exposes its capabilities through an MCP server, your platform interacts with it the same way it would interact with any other MCP server — by speaking the protocol. There is no SDK to vendor, no auto-generated client to keep in sync, no version ceremony. The contract is the protocol, not the package.

Concretely, this means:

| Old shape (SDK integration) | New shape (MCP consumption) |
|---|---|
| `pip install vendor-sdk==3.4.1` | Configure an MCP server endpoint + auth |
| Vendor's classes leak into your domain model | Your domain model stays clean; only the tool I/O crosses the boundary |
| Breaking change in v4.0 forces a refactor | Server adds a new tool; old tools keep working (capability negotiation) |
| Your security team audits the SDK's transitive deps | Your security team audits one HTTP+JSON-RPC client and a schema validator |
| Your code links into their object model at compile time | Your code calls discovered tools at runtime |

The architectural property that matters most: **the vendor's code never executes inside your process**. Their failures, their dependency choices, their telemetry, their crashes — all stay on the other side of the protocol boundary. That is the isolation property the SDK model can never give you.

---

## The Gateway + Registry Pattern (The 2026 Consensus)

Every serious enterprise MCP deployment in 2026 looks structurally similar. The pattern that emerged from Uber, Amazon, Docker, Kong, Solo.io, and others at the AAIF summit is essentially this:

```
                 ┌─────────────────────────────────────────────┐
                 │              Your Platform                   │
                 │                                              │
                 │   Agent ──► Reasoning Layer (LLM)            │
                 │                  │                           │
                 │                  ▼                           │
                 │     ┌─────────────────────────────┐          │
                 │     │   MCP Gateway (egress)      │          │
                 │     │  ┌───────────────────────┐  │          │
                 │     │  │  Registry (catalog)   │  │          │
                 │     │  │  Auth + scoping       │  │          │
                 │     │  │  Schema validation    │  │          │
                 │     │  │  PII / id scrubbing   │  │          │
                 │     │  │  Audit + replay log   │  │          │
                 │     │  └───────────────────────┘  │          │
                 │     └─────────────┬───────────────┘          │
                 └───────────────────┼──────────────────────────┘
                                     │  (MCP / JSON-RPC over HTTPS)
              ┌──────────────────────┼─────────────────────────┐
              ▼                      ▼                         ▼
        Vendor MCP            Internal MCP              Partner MCP
        Server                Server                    Server
        (CRM)                 (Tickets)                 (A2A bridge)
```

Three things make this pattern work:

### 1. Reasoning Layer ≠ Action Layer

This frame, made sharp by Alex Salazar of Arcade.dev at the 2026 summit, is the simplest mental model in the whole space:

- **Reasoning layer**: where the LLM thinks. It can be wrong, hallucinate, get prompt-injected, or misinterpret a tool description.
- **Action layer**: where things actually happen — data is read, records are mutated, money moves. This is where governance, authorization, and mutation control *must* live.

The gateway is the action layer. The model never talks directly to a vendor MCP server. It asks the gateway, the gateway enforces, the gateway forwards. If the model is compromised, the blast radius stops at the gateway's policy.

### 2. The Registry Is the Source of Truth

The registry knows: which MCP servers exist, what capabilities each exposes, which tenants/agents may call which tools, what scopes apply, and what the current schema for each tool looks like. Tool discovery for agents flows through the registry — not through ad-hoc JSON files committed to repos, and not through ambient environment configuration.

This is also where **progressive tool discovery** lives. Claude Code's published numbers — ~85% reduction in token usage by deferring tool definitions until they're actually relevant — are not about prompt engineering. They're about treating the registry as a queryable index, not a flat dump.

### 3. Egress, Not Just Ingress

Most discussion of MCP security focuses on the *server* side: how do I protect my MCP server from malicious clients? The gateway pattern flips this: how do I protect *my agents and my data* from the MCP servers they consume?

That's the part of the story that matters when you're consuming external platforms — and it's where most teams under-invest.

---

## Schemas at the Boundary: Pydantic as a Security Primitive

Here is the move that elevates an MCP gateway from a proxy to a trust boundary.

Every tool call entering or leaving your platform crosses one or more schemas: the request you send, the response you receive, the A2A message you forward to a peer agent. The naïve approach is to take the vendor's published schema, generate types from it, and trust the wire to match.

The disciplined approach is to define **your own** schemas — typically as Pydantic models in Python (or zod in TypeScript, or Protobuf, or any strict validator) — that describe what your platform is *willing to accept* and *willing to emit*. The vendor's schema describes what *they* offer; your schema describes what *you* will tolerate. These are not the same artifact, and conflating them is how supply-chain bugs get into AI systems.

```python
# Illustrative — not production code

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Literal

class ExternalToolResponse(BaseModel):
    """What we accept back from a partner MCP server.

    Strict by default: unknown fields are rejected, types are coerced
    only where explicitly safe, and free-form text is length-bounded.
    """
    model_config = ConfigDict(extra="forbid", strict=True)

    status: Literal["ok", "partial", "error"]
    record_id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    summary: str = Field(max_length=2_000)
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("summary")
    @classmethod
    def no_control_chars(cls, v: str) -> str:
        if any(ord(c) < 0x20 and c not in ("\n", "\t") for c in v):
            raise ValueError("control characters in summary")
        return v
```

What this buys you, beyond type safety:

1. **Untrusted-by-default ingress.** A partner cannot inject a field your platform didn't ask for. If their server starts returning a new `internal_user_email` field you didn't model, validation rejects it before it reaches your agent. The "tool poisoning" class of attacks — where a server quietly mutates its outputs to smuggle data or instructions — is contained at the schema layer.
2. **Bounded blast radius for prompt injection.** Length caps, character-class restrictions, and explicit enums turn "the LLM will read this" into "the LLM will read at most 2,000 sanitized characters." The lethal trifecta (untrusted input + sensitive context + external egress) cannot fire if your inputs can't carry an unbounded payload.
3. **Stable internal types.** When the partner ships a breaking change, exactly one place in your code breaks: the boundary model. Your domain logic doesn't move.
4. **Replayable audit.** Every validated message is a structured object you can serialize, hash, and store. When a regulator or an incident-response engineer asks "what did the partner actually send us at 03:14 UTC?", the answer is a row in a table, not a guess from logs.

The same model applies in reverse for **A2A messages**. When your agent receives a structured message from another organization's agent, that message is *adversarial input by default* — even if the sender is a trusted partner, the agent on their side may have been jailbroken. Pydantic at the inbound A2A boundary is the cheapest defense in depth you will ever deploy.

---

## Don't Reveal Your Platform: The Minimum-Viable Agent Card

A2A introduces **Agent Cards** — JSON metadata documents that describe what an agent can do, how to reach it, what auth it expects, and what message shapes it understands. Agent Cards are how peer agents discover each other.

They are also, by default, an information-disclosure surface.

The temptation is to publish a maximalist Agent Card: every capability, every parameter, every internal model name, every tool you've wired up. Don't. The Agent Card is the *external* description of your agent, not its internal table of contents.

**Principles for a minimum-viable Agent Card:**

| Do | Don't |
|---|---|
| Advertise capabilities at the **outcome** level ("can summarize a customer interaction") | Enumerate the **tools** that implement the capability |
| Use **stable, generic names** ("knowledge_lookup") | Use **internal product names** ("avinshi-akashic-v3") |
| Expose **per-partner** capability subsets via auth scope | Publish one card that shows everything you can do |
| Return generic, structured **error codes** | Return stack traces, internal IDs, or upstream vendor messages |
| Quote a **stable schema version** the partner can pin | Leak your internal schema migration state |

The same hygiene applies to MCP **tool descriptions** when your platform itself exposes an MCP server. Tool descriptions are read by other organizations' LLMs. They become part of those models' context. Anything you write there is, effectively, broadcast.

A useful test: *if a competitor's research team scraped every Agent Card and tool description we publish, would our roadmap, our internal architecture, or our differentiating logic be visible?* If the answer is yes, you're publishing a marketing brochure as a security boundary.

---

## Egress Hygiene: The Underrated Half of Isolation

Even with a perfect gateway, perfect schemas, and a minimum-viable Agent Card, three subtle channels still leak your platform if you don't close them:

### 1. Error Messages

When a tool call fails, the natural instinct is to bubble the error up. Don't bubble it raw. Strip stack traces, internal hostnames, database identifiers, ORM class names, and upstream vendor error strings. Replace with a stable error code and a generic message. Log the rich version internally for your operators; emit the sanitized version to the wire.

### 2. Telemetry and Trace Headers

OpenTelemetry is wonderful and also a leak vector. If you propagate your own trace IDs, span names, baggage, and service names into outbound MCP calls, you've just told every server you talk to the internal shape of your system — service names, environment, deployment topology. Strip or rewrite outbound trace headers at the gateway. Use distinct trace contexts for internal vs. external spans.

### 3. Tool Output Shape Drift

When you forward a tool's output to your LLM, that output (after validation) becomes part of the model's context. If the model then makes another tool call and includes any of that content in its arguments, **you have just round-tripped the partner's data back to a different partner.** Treat every cross-server hop in a multi-step plan as a fresh egress decision. The gateway is the right place to enforce this — outbound payloads should be re-validated against the *destination's* schema, not assumed safe because they came from "inside."

This is the operational version of the lethal trifecta: untrusted input from one MCP server, sensitive context built up in the agent, egress to a second MCP server. The gateway is the only place that sees both ends.

---

## Putting It Together: A Reference Flow

A single tool call from your agent to an external partner, end to end:

```
Agent decides: "I need to look up customer record X."
       │
       ▼
Call gateway.invoke(capability="customer.lookup", args={...})
       │
       ▼
Gateway:
  1. Look up capability in registry → resolves to partner MCP server + tool name
  2. Check tenant + agent scope → authorized?
  3. Validate outbound args against OUR egress schema (Pydantic)
  4. Strip/rewrite trace headers; attach scoped credentials
  5. Forward as MCP tool call (JSON-RPC over HTTPS)
       │
       ▼
Partner MCP server executes, returns response
       │
       ▼
Gateway:
  6. Validate response against OUR ingress schema (Pydantic, extra="forbid")
  7. Sanitize: drop unknown fields, bound lengths, scrub control chars
  8. Redact PII / partner-internal identifiers
  9. Append to audit log (request hash, response hash, schema version, timestamp)
 10. Return validated, typed object to agent
       │
       ▼
Agent reasons over the validated result.
```

Every numbered step is a place where, in an SDK-based integration, you would have been trusting the vendor's code to do the right thing inside your process. In the MCP+gateway model, *your* code controls each one — and the vendor's code never crosses the boundary.

---

## Where This Aligns with the Rest of the Stack

This article is the third panel of a triptych that also includes [Beyond RAG: Context-Augmented Generation](./beyond-rag-context-augmented-generation.md) (context → agent), [Forget AI Talking to You; The Real Revolution Is AI Talking to AI](./forget-ai-talking-to-you-ai-talking-to-ai.md) (agent ↔ agent), and [The Invisible Fortress](./agentic-os-invisible-fortress-enterprise.md) (agent runtime isolation).

The four layers fit together cleanly:

| Layer | Standard | What it carries |
|---|---|---|
| **Context → Agent** | CAG (architectural pattern) | Identity, session, knowledge, policy, temporal |
| **Agent → Tools/Data** | **MCP** | Discoverable tool calls, resources, prompts |
| **Agent ↔ Agent** | **A2A** | Peer discovery, structured messages, delegation |
| **Agent Runtime** | Agentic OS (architectural pattern) | Isolation, capability-based security, audit |

MCP and A2A are the two protocol layers; CAG and the Agentic OS are the architectural patterns that wrap them. **The gateway is where all four meet.** It is where context is enforced (CAG), where tool calls are governed (MCP), where peer messages are validated (A2A), and where the runtime's isolation guarantees are made real (Agentic OS).

---

## What to Build, in What Order

If you're starting from a platform with vendor SDKs and direct integrations, the migration path is concrete:

1. **Stand up an MCP gateway in front of one external integration.** Pick the noisiest dependency. Forward everything through the gateway. Measure the latency cost (it is small) and the operational win (it is large).
2. **Define Pydantic models for ingress and egress on that one integration.** Reject anything the vendor sends that you didn't ask for. Watch your error logs. You will discover fields you did not know existed. Most of them you do not want.
3. **Add a registry — even a JSON file behind a typed accessor counts.** The point is to centralize "what tools exist and who can call them," not to ship a microservice on day one.
4. **Move the next integration behind the gateway.** Then the next. The SDK directory shrinks. Your dependency graph gets shallower.
5. **Publish your own MCP server** for the capability you most want partners to consume — with a minimum-viable tool description and strict schemas. This replaces the SDK you would otherwise have shipped.
6. **Adopt A2A for any agent-to-agent path that crosses an organizational boundary.** Use Agent Cards as a feature-hiding discipline, not a feature-advertising one.
7. **Wire egress hygiene into the gateway by default** — header stripping, error sanitization, trace context isolation, cross-hop schema re-validation.

Nothing in this list requires a moonshot. Each step is a week of work, individually shippable, individually reversible.

---

## The Compounding Effect

The reason MCP is ending the SDK era is not that SDKs are bad. It is that the *N×M shape* is bad, and AI agents have made the cost of that shape impossible to ignore. Every new model, every new partner, every new internal service was another integration to write, audit, secure, and version.

A protocol-first, gateway-mediated platform inverts the math. The cost of adding a new partner becomes a registry entry and two Pydantic models. The cost of letting partners consume your capabilities becomes one MCP server. The cost of trusting any of them becomes nearly zero — because you don't.

That last sentence is the whole point. **Isolation is not the absence of integration. It is integration done right.**

When your platform can absorb new capabilities from anywhere without adopting anyone else's code, schemas, or assumptions — and expose its own capabilities without revealing how they're built — you have what every enterprise architecture has been trying to build for twenty years: real composability, with the trust boundary in the right place.

The protocols are here. The governance is here. The gateway pattern is here. The only thing left is to build it.

---

## 📚 References & Further Reading

- **MCP specification (2025-11-25):** [modelcontextprotocol.io/specification](https://modelcontextprotocol.io/specification)
- **A2A protocol:** [a2a-protocol.org](https://a2a-protocol.org)
- **Agentic AI Foundation (Linux Foundation):** [aaif.io](https://aaif.io/)
- **AAIF MCP Dev Summit NA 2026 recap:** [InfoQ — Gateways, gRPC, and Observability Signal Protocol Hardening](https://www.infoq.com/news/2026/04/aaif-mcp-summit/)
- **MCP security landscape:** Hou et al., "Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions," arXiv:2503.23278
- **Tool poisoning attacks:** [InvariantLabs — MCP Security Notification](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- **The "lethal trifecta" framing:** Simon Willison, multiple posts (2024–2026)
- **MCP as USB-C for AI:** Edwards, Ars Technica (April 2025)
- **Companion articles in this series:** [Beyond RAG (CAG)](./beyond-rag-context-augmented-generation.md) · [AI ↔ AI (A2A)](./forget-ai-talking-to-you-ai-talking-to-ai.md) · [The Invisible Fortress (Agentic OS)](./agentic-os-invisible-fortress-enterprise.md) · [AI Trust Boundaries](./ai-trust-boundaries-protecting-platforms.md) · [GenAI Validation & Guardrails](./genai-content-validation-production-guardrails.md)
