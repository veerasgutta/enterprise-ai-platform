# When Agents Form a Loop

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Veera%20S%20Gutta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veerasgutta/)

**Published:** October 2026  
**Author:** Veera S Gutta  
**Status:** Research & Thought Leadership  
**LinkedIn:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

A customer sends a simple request:

> "Can we move Friday's shipment to our Toronto warehouse instead?"

The platform routes the message to the **Shipping Agent**.

The Shipping Agent checks its instructions: *Never book a cross-border carrier until Compliance approves the destination address.* So it sends a sub-task to the **Compliance Agent**: "Please approve the Toronto warehouse address for Order #402."

The Compliance Agent checks its own instructions: *Never approve a cross-border shipment without a confirmed carrier and delivery date.* So it sends a sub-task to the **Shipping Agent**: "Please confirm the carrier and Friday delivery slot for Order #402 before compliance review."

The Shipping Agent receives that request as a fresh task. To confirm the carrier, it first needs address approval. So it calls the Compliance Agent again.

Neither agent is broken. Neither agent is hallucinating. Each one is following a sensible business rule written by a different team.

Fifteen minutes later, that single customer question has generated hundreds of polite, well-formed calls between the two agents, consumed the workflow's token budget, and still produced no answer for the customer.

**Each rule made sense on its own. Together, they built a room with no door.**

*This is an illustrative scenario, not a reported incident.*

## Why Machines Don't Hang Up

Every customer has experienced the human version of this loop.

You call your bank to update an address. Account Services transfers you to Card Security because there is an active travel notice on your account. Card Security tells you they cannot touch the notice until Account Services updates your address, and transfers you right back.

When that happens to a person, the loop ends quickly. On the second transfer, you realize what is happening, lose patience, and ask for a supervisor—or hang up.

An AI agent never loses patience.

It does not notice that it is having the same conversation for the fortieth time unless the system is built to track it. Worse, modern agents are prompted to be persistent, helpful, and thorough. When a tool call does not return the final answer, the agent tries another angle, rephrases the request, and keeps going.

What stops a human loop is frustration. In an automated workflow, you have to replace frustration with architecture.

## Why Normal Monitoring Misses It

When a loop like this happens in production, it rarely triggers a traditional alert at first.

Look at how the traffic appears to standard infrastructure monitoring:

| What Standard Monitoring Checks | What It Sees in an Agent Loop | What Is Actually Happening |
|---|---|---|
| **User traffic volume** | One normal request from one authenticated customer | That single request is multiplying inside the service mesh |
| **Payload validity** | Well-formed JSON matching the expected schema | The same unresolved dependency is being passed back and forth |
| **Service health** | Fast responses, HTTP 200 status codes, zero crashes | Agents are succeeding at calling each other while failing the task |
| **Per-agent limits** | Each individual call stays within its token and time limit | The combined chain of calls is quietly draining the budget |

To a normal API gateway, nothing looks wrong. The user only clicked send once. Every internal call carries valid credentials. Every response arrives on time.

The system looks busy and healthy right up until the budget alarm fires or the customer asks why a simple address change is still "in progress."

**A healthy step is not proof of a moving workflow.**

## The Problem of Two Witnesses

The logicians of ancient India had a rule for arguments that travel in a circle.

Imagine two witnesses standing before a judge. The first speaker says his claim is true because the second speaker vouches for it. The second speaker says his word can be trusted because the first speaker vouches for him.

So how do you judge a case like that?

You throw out both claims.

Call a witness to prove a claim, and if that witness points right back to the first speaker for proof, nothing has been established. You just have two people in a room pointing at each other.

Two witnesses. Zero proof.

We assume a request gets closer to an answer each time one specialist agent hands it to another. It doesn't. Passing a question around a circle feels like activity, but it never creates the missing piece of information.

## Four Rules That Break the Circle

Stopping multi-agent loops does not require smarter prompts. It requires a few plain rules enforced outside the agents' own reasoning.

**1. Count Handoffs Across the Whole Request**

Do not just limit how long a single agent can think. Put a strict cap on how many times a single user request can be handed from one agent to another. In most business workflows, if a task has bounced across four or five handoffs without producing new verified data, it is not making progress. Stop the chain and surface it for review.

**2. Never Delegate Back to an Agent That Is Already Waiting**

If the Shipping Agent is paused and waiting for an answer from the Compliance Agent, the Compliance Agent must not be allowed to open a new sub-task back to the Shipping Agent on the same order. Track the chain of who called whom. The moment a request points back to an ancestor in the same chain, block the call and flag the conflict.

**3. Budget the Customer Request, Not Just the Agent**

If you give five agents a budget of $0.50 each, a loop across those agents will happily spend $25.00 one polite call at a time. Attach one shared budget—tokens, tool calls, and elapsed time—to the originating request. Every sub-task draws from the same envelope. When the envelope is empty, the entire chain stops together.

**4. Make "Blocked by a Conflict" a Valid Outcome**

Many agent loops happen for a simple reason: the agents were never given a clean way to say, *"These two rules contradict each other."* When every prompt tells the agent to complete the task at all costs, it will keep trying forever. Give agents an explicit outcome state for policy or dependency deadlocks, so stopping early is treated as a success rather than a failure.

## A Ten-Minute Design Review

Before you connect two or more specialist agents in production, run this check on a whiteboard:

Pick any two agents that are allowed to call each other—such as **Order Management** and **Fraud Review**, or **IT Provisioning** and **Security Approval**.

Write down what Agent A requires from Agent B before acting. Then write down what Agent B requires from Agent A.

Now ask one question:

**What happens when a request arrives where both pieces of information are missing at the same time?**

If the answer is that Agent A asks Agent B, and Agent B asks Agent A, you have found your loop before your customers did.

## One Last Thought

Connecting specialist agents is the easy part of multi-agent design.

The discipline that makes them dependable is deciding in advance what happens when two sensible rules point at each other—and making sure the system knows how to stop, explain the deadlock, and ask for help.

*Autonomy is not just knowing who to ask next. It is knowing when asking again will not change the answer.*

---

## ⚖️ Legal Disclaimer

**IMPORTANT NOTICE:** This document represents personal learning, research, and experimentation conducted independently. All content is created for educational purposes and knowledge sharing within the AI/ML community.

- 🎓 **Educational Content**: Based on publicly available documentation, open-source tools, and community knowledge
- 📚 **Public Research**: Insights derived from publicly available academic papers (ArXiv, Stanford HAI, MIT Technology Review, ACM, IEEE) and open-source projects
- 💡 **Illustrative Examples**: Architecture patterns and examples are created for demonstration purposes, not production specifications
- 🚫 **No Proprietary Information**: Contains no confidential information from any employer or client
- 🧭 **High-Level Pattern Only**: This article intentionally avoids describing specific platform internals, registry design, or implementation details; it stays at the governance and architectural pattern level.

---

## 🔗 Related in this series

- [When Agents Invent Their Own Slang](./when-agents-invent-their-own-slang.md) — why multi-agent swarms optimize for mutual speed over human legibility, and what the Stranger Test demands.
- [The Agent That Marked Its Own Homework](./agent-marked-its-own-homework-separation-of-duties.md) — why the agent doing the work cannot be the party certifying that the work was safe.
- [The Rules You Can't Relax](./gated-autonomy-rules-you-cant-relax.md) — why prompt-based guardrails fail when users plead emergencies, and why autonomy needs hierarchical composition.
- [Power You Can't Withdraw Isn't Authority](./reversibility-undo-problem-agent-autonomy.md) — why reversibility, not permission, is the real ceiling on agent autonomy.
- [Forget AI Talking to You. The Real Revolution Is AI Talking to AI.](./forget-ai-talking-to-you-ai-talking-to-ai.md) — why machine-to-machine coordination is the real shift, and where the boundaries must be drawn.

**Connect with me:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)
