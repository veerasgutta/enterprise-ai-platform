# The Agent That Marked Its Own Homework

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Veera%20S%20Gutta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veerasgutta/)

**Published:** September 2026  
**Author:** Veera S Gutta  
**Status:** Research & Thought Leadership  
**LinkedIn:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

## ⚖️ Legal Disclaimer

**IMPORTANT NOTICE:** This document represents personal learning, research, and experimentation conducted independently. All content is created for educational purposes and knowledge sharing within the AI/ML community.

- 🎓 **Educational Content**: Based on publicly available documentation, open-source tools, and community knowledge
- 📚 **Public Research**: Insights derived from publicly available academic papers (ArXiv, Stanford HAI, MIT Technology Review, ACM, IEEE) and open-source projects
- 💡 **Illustrative Examples**: Architecture patterns and examples are created for demonstration purposes, not production specifications
- 🚫 **No Proprietary Information**: Contains no confidential information from any employer or client

---

## 📋 Executive Summary

Here is a question worth asking about your most autonomous agent.

**Who approved its last consequential action?**

Not which system. Not which field. Which *person*. Name them.

Most teams can point to a record. Very few can point to a human. And the gap between those two things is where almost every oversight control in production quietly fails.

**Key Insights:**
- 🧾 **Separation of duties is the oldest control we have** — and it never made it into agent architecture. We enforce it rigorously for money and abandoned it entirely for autonomy.
- ✅ **A flag is not a person.** An approval that can't be traced to a named human, an exact action, and a moment in time is a claim, not a control.
- 🕳️ **Absence is not a pass.** In most systems "unknown" quietly reads as "fine," and advancement happens on missing evidence rather than good evidence.
- ➗ **Averaging is how safety findings disappear.** A categorical finding and a quality score are different kinds of fact, and one should never be allowed to dilute the other.
- 🤝 **Agreement is not correctness.** Agents ratifying other agents is a committee, not a check.
- 🏛️ **The frontier labs just spent a month hiring outside graders.** That is the whole argument, made in public, by the people with the most to lose from making it.

---

Every enterprise on earth enforces one rule without being asked.

The person who raises the invoice cannot be the person who approves the payment. The engineer who writes the change cannot be the only one who reviews it. The lab running the trial does not get to be the body that certifies the result.

We don't debate this. It's plumbing. It survived because it doesn't depend on anyone being trustworthy — it works precisely *because* it assumes nobody is.

Then we built agent systems, and quietly dropped it.

---

## How the Three Roles Collapsed

In a healthy control, three roles stay separate. Someone **does** the thing. Someone else **approves** it. Someone else again **verifies** it happened correctly.

In most agent deployments I've looked at, all three have folded into the same party — not by decision, but by accretion. Nobody removed the oversight. It just stopped being exercised by anyone other than the thing being overseen.

Here are the five ways it happens. None of them look like a failure while they're happening.

| The collapse | What it looks like in practice | Why it passes review | What it actually proves |
|---|---|---|---|
| **Self-classified risk** | The request declares how risky it is, and the gate trusts the declaration | The classification field is populated and well-formed | That the requester knows which answer opens the gate |
| **The approval flag** | A boolean travels with the call saying a human approved this | There's an approval field and it says yes | That something, somewhere, set a variable |
| **Peer ratification** | Other agents review the output and concur | Multiple independent reviewers agreed | That they share a blind spot |
| **Advancement on absence** | Qualification proceeds because nothing negative was recorded | No failures on file | That nobody was measuring |
| **The averaged finding** | A real safety flag is folded into an aggregate quality score and the total passes | The composite score cleared the bar | That the bar is measuring the wrong thing |

Look at the middle column. Every one of those would survive an audit. Every one produces a clean record. That's the problem — these aren't gaps in the paperwork. **The paperwork is immaculate.** It just isn't describing what everyone believes it describes.

---

## A Flag Is Not a Person

The approval boolean deserves its own paragraph, because it's the most common and the most deceptive.

Somewhere in most agent stacks, a value travels with a request that means *a human said yes to this*. Downstream, a gate reads it and steps aside. It works. It's clean. It's in the logs.

And it establishes nothing.

The flag doesn't know which human. It doesn't know which action they were looking at when they said yes — possibly a summary, possibly a different version of the plan, possibly a batch of forty requests approved in one click. It doesn't know when. It doesn't know whether the thing that eventually executed is the thing they saw.

A real approval binds four things together and refuses to exist without all four: **a named person, an exact action against an exact target, the moment it was given, and an expiry.** Anything weaker is a claim in transit, and claims in transit can be set by anyone who can reach the code path.

This is the same reason a signature matters more than a tick box. Not because handwriting is magic — because a signature is *attached to a specific document at a specific time*, and a tick box floats free.

---

## Absence Is Not a Pass

This is the quietest of the five, and in my experience the most widespread.

An agent comes up for more authority. The system checks the record. There's nothing bad in it. Authority granted.

But there are two very different reasons a record can be clean. One is that the thing performed well under observation. The other is that **nobody was observing.** Almost no system distinguishes them, because both produce the same absence — and absence is the easiest thing in the world to mistake for a good result.

The correction is one line of policy and it's worth writing down: *missing evidence routes to the safe branch, never the permissive one.* Unknown is not a synonym for fine. It's a synonym for we don't know, and we don't know should never be the basis for increasing what something is allowed to do on its own.

---

## Never Average a Safety Finding

The fifth collapse is the most technically seductive, because aggregate scores are genuinely useful and the failure mode looks like good engineering.

You have an evaluator. It produces a composite — quality, helpfulness, format, latency, and somewhere in the mix, safety. The composite clears the threshold. It passes.

Inside that composite there was a real finding. A possible leak. A refusal that should have fired and didn't. Something categorical. And it got outvoted by four dimensions that had a good day.

A categorical finding and a quality score are not the same kind of fact, and no amount of weighting makes them commensurable. One says *this is good*. The other says *this is not allowed*. The second should never be able to lose an argument to the first.

The practical rule: safety findings get their own verdict, computed separately, with the power to fail the whole thing on their own. Uncertain findings don't get rounded toward passing — they get escalated. A single real finding at a mediocre confidence should outrank a strong average, every time.

---

There's a scene in the Mahabharata, the great epic of ancient India, that everyone remembers as a story about gambling. It isn't.

A king is invited to a game of dice. He plays against a man who is rolling on behalf of the other side — the side that gains everything the king loses. Nobody hides this. The hall is full of elders and they watch the whole thing. The rules are followed. Every throw is announced properly. He loses his wealth, then his kingdom, then his brothers, then himself.

So why did nobody stop it?

Because nothing about the procedure was wrong. The form was perfect. The only thing wrong was who was holding the dice.

The game was fair. The dice were not.

We assume a decision is sound if the process was followed. It isn't. It's sound if whoever ran the process had nothing to gain from the answer.

---

## The Labs Just Said This Out Loud

The reason to write this now is that the people with the most to lose from admitting it spent the last month admitting it.

Inside a few weeks: a frontier lab partnering with an outside firm on **embedded evaluation**. A **verification programme** for a high-stakes domain, gating who may use what. A published **framework for reporting model misalignment** — a reporting framework, aimed outward. A **threat intelligence report** detailing eight months of misuse caught and disrupted. An **independent external review** commissioned after models were found to have gained access they shouldn't have had. And a proposal for **metrics that would let people outside the labs see the pace of development inside them**, published with the plain observation that right now, the world can't see in.

Read those as products and they're a scattered quarter. Read them together and they're one move, made six times: **stop asking the system to report on itself.**

That's not a safety story. It's a governance story, and it's the same rule accounting figured out centuries ago, arriving in AI the way these things always arrive — after the first few incidents, all at once, from the people who can least afford to be wrong about it.

Enterprises will get here too. The only variable is whether it's by design or by incident.

---

## What This Looks Like In Practice

Four changes. None of them exotic.

**1. Approvals bind, or they don't count.** A person, an exact action and target, a timestamp, an expiry. Single use. If the action that executes isn't the action that was shown, the approval doesn't carry. A boolean in flight is not an approval — it's a rumour with good formatting.

**2. Nothing supplies its own classification.** Risk level, reviewer identity, qualification status, and trusted-evidence status are determined by the thing enforcing the gate, never by the thing requesting passage. If a request can describe itself as low risk, that field is decoration.

**3. Unknown routes to safe.** Missing evidence never advances authority. Write it as a rule so it survives the sprint where someone needs the pipeline to go green.

**4. The verifier is a different party, and has an owner too.** Whatever checks the work should not report to the work. And it needs its own qualification, its own audit coverage, and someone accountable for it — otherwise you've just moved the collapse one level up and stopped looking at it.

---

## The Part Nobody Wants to Hear

Separation of duties is slower. That's not a side effect; it's the mechanism. The whole reason it works is that it inserts a party with no stake in the outcome, and parties with no stake in the outcome are, by design, not in a hurry.

Which means adopting this will make some of your automation look worse. Approvals that used to clear instantly will queue. Agents that used to advance on a clean record will sit until someone actually measures them. A few composites that used to pass will start failing on a single finding, and someone will file a ticket asking why the eval got stricter.

It didn't get stricter. It got honest.

The trade is the same one every finance department made a long time ago, and nobody in finance is arguing to go back.

---

## What To Do Next

One exercise. It takes an afternoon and it's worth more than any framework.

**Take your three most consequential agent actions. For each one, write down three names: who authored it, who approved it, who verified it worked.**

Three columns. Real names, not systems.

You'll find one of three things. Sometimes all three are different people — those are fine, leave them alone. Sometimes two of the three are the same party, which is a known risk you can now decide about deliberately. And sometimes one of the columns turns out to contain a field name rather than a person.

That last group is your actual risk register. It is usually shorter than people fear and considerably more uncomfortable than they expect, because the discovery isn't that oversight was weak. It's that there was a complete and beautifully formatted record of oversight that nobody had actually performed.

Most teams have never made this list.

---

## One Last Thought

We spent a century making sure no single person could move money alone, sign off on their own expenses, or audit their own books. We built entire professions around the principle that the checker must have nothing to gain.

Then we built systems where one process does the work, marks the work, and files the report saying the work went well — and we called the report evidence.

Permission asks whether an agent *may* act.
Reversibility asks whether you can take it back.
This one asks something simpler and more awkward:

**when your system tells you everything is fine, who is actually speaking?**

---

---

**Related Articles:**
- [Capability Is Becoming a Privilege](./capability-is-becoming-a-privilege-earned-agent-access.md)
- [Eval-Driven Development: Building AI Pipelines That Judge Themselves](./eval-driven-development-ai-pipeline-judges.md)
- [Prove It Without Keeping It](./prove-it-without-keeping-it-zero-retention-audit.md)
- [Power You Can't Withdraw Isn't Authority](./reversibility-undo-problem-agent-autonomy.md)
- [Getting In Is the Easy Part](./agent-exit-problem-long-running-agents.md)
- [Digital Colleagues: Accountability, Ownership & Judgment](./digital-colleagues-accountability-ownership-judgment.md)
- [AI Trust Boundaries: Protecting Platforms in the Age of Agentic AI](./ai-trust-boundaries-protecting-platforms.md)
- [Trust but Verify: GenAI Content Validation & Production Guardrails](./genai-content-validation-production-guardrails.md)
- [The Agent That Remembers: Why Persistent Memory Is the Next Trust Boundary](./agent-memory-persistent-state-trust-boundary.md)
- [The Dharma Machine: Ancient Indian Wisdom & Governing AI](./the-dharma-machine-ancient-indian-wisdom-governing-ai.md)

---

**Connect with me:** [linkedin.com/in/veerasgutta](https://www.linkedin.com/in/veerasgutta/)

---

## 🔗 Related in this series

- [Eval-Driven Development](./eval-driven-development-ai-pipeline-judges.md) — that article argued you need a judge; this one asks who the judge works for
- [Capability Is Becoming a Privilege](./capability-is-becoming-a-privilege-earned-agent-access.md) — what earns authority; this one covers who is allowed to certify that it was earned
- [Prove It Without Keeping It](./prove-it-without-keeping-it-zero-retention-audit.md) — the evidence that survives deletion, and why an attestation needs an author
- [Digital Colleagues: Accountability, Ownership & Judgment](./digital-colleagues-accountability-ownership-judgment.md) — who answers for the approval nobody gave

---

*The game was fair. The dice were not.*
